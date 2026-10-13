import pytest

from src.chunking import Chunk, build_chunks
from src.corpus import load_corpus
from src.retrieval import retrieve_top_k


def test_retrieve_top_k_orders_by_score_desc() -> None:
    chunks = [
        Chunk(chunk_id="a", doc_id="1", title="A", text="rag citations trust"),
        Chunk(chunk_id="b", doc_id="1", title="B", text="rag citations evidence"),
        Chunk(chunk_id="c", doc_id="1", title="C", text="rag citations"),
        Chunk(chunk_id="d", doc_id="1", title="D", text="weather forecast rain tomorrow"),
    ]

    results = retrieve_top_k("rag citations trust", chunks, k=3)

    assert [item.chunk.chunk_id for item in results] == ["a", "b", "c"]
    assert [item.score for item in results] == sorted((item.score for item in results), reverse=True)


@pytest.mark.parametrize("k", [2, 3])
def test_retrieve_top_k_caps_results_at_requested_limit(k: int) -> None:
    chunks = [
        Chunk(chunk_id=str(i), doc_id="1", title="Source", text=f"rag citations evidence {i}")
        for i in range(5)
    ]

    assert len(retrieve_top_k("rag citations", chunks, k=k)) == k


@pytest.mark.parametrize("k", [0, -1])
def test_retrieve_top_k_rejects_nonpositive_k(k: int) -> None:
    with pytest.raises(ValueError, match="k must be > 0"):
        retrieve_top_k("rag", [], k=k)


def test_retrieve_top_k_returns_empty_for_unrelated_query() -> None:
    chunks = [
        Chunk(chunk_id="a", doc_id="1", title="A", text="vector database retrieval"),
    ]
    results = retrieve_top_k("basketball playoffs", chunks, k=2)
    assert results == []


def test_retrieve_top_k_ignores_common_words_without_meaningful_overlap() -> None:
    chunks = [
        Chunk(chunk_id="generic", doc_id="1", title="Generic", text="The guide is in the system."),
    ]

    assert retrieve_top_k("the in is", chunks, k=2) == []
    assert retrieve_top_k("Who won the World Cup in 1958?", chunks, k=2) == []


def test_retrieve_top_k_filters_passages_with_only_one_of_several_meaningful_terms() -> None:
    chunks = [
        Chunk(chunk_id="supported", doc_id="1", title="Supported", text="RAG citations improve trust"),
        Chunk(chunk_id="weak", doc_id="2", title="Weak", text="RAG practice can reduce hallucinations"),
    ]

    results = retrieve_top_k("Why are citations important in RAG?", chunks, k=3)

    assert [item.chunk.chunk_id for item in results] == ["supported"]


def test_retrieve_top_k_returns_empty_for_empty_question() -> None:
    chunks = [Chunk(chunk_id="a", doc_id="1", title="A", text="rag citations evidence")]
    assert retrieve_top_k("  ", chunks, k=2) == []


def test_chunking_comparison_is_deterministic_for_same_query_and_corpus() -> None:
    documents = load_corpus("training-rag")
    question = "Why are citations important in RAG?"

    standard_chunks = build_chunks(documents, chunk_size=140, overlap=30)
    candidate_chunks = build_chunks(documents, chunk_size=80, overlap=20)
    standard = retrieve_top_k(question, standard_chunks, k=2)
    candidate = retrieve_top_k(question, candidate_chunks, k=2)
    standard_again = retrieve_top_k(question, build_chunks(documents, 140, 30), k=2)

    assert standard
    assert candidate
    assert [(item.chunk.chunk_id, item.score) for item in standard] == [
        (item.chunk.chunk_id, item.score) for item in standard_again
    ]
    assert [item.chunk.text for item in standard] != [item.chunk.text for item in candidate]
