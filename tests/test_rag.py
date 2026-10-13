from src.chunking import build_chunks
from src.corpus import Document, load_corpus, load_default_corpus
from src.rag import build_grounded_answer
from src.retrieval import retrieve_top_k


def test_build_grounded_answer_returns_citations_for_supported_query() -> None:
    chunks = build_chunks(load_default_corpus(), chunk_size=120, overlap=20)
    result = build_grounded_answer("What is retrieval augmented generation?", chunks, top_k=2)
    assert result.refused is False
    assert len(result.citations) >= 1


def test_grounded_answer_uses_complete_source_sentence_when_chunk_ends_mid_sentence() -> None:
    documents = [Document(doc_id="doc", title="Sentences", text="First complete sentence. Second complete sentence.")]
    chunks = build_chunks(documents, chunk_size=17, overlap=0)

    result = build_grounded_answer("What is First?", chunks, top_k=1)

    assert result.refused is False
    assert result.answer == "Grounded response based on retrieved context:\n[doc-chunk-0] First complete sentence."


def test_supported_training_answer_cites_exact_retrieved_chunks_and_their_text() -> None:
    chunks = build_chunks(load_corpus("training-rag"), chunk_size=140, overlap=30)
    question = "Why are citations important in RAG?"
    retrieved = retrieve_top_k(question, chunks, k=2)

    result = build_grounded_answer(question, chunks, top_k=2)

    retrieved_ids = [item.chunk.chunk_id for item in retrieved]
    assert result.refused is False
    assert result.answer.strip()
    assert result.citations == retrieved_ids
    for item in retrieved:
        assert f"[{item.chunk.chunk_id}] {item.chunk.text}" in result.answer


def test_build_grounded_answer_refuses_unsupported_query() -> None:
    chunks = build_chunks(load_default_corpus(), chunk_size=120, overlap=20)
    result = build_grounded_answer("Who was emperor of Mars?", chunks, top_k=2)
    assert result.refused is True
    assert result.citations == []


def test_build_grounded_answer_refuses_world_cup_question_with_common_word_overlap() -> None:
    chunks = build_chunks(load_corpus("training-rag"), chunk_size=140, overlap=30)

    result = build_grounded_answer("Who won the World Cup in 1958?", chunks, top_k=2)

    assert result.refused is True
    assert "not have enough grounded evidence" in result.answer
    assert result.citations == []


def test_build_grounded_answer_refuses_when_there_are_no_chunks() -> None:
    result = build_grounded_answer("What is RAG?", [], top_k=2)
    assert result.refused is True
    assert result.citations == []
