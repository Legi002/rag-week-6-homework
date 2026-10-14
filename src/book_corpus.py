from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
from typing import Optional, Tuple


NORMALIZER_VERSION = "lf-v1"
PARSER_VERSION = "prince-sections-v1"
SOURCE_URL = "https://www.gutenberg.org/ebooks/1232"
DOWNLOAD_URL = "https://www.gutenberg.org/cache/epub/1232/pg1232.txt"
START_MARKER = "*** START OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***"
END_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***"

FRONT_ANCHORS = (
    ("introduction", "INTRODUCTION", "front-matter"),
    ("youth", "YOUTH — Æt. 1-25—1469-94", "front-matter"),
    ("office", "OFFICE — Æt. 25-43—1494-1512", "front-matter"),
    ("literature-death", "LITERATURE AND DEATH — Æt. 43-58—1512-27", "front-matter"),
    ("man-works", "THE MAN AND HIS WORKS", "front-matter"),
    ("dedication", "DEDICATION", "front-matter"),
)
ROMAN_NUMERALS = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI")
PRINCE_SECTION_IDS = (
    "editorial-note", "introduction", "youth", "office", "literature-death",
    "man-works", "dedication", *("chapter-%02d" % n for n in range(1, 27)),
    "appendix-valentino", "appendix-castruccio",
)


class BookInputError(ValueError):
    """An actionable local-source or book-configuration error."""


def parser_id_component(parser_version: str) -> str:
    """Return the stable identifier component for a versioned parser name."""
    match = re.search(r"-v([0-9]+)$", parser_version)
    if match is None:
        raise ValueError("parser_version must end with -v followed by a version number")
    return "p" + match.group(1)


@dataclass(frozen=True)
class BookManifest:
    ebook_id: str
    title: str
    author: str
    translator: str
    language: str
    release_date: str
    updated_date: str
    source_sha256: str
    body_sha256: str
    section_ids: Tuple[str, ...]
    normalizer_version: str = NORMALIZER_VERSION
    parser_version: str = PARSER_VERSION


PRINCE_MANIFEST = BookManifest(
    ebook_id="1232",
    title="The Prince",
    author="Niccolò Machiavelli",
    translator="W. K. Marriott",
    language="English",
    release_date="2006-02-11",
    updated_date="2026-07-24",
    source_sha256="948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368",
    body_sha256="347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1",
    section_ids=PRINCE_SECTION_IDS,
)


@dataclass(frozen=True)
class SourceSection:
    section_id: str
    heading: str
    kind: str
    heading_start: int
    content_start: int
    end_char: int
    doc_id: str


@dataclass(frozen=True)
class BookCorpus:
    doc_id: str
    title: str
    author: str
    translator: str
    language: str
    ebook_id: str
    release_date: str
    updated_date: str
    source_url: str
    download_url: str
    raw_sha256: str
    source_sha256: str
    body_sha256: str
    body_text: str
    sections: Tuple[SourceSection, ...]
    manifest: BookManifest
    imported_at_utc: Optional[str] = None


@dataclass(frozen=True)
class SentenceSpan:
    section_id: str
    start_char: int
    end_char: int


def _canonicalize(text: str) -> str:
    if text.startswith("\ufeff"):
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _field(header: str, label: str) -> str:
    match = re.search(r"(?m)^" + re.escape(label) + r":\s*(.*?)\s*$", header)
    if not match:
        raise BookInputError("The source header is missing required metadata: " + label + ".")
    return match.group(1)


def _metadata(header: str) -> dict:
    title = _field(header, "Title")
    author = _field(header, "Author")
    translator = _field(header, "Translator")
    language = _field(header, "Language")
    release = re.search(r"(?m)^Release date:\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})\s+\[eBook #(\d+)\]", header)
    updated = re.search(r"(?m)^\s*Most recently updated:\s*([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})\s*$", header)
    if not release or not updated:
        raise BookInputError("The source header has a malformed release date, update date, or ebook number.")
    months = {name.lower(): number for number, name in enumerate(("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"), start=1)}
    try:
        release_date = "%04d-%02d-%02d" % (int(release.group(3)), months[release.group(1).lower()], int(release.group(2)))
        updated_date = "%04d-%02d-%02d" % (int(updated.group(3)), months[updated.group(1).lower()], int(updated.group(2)))
    except KeyError as exc:
        raise BookInputError("The source header contains an unrecognized month name.") from exc
    return {"title": title, "author": author, "translator": translator, "language": language,
            "release_date": release_date, "updated_date": updated_date, "ebook_id": release.group(4)}


