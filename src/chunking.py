from dataclasses import dataclass
import re
from typing import Optional

from .corpus import Document


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    text: str
    answer_text: Optional[str] = None


SENTENCE_END_RE = re.compile(r"[.!?](?=\s|$)")


def _sentence_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0

    for match in SENTENCE_END_RE.finditer(text):
        end = match.end()
        sentence_start = start
        while sentence_start < end and text[sentence_start].isspace():
            sentence_start += 1
        if sentence_start < end:
            spans.append((sentence_start, end))
        start = end

    tail_start = start
    while tail_start < len(text) and text[tail_start].isspace():
        tail_start += 1
    if tail_start < len(text):
        spans.append((tail_start, len(text)))

    return spans


def _iter_chunk_spans(text: str, chunk_size: int, overlap: int):
    step = chunk_size - overlap
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            yield start, end, chunk
        if end == len(text):
            break
        start += step


def split_text_with_overlap(text: str, chunk_size: int = 140, overlap: int = 30) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    return [chunk for _, _, chunk in _iter_chunk_spans(cleaned, chunk_size, overlap)]


def build_chunks(documents: list[Document], chunk_size: int = 80, overlap: int = 30) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        cleaned = " ".join(doc.text.split())
        sentence_spans = _sentence_spans(cleaned)
        for i, (start, end, part) in enumerate(_iter_chunk_spans(cleaned, chunk_size, overlap)):
            answer_sentences = [
                cleaned[sentence_start:sentence_end]
                for sentence_start, sentence_end in sentence_spans
                if sentence_start < end and sentence_end > start
            ]
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.doc_id}-chunk-{i}",
                    doc_id=doc.doc_id,
                    title=doc.title,
                    text=part,
                    answer_text=" ".join(answer_sentences) or part,
                )
            )
    return chunks
