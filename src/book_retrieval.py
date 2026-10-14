from collections import Counter
from dataclasses import dataclass
import math
import re
from types import MappingProxyType
from typing import Mapping, Tuple

from .book_corpus import BookCorpus

TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")
BOOK_TOKEN_POLICY_VERSION = "book-lexical-v1"
K1 = 1.5
B = 0.75

# Frozen copy of the inherited homework stop list, with polarity words retained for book queries.
BOOK_STOP_WORDS = frozenset({
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any",
    "are", "as", "at", "be", "because", "been", "before", "being", "below", "between",
    "both", "but", "by", "can", "could", "did", "do", "does", "doing", "down", "during",
    "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "her",
    "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into",
    "is", "it", "its", "itself", "just", "me", "more", "most", "my", "myself", "nor", "of",
    "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over",
    "own", "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "we", "were", "what", "when", "where",
    "which", "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself",
    "yourselves",
})


class BookConfigurationError(ValueError):
    """An invalid book query or chunking configuration."""


@dataclass(frozen=True)
class BookChunk:
    chunk_id: str
    doc_id: str
    section_id: str
    heading: str
    kind: str
    start_char: int
    end_char: int
    text: str
    chunk_size: int
    overlap: int
    parser_version: str
    normalizer_version: str


@dataclass(frozen=True)
class BookIndex:
    chunks: Tuple[BookChunk, ...]
    token_counts: Tuple[Mapping[str, int], ...]
    document_frequency: Mapping[str, int]
    document_count: int
    average_document_length: float
    token_policy_version: str = BOOK_TOKEN_POLICY_VERSION
    k1: float = K1
    b: float = B

    @property
    def n(self):
        return self.document_count

    @property
    def df(self):
        return self.document_frequency

    @property
    def avgdl(self):
        return self.average_document_length


@dataclass(frozen=True)
class BookRetrievalResult:
    chunk: BookChunk
    score: float
    rank: int


def book_tokens(text: str) -> list:
    return [token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in BOOK_STOP_WORDS]


def build_book_chunks(book: BookCorpus, chunk_size: int = 800, overlap: int = 120) -> list:
    if chunk_size <= 0:
        raise BookConfigurationError("chunk_size must be > 0")
    if overlap < 0:
        raise BookConfigurationError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise BookConfigurationError("overlap must be smaller than chunk_size")
    step = chunk_size - overlap
    chunks = []
    for section in book.sections:
        raw_start = section.content_start
        while raw_start < section.end_char:
            raw_end = min(raw_start + chunk_size, section.end_char)
            start, end = raw_start, raw_end
            while start < end and book.body_text[start].isspace():
                start += 1
            while end > start and book.body_text[end - 1].isspace():
                end -= 1
            if start < end:
                chunk_id = "pg1232-%s-p1-c%d-o%d-%s-w%d-%d" % (book.source_sha256, chunk_size, overlap, section.section_id, start, end)
                chunks.append(BookChunk(chunk_id, book.doc_id, section.section_id, section.heading, section.kind,
                                        start, end, book.body_text[start:end], chunk_size, overlap,
                                        book.manifest.parser_version, book.manifest.normalizer_version))
            if raw_end == section.end_char:
                break
            raw_start += step
    return chunks


def build_book_index(chunks: list) -> BookIndex:
    indexed_chunks = []
    token_counts = []
    document_frequency = Counter()
    lengths = []
    for chunk in chunks:
        counts = Counter(book_tokens(chunk.text))
        if not counts:
            continue
        indexed_chunks.append(chunk)
        token_counts.append(MappingProxyType(dict(counts)))
        document_frequency.update(counts.keys())
        lengths.append(sum(counts.values()))
    n = len(indexed_chunks)
    average = sum(lengths) / n if n else 0.0
    return BookIndex(tuple(indexed_chunks), tuple(token_counts), MappingProxyType(dict(document_frequency)), n, average)


def retrieve_book_candidates(question: str, index: BookIndex) -> list:
    terms = set(book_tokens(question))
    if not terms or index.document_count == 0 or index.average_document_length == 0:
        return []
    scored = []
    for chunk, counts in zip(index.chunks, index.token_counts):
        score = 0.0
        dl = sum(counts.values())
        normalization = index.k1 * (1.0 - index.b + index.b * dl / index.average_document_length)
        for term in sorted(terms):
            tf = counts.get(term, 0)
            df = index.document_frequency.get(term, 0)
            if tf <= 0 or df <= 0:
                continue
            idf = math.log1p((index.document_count - df + 0.5) / (df + 0.5))
            score += idf * tf * (index.k1 + 1.0) / (tf + normalization)
        if score > 0 and math.isfinite(score):
            scored.append((chunk, score))
    scored.sort(key=lambda item: (-item[1], item[0].start_char, item[0].end_char, item[0].chunk_id))
    return [BookRetrievalResult(chunk, score, rank) for rank, (chunk, score) in enumerate(scored, start=1)]
