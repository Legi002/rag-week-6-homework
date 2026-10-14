import hashlib
from pathlib import Path

import pytest
from typing import Union

from src.book_corpus import BookInputError, PRINCE_MANIFEST, load_book_corpus
from tests.book_fixture import make_fixture_text, fixture_manifest


def write(tmp_path: Path, value: Union[str, bytes]) -> Path:
    path = tmp_path / "book.txt"
    path.write_bytes(value.encode("utf-8") if isinstance(value, str) else value)
    return path


def test_fixture_loads_only_with_explicit_fixture_manifest(tmp_path):
    path = write(tmp_path, make_fixture_text())
    with pytest.raises(BookInputError, match="supported edition|fingerprint|digest"):
        load_book_corpus(path)
    book = load_book_corpus(path, manifest=fixture_manifest())
    assert book.title == "The Prince"
    assert book.translator == "W. K. Marriott"
    assert book.ebook_id == "1232"


def test_missing_and_nonfile_paths_are_actionable(tmp_path):
    with pytest.raises(BookInputError, match="read|file|exist"):
        load_book_corpus(tmp_path / "missing.txt", manifest=fixture_manifest())
    with pytest.raises(BookInputError, match="file"):
        load_book_corpus(tmp_path, manifest=fixture_manifest())


def test_unreadable_path_is_wrapped_without_os_traceback(tmp_path, monkeypatch):
    path = write(tmp_path, make_fixture_text())
    def denied(_self):
        raise PermissionError("denied")
    monkeypatch.setattr(Path, "read_bytes", denied)
    with pytest.raises(BookInputError, match="read"):
        load_book_corpus(path, manifest=fixture_manifest())


def test_invalid_utf8_is_rejected(tmp_path):
    path = write(tmp_path, b"\xff\xfe")
    with pytest.raises(BookInputError, match="UTF-8"):
        load_book_corpus(path, manifest=fixture_manifest())


@pytest.mark.parametrize("mutation", [
    lambda text: text.replace("*** START OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***", "START missing", 1),
    lambda text: text.replace("Author: Nicolo Machiavelli", "Author: Someone Else", 1),
    lambda text: text.replace("Title: The Prince", "Title: Other Book", 1),
])
def test_marker_or_metadata_mismatch_is_rejected(tmp_path, mutation):
    raw = mutation(make_fixture_text())
    path = write(tmp_path, raw)
    with pytest.raises(BookInputError):
        load_book_corpus(path, manifest=fixture_manifest())


def test_changed_content_with_plausible_metadata_fails_fingerprint(tmp_path):
    raw = make_fixture_text().replace("period in Florence", "period somewhere", 1)
    path = write(tmp_path, raw)
    manifest = fixture_manifest()
    with pytest.raises(BookInputError, match="digest|fingerprint"):
        load_book_corpus(path, manifest=manifest)


def test_bom_and_line_endings_do_not_change_canonical_identity(tmp_path):
    canonical = make_fixture_text()
    variant = "\ufeff" + canonical.replace("\n", "\r\n")
    path = write(tmp_path, variant)
    book = load_book_corpus(path, manifest=fixture_manifest(canonical))
    assert book.source_sha256 == hashlib.sha256(canonical.encode()).hexdigest()
    assert book.body_text == fixture_manifest_body(canonical)


def fixture_manifest_body(raw: str) -> str:
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***\n"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***"
    return raw.split(start_marker, 1)[1].split(end_marker, 1)[0]


def test_production_manifest_rejects_synthetic_even_with_plausible_metadata(tmp_path):
    path = write(tmp_path, make_fixture_text())
    with pytest.raises(BookInputError):
        load_book_corpus(path, manifest=PRINCE_MANIFEST)
from pathlib import Path

import pytest
from typing import Union

from src.book_corpus import BookInputError, load_book_corpus
from tests.book_fixture import fixture_body, fixture_manifest, make_fixture_text


def load_variant(tmp_path: Path, raw: str):
    path = tmp_path / "mutated.txt"
    path.write_text(raw, encoding="utf-8", newline="")
    return load_book_corpus(path, manifest=fixture_manifest(raw))


def test_parser_has_exact_35_ordered_sections_and_26_chapters(tmp_path):
    book = load_variant(tmp_path, make_fixture_text())
    assert len(book.sections) == 35
    assert [section.section_id for section in book.sections] == list(book.manifest.section_ids)
    chapters = [section for section in book.sections if section.kind == "chapter"]
    assert len(chapters) == 26
    assert chapters[17].section_id == "chapter-18"
    assert "XVIII.[1]" in book.body_text[chapters[17].heading_start:chapters[17].content_start]


