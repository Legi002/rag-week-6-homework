from dataclasses import dataclass
import re
from typing import Optional, Tuple

from .book_corpus import BookCorpus, book_sentence_spans
from .rag import REFUSAL_MESSAGE
from .book_retrieval import (
    BOOK_TOKEN_POLICY_VERSION, K1, B, BookConfigurationError, BookIndex,
    BookRetrievalResult, book_tokens, retrieve_book_candidates,
)

ADMISSION_POLICY_VERSION = "book-evidence-v1"
POLICY_REFUSAL_EXPLANATION = "The local quote policy did not admit evidence; this does not prove the book lacks an answer."
RAW_WORD_RE = re.compile(r"[a-zA-Z0-9]+")
CARDINALS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}


@dataclass(frozen=True)
class EvidenceExcerpt:
    excerpt_id: str
    section_id: str
    heading: str
    kind: str
    start_char: int
    end_char: int
    text: str
    coverage: float
    origin_chunk_id: str
    origin_score: float
    admission_policy_version: str


@dataclass(frozen=True)
class BookAnswer:
    answer: str
    citations: Tuple[str, ...]
    refused: bool
    ranked_candidates: Tuple[BookRetrievalResult, ...]
    accepted_excerpts: Tuple[EvidenceExcerpt, ...]
    refusal_reason: Optional[str]
    source_title: str
    translator: str
    source_sha256: str
    body_sha256: str
    parser_version: str
    token_policy_version: str
    admission_policy_version: str
    chunk_size: int
    overlap: int
    top_k: int
    bm25_k1: float
    bm25_b: float


def _raw_words(text: str) -> list:
    return [word.lower() for word in RAW_WORD_RE.findall(text)]


def _count_requests(question: str) -> list:
    words = _raw_words(question)
    found = []
    for index, word in enumerate(words[:-1]):
        count = CARDINALS.get(word)
        if count is None and word.isdigit() and int(word) > 0:
            count = int(word)
        noun = words[index + 1]
        if count is not None and noun.endswith("s") and len(noun) > 1:
            found.append((count, noun))
    return found


def _has_counted_list(sentence: str, count: int, noun: str) -> bool:
    count_word = str(count)
    for word, number in CARDINALS.items():
        if number == count:
            count_word = "(?:%s|%d)" % (re.escape(word), count)
            break
    pattern = re.compile(r"\b" + count_word + r"(?:\s+[a-zA-Z][a-zA-Z-]*){0,2}\s+" + re.escape(noun) + r"\s*:", re.IGNORECASE)
    match = pattern.search(sentence)
    if not match:
        return False
    tail = sentence[match.end():]
    items = [item.strip() for item in re.split(r"[,;]", tail) if item.strip()]
    if len(items) != count:
        return False
    return all(len(book_tokens(item)) >= 2 for item in items)


def _refused(question: str, reason: str, candidates, book, index, top_k: int) -> BookAnswer:
    return BookAnswer(
        answer=REFUSAL_MESSAGE + "\n" + POLICY_REFUSAL_EXPLANATION,
        citations=(), refused=True, ranked_candidates=tuple(candidates), accepted_excerpts=(),
        refusal_reason=reason, source_title=book.title, translator=book.translator,
        source_sha256=book.source_sha256, body_sha256=book.body_sha256,
        parser_version=book.manifest.parser_version, token_policy_version=BOOK_TOKEN_POLICY_VERSION,
        admission_policy_version=ADMISSION_POLICY_VERSION,
        chunk_size=index.chunks[0].chunk_size if index.chunks else 800,
        overlap=index.chunks[0].overlap if index.chunks else 120, top_k=top_k, bm25_k1=index.k1, bm25_b=index.b,
    )