def _check_identity(metadata: dict, manifest: BookManifest) -> None:
    for key in ("ebook_id", "title", "author", "translator", "language", "release_date", "updated_date"):
        if metadata[key] != getattr(manifest, key):
            raise BookInputError("Source metadata does not match the selected edition (" + key + ").")


def _line_records(text: str):
    offset = 0
    for line in text.splitlines(keepends=True):
        plain = line[:-1] if line.endswith("\n") else line
        yield offset, offset + len(plain), plain
        offset += len(line)
    if not text or not text.endswith("\n"):
        return


def _parse_sections(body: str, manifest: BookManifest, doc_id: str) -> Tuple[SourceSection, ...]:
    lines = list(_line_records(body))
    events = []

    def add_unique(section_id, kind, matcher, title_mode):
        found = [(idx, start, end, line) for idx, (start, end, line) in enumerate(lines) if matcher(line)]
        if len(found) != 1:
            raise BookInputError("Expected exactly one source anchor for section " + section_id + ".")
        idx, start, end, line = found[0]
        if title_mode == "same-line":
            heading = line
            content_start = end + (1 if end < len(body) and body[end] == "\n" else 0)
        else:
            title_lines = [line]
            last_end = end
            cursor = idx + 1
            while cursor < len(lines):
                _s, e, following = lines[cursor]
                if not following or not following.isupper():
                    break
                title_lines.append(following)
                last_end = e
                cursor += 1
            heading = " ".join(title_lines)
            content_start = last_end + (1 if last_end < len(body) and body[last_end] == "\n" else 0)
        events.append({"id": section_id, "kind": kind, "start": start, "content": content_start, "heading": heading})

    add_unique("editorial-note", "editorial-note", lambda s: s.startswith("_ Nicolo Machiavelli, born at Florence"), "same-line")
    # The note anchor is itself source prose, so its indexed content starts at its first character.
    events[-1]["content"] = events[-1]["start"]
    for section_id, anchor, kind in FRONT_ANCHORS:
        add_unique(section_id, kind, lambda s, anchor=anchor: s == anchor, "same-line")

    chapter_matches = []
    chapter_re = re.compile(r"^CHAPTER ([IVXLCDM]+)\.(?:\[\d+\])?$")
    for idx, (start, end, line) in enumerate(lines):
        match = chapter_re.fullmatch(line)
        if match:
            chapter_matches.append((idx, start, end, match.group(1), line))
    markers = [item[3] for item in chapter_matches]
    if markers != list(ROMAN_NUMERALS):
        raise BookInputError("Chapter markers must be exactly I through XXVI, once each and in order.")
    for number, (idx, start, end, roman, line) in enumerate(chapter_matches, start=1):
        title_lines = []
        last_end = end
        cursor = idx + 1
        while cursor < len(lines):
            _s, e, following = lines[cursor]
            if not following or not following.isupper():
                break
            title_lines.append(following)
            last_end = e
            cursor += 1
        if not title_lines:
            raise BookInputError("Chapter " + roman + " has no uppercase title lines.")
        events.append({"id": "chapter-%02d" % number, "kind": "chapter", "start": start,
                       "content": last_end + (1 if last_end < len(body) and body[last_end] == "\n" else 0),
                       "heading": " ".join(title_lines)})

    add_unique("appendix-valentino", "appendix", lambda s: s == "DESCRIPTION OF THE METHODS ADOPTED BY THE DUKE VALENTINO WHEN MURDERING", "multiline")
    add_unique("appendix-castruccio", "appendix", lambda s: s == "THE LIFE OF CASTRUCCIO CASTRACANI OF LUCCA", "multiline")

    events.sort(key=lambda item: item["start"])
    ids = tuple(item["id"] for item in events)
    if ids != tuple(manifest.section_ids):
        raise BookInputError("Book sections are missing, duplicated, reordered, or outside the supported structure.")
    dedication = next(item for item in events if item["id"] == "dedication")
    banners = [(start, line) for start, _end, line in lines if line == "THE PRINCE" and start > dedication["start"]]
    if len(banners) != 1:
        raise BookInputError("The standalone THE PRINCE banner after DEDICATION is missing or duplicated.")

    sections = []
    for index, event in enumerate(events):
        end_char = events[index + 1]["start"] if index + 1 < len(events) else len(body)
        if event["id"] == "dedication":
            end_char = banners[0][0]
        if not (0 <= event["start"] <= event["content"] < end_char <= len(body)) or not body[event["content"]:end_char].strip():
            raise BookInputError("Section " + event["id"] + " is empty or has invalid source ranges.")
        sections.append(SourceSection(event["id"], event["heading"], event["kind"], event["start"], event["content"], end_char, doc_id))
    return tuple(sections)