def test_multiline_uppercase_titles_are_displayed_without_moving_source_text(tmp_path):
    body = fixture_body().replace("SYNTHETIC CHAPTER 1 TITLE\n\n", "FIRST UPPER TITLE\nSECOND UPPER LINE\n\n", 1)
    book = load_variant(tmp_path, make_fixture_text(body))
    first = book.sections[7]
    assert first.heading == "FIRST UPPER TITLE SECOND UPPER LINE"
    assert book.body_text[first.heading_start:first.content_start].endswith("SECOND UPPER LINE\n")


def test_contents_banner_and_license_are_not_indexed(tmp_path):
    book = load_variant(tmp_path, make_fixture_text())
    indexed = "\n".join(book.body_text[s.heading_start:s.end_char] for s in book.sections)
    assert "Contents" not in indexed
    assert "Excluded title banner" not in indexed
    assert "Project Gutenberg License" not in indexed
    assert "THE PRINCE\nExcluded title banner" not in indexed


def test_appendix_byline_remains_inside_content(tmp_path):
    book = load_variant(tmp_path, make_fixture_text())
    valentino = book.sections[-2]
    assert valentino.heading == "DESCRIPTION OF THE METHODS ADOPTED BY THE DUKE VALENTINO WHEN MURDERING A VICTIM AT SINIGAGLIA"
    assert "By Nicolo Machiavelli" in book.body_text[valentino.content_start:valentino.end_char]


@pytest.mark.parametrize("mutate", [
    lambda body: body.replace("CHAPTER I.\n", "CHAPTER II.\n", 1),
    lambda body: body.replace("CHAPTER XXVI.\n", "", 1),
    lambda body: body.replace("CHAPTER II.\n", "CHAPTER IV.\n", 1),
    lambda body: body.replace("SYNTHETIC CHAPTER 4 TITLE\n\n", "\n\n", 1),
    lambda body: body.replace("By Nicolo Machiavelli", "").replace("The final appendix closes the fixture.", ""),
])
def test_missing_duplicate_reordered_or_empty_sections_fail(tmp_path, mutate):
    body = mutate(fixture_body())
    raw = make_fixture_text(body)
    with pytest.raises(BookInputError):
        load_variant(tmp_path, raw)


def test_section_ranges_are_ordered_nonoverlapping_and_nonempty(tmp_path):
    book = load_variant(tmp_path, make_fixture_text())
    previous_end = 0
    for section in book.sections:
        assert 0 <= section.heading_start <= section.content_start < section.end_char <= len(book.body_text)
        assert previous_end <= section.heading_start
        previous_end = section.end_char
    assert book.sections[-1].end_char == len(book.body_text)


def test_duplicate_start_and_end_markers_are_rejected(tmp_path):
    from tests.book_fixture import END, START

    original = make_fixture_text()
    duplicate_start = original.replace("This editorial note includes Unicode", START + "\nThis editorial note includes Unicode", 1)
    path = write(tmp_path, duplicate_start)
    with pytest.raises(BookInputError, match="marker|digest|fingerprint"):
        load_book_corpus(path, manifest=fixture_manifest(duplicate_start))

    duplicate_end = original.replace(END, END + "\n" + END, 1)
    path = write(tmp_path, duplicate_end)
    with pytest.raises(BookInputError, match="marker"):
        load_book_corpus(path, manifest=fixture_manifest(duplicate_end))


def test_reversed_markers_are_rejected_after_injected_hashes(tmp_path):
    from dataclasses import replace
    from tests.book_fixture import END, START

    original = make_fixture_text()
    reordered = original.replace(START, "TEMP MARKER", 1).replace(END, START, 1).replace("TEMP MARKER", END, 1)
    canonical = reordered.replace("\r\n", "\n").replace("\r", "\n")
    empty_body_digest = hashlib.sha256(b"").hexdigest()
    manifest = replace(fixture_manifest(), source_sha256=hashlib.sha256(canonical.encode("utf-8")).hexdigest(), body_sha256=empty_body_digest)
    path = write(tmp_path, reordered)
    with pytest.raises(BookInputError, match="ordered|marker"):
        load_book_corpus(path, manifest=manifest)


def test_chapter_marker_reordering_is_rejected(tmp_path):
    body = fixture_body()
    body = body.replace("CHAPTER II.\n", "CHAPTER TEMP.\n", 1)
    body = body.replace("CHAPTER III.\n", "CHAPTER II.\n", 1)
    body = body.replace("CHAPTER TEMP.\n", "CHAPTER III.\n", 1)
    raw = make_fixture_text(body)
    with pytest.raises(BookInputError, match="Chapter markers"):
        load_variant(tmp_path, raw)
