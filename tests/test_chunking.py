import pytest

from src.chunking import build_chunks, split_text_with_overlap
from src.corpus import Document


def test_split_text_with_overlap_returns_multiple_chunks() -> None:
    text = "abcdefghijklmnopqrstuvwxyz" * 4
    chunks = split_text_with_overlap(text, chunk_size=30, overlap=10)
    assert len(chunks) >= 3


def test_split_text_with_overlap_preserves_exact_character_overlap() -> None:
    chunks = split_text_with_overlap("abcdefghijklmnopqrstuvwxyz", chunk_size=10, overlap=4)
    assert chunks == ["abcdefghij", "ghijklmnop", "mnopqrstuv", "stuvwxyz"]
    assert chunks[0][-4:] == chunks[1][:4]


def test_split_text_with_overlap_respects_size_bound_and_skips_whitespace() -> None:
    chunks = split_text_with_overlap("  alpha   beta gamma delta  ", chunk_size=8, overlap=2)
    assert chunks
    assert all(len(chunk) <= 8 for chunk in chunks)
    assert split_text_with_overlap(" \n\t ", chunk_size=8, overlap=2) == []


@pytest.mark.parametrize(
    ("chunk_size", "overlap"),
    [(0, 0), (-1, 0), (10, -1), (10, 10), (10, 11)],
)
def test_split_text_with_overlap_rejects_invalid_parameters(chunk_size: int, overlap: int) -> None:
    with pytest.raises(ValueError):
        split_text_with_overlap("abc", chunk_size=chunk_size, overlap=overlap)


def test_build_chunks_retains_source_metadata_and_unique_ids() -> None:
    documents = [
        Document(doc_id="doc-a", title="Alpha", text="abcdefghijklmnop"),
        Document(doc_id="doc-b", title="Beta", text="qrstuvwxyz"),
    ]

    chunks = build_chunks(documents, chunk_size=8, overlap=2)

    assert len({chunk.chunk_id for chunk in chunks}) == len(chunks)
    assert all(chunk.doc_id in {"doc-a", "doc-b"} for chunk in chunks)
    assert all(chunk.title == ("Alpha" if chunk.doc_id == "doc-a" else "Beta") for chunk in chunks)