def load_book_corpus(path, *, manifest: BookManifest = PRINCE_MANIFEST) -> BookCorpus:
    source_path = Path(path)
    if not source_path.exists():
        raise BookInputError("Cannot read the selected source file because it does not exist.")
    if not source_path.is_file():
        raise BookInputError("The selected source path must be a regular file.")
    try:
        raw_bytes = source_path.read_bytes()
    except OSError as exc:
        raise BookInputError("Cannot read the selected source file: " + str(exc)) from exc
    try:
        decoded = raw_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise BookInputError("The source file must use valid UTF-8 encoding.") from exc
    canonical = _canonicalize(decoded)
    raw_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    source_sha256 = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if source_sha256 != manifest.source_sha256:
        raise BookInputError("The source digest does not match the researched edition; only the reviewed manifest and evaluation may change this.")

    header, separator, _rest = canonical.partition(START_MARKER)
    if not separator:
        raise BookInputError("The source is missing the standalone Gutenberg START marker.")
    metadata = _metadata(header)
    _check_identity(metadata, manifest)
    starts = list(re.finditer(r"(?m)^" + re.escape(START_MARKER) + r"$", canonical))
    ends = list(re.finditer(r"(?m)^" + re.escape(END_MARKER) + r"$", canonical))
    if len(starts) != 1 or len(ends) != 1 or starts[0].end() >= ends[0].start():
        raise BookInputError("The source must contain one ordered standalone START and END marker.")
    body_start = starts[0].end()
    if body_start < len(canonical) and canonical[body_start] == "\n":
        body_start += 1
    body = canonical[body_start:ends[0].start()]
    body_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if body_sha256 != manifest.body_sha256:
        raise BookInputError("The canonical book body digest does not match the selected edition.")
    doc_id = "pg1232-" + source_sha256
    sections = _parse_sections(body, manifest, doc_id)
    return BookCorpus(doc_id, metadata["title"], metadata["author"], metadata["translator"], metadata["language"], metadata["ebook_id"], metadata["release_date"], metadata["updated_date"], SOURCE_URL, DOWNLOAD_URL, raw_sha256, source_sha256, body_sha256, body, sections, manifest)


def book_sentence_spans(book: BookCorpus):
    boundary = re.compile(r"[.!?](?=\s|$)")
    spans = []
    for section in book.sections:
        content = book.body_text[section.content_start:section.end_char]
        start = 0
        for match in boundary.finditer(content):
            end = match.end()
            sentence_start = start
            while sentence_start < end and content[sentence_start].isspace():
                sentence_start += 1
            if sentence_start < end:
                spans.append(SentenceSpan(section.section_id, section.content_start + sentence_start, section.content_start + end))
            start = end
        tail_start = start
        while tail_start < len(content) and content[tail_start].isspace():
            tail_start += 1
        if tail_start < len(content):
            spans.append(SentenceSpan(section.section_id, section.content_start + tail_start, section.end_char))
    return spans