def build_book_answer(question: str, book: BookCorpus, index: BookIndex, top_k: int = 2) -> BookAnswer:
    if top_k <= 0:
        raise BookConfigurationError("top_k must be > 0")
    candidates = retrieve_book_candidates(question, index)
    terms = set(book_tokens(question))
    if not terms:
        return _refused(question, "EMPTY_QUERY", candidates, book, index, top_k)
    raw_words = _raw_words(question)
    if any(word in {"not", "no", "never", "without"} for word in raw_words):
        return _refused(question, "UNSUPPORTED_POLARITY", candidates, book, index, top_k)
    if any(word in {"if", "suppose", "hypothetical"} for word in raw_words):
        return _refused(question, "UNSUPPORTED_HYPOTHETICAL", candidates, book, index, top_k)

    count_requests = _count_requests(question)
    if len(count_requests) > 1:
        return _refused(question, "NO_ADMISSIBLE_SENTENCE", candidates, book, index, top_k)
    wants_why = re.match(r"^\s*why\b", question, re.IGNORECASE) is not None
    wants_when = re.match(r"^\s*when\b", question, re.IGNORECASE) is not None
    section_by_id = {section.section_id: section for section in book.sections}
    body_hash = book.body_sha256
    sentence_by_offsets = {}
    for span in book_sentence_spans(book):
        sentence_by_offsets[(body_hash, span.start_char, span.end_char)] = span

    origins = {}
    for candidate in candidates:
        chunk = candidate.chunk
        for key, span in sentence_by_offsets.items():
            if span.start_char >= chunk.end_char or span.end_char <= chunk.start_char:
                continue
            text = book.body_text[span.start_char:span.end_char]
            if len(text) > 2000:
                continue
            sentence_terms = set(book_tokens(text))
            if not terms.issubset(sentence_terms):
                continue
            lower = text.lower()
            if wants_why and not re.search(r"\b(?:because|for|since)\b", lower):
                continue
            if wants_when and not re.search(r"\b\d{4}\b", text):
                continue
            if count_requests and not _has_counted_list(text, count_requests[0][0], count_requests[0][1]):
                continue
            section = section_by_id[span.section_id]
            origin_key = (-candidate.score, chunk.start_char, chunk.end_char, chunk.chunk_id)
            existing = origins.get(key)
            if existing is None or origin_key < existing[0]:
                origins[key] = (origin_key, candidate, section, text)

    excerpts = []
    for (_excerpt_body_hash, start, end), (_origin_key, candidate, section, text) in origins.items():
        section_id = section.section_id
        excerpt_id = "pg1232-%s-p1-c%d-o%d-%s-s%d-%d" % (
            book.source_sha256, candidate.chunk.chunk_size, candidate.chunk.overlap, section_id, start, end
        )
        excerpts.append(EvidenceExcerpt(excerpt_id, section_id, section.heading, section.kind, start, end, text,
                                        1.0, candidate.chunk.chunk_id, candidate.score, ADMISSION_POLICY_VERSION))
    excerpts.sort(key=lambda excerpt: (-excerpt.origin_score, excerpt.start_char, excerpt.end_char, excerpt.excerpt_id))
    excerpts = excerpts[:top_k]
    if not excerpts:
        return _refused(question, "NO_ADMISSIBLE_SENTENCE", candidates, book, index, top_k)

    answer = "Matching source excerpts:\n" + "\n".join('"' + excerpt.text + '"' for excerpt in excerpts)
    first_chunk = index.chunks[0] if index.chunks else None
    return BookAnswer(
        answer=answer, citations=tuple(excerpt.excerpt_id for excerpt in excerpts), refused=False,
        ranked_candidates=tuple(candidates), accepted_excerpts=tuple(excerpts), refusal_reason=None,
        source_title=book.title, translator=book.translator, source_sha256=book.source_sha256,
        body_sha256=body_hash, parser_version=book.manifest.parser_version,
        token_policy_version=BOOK_TOKEN_POLICY_VERSION, admission_policy_version=ADMISSION_POLICY_VERSION,
        chunk_size=first_chunk.chunk_size if first_chunk else 800, overlap=first_chunk.overlap if first_chunk else 120,
        top_k=top_k, bm25_k1=index.k1, bm25_b=index.b,
    )
