import math
from pathlib import Path

import pytest

from src.book_corpus import book_sentence_spans, load_book_corpus
from src.book_retrieval import BookChunk, BookIndex, build_book_chunks, build_book_index, book_tokens, retrieve_book_candidates
from tests.book_fixture import fixture_manifest, make_fixture_text


def synthetic_book(tmp_path: Path, body: str = None):
    raw = make_fixture_text() if body is None else make_fixture_text(body)
    path = tmp_path / "book.txt"
    path.write_text(raw, encoding="utf-8", newline="")
    return load_book_corpus(path, manifest=fixture_manifest(raw))


def test_book_chunks_are_exact_configured_slices_and_ids_include_configuration(tmp_path):
    book = synthetic_book(tmp_path)
    chunks = build_book_chunks(book, chunk_size=32, overlap=8)
    assert chunks
    assert all(chunk.text == book.body_text[chunk.start_char:chunk.end_char] for chunk in chunks)
    assert all(0 < chunk.end_char - chunk.start_char <= 32 for chunk in chunks)
    assert all(f"-c32-o8-" in chunk.chunk_id for chunk in chunks)
    other = build_book_chunks(book, chunk_size=40, overlap=8)
    assert chunks[0].chunk_id != other[0].chunk_id
    assert book.source_sha256 in chunks[0].chunk_id


def test_untrimmed_step_schedule_survives_boundary_whitespace(tmp_path):
    book = synthetic_book(tmp_path)
    section = next(section for section in book.sections if section.section_id == "chapter-01")
    chunks = [c for c in build_book_chunks(book, 40, 10) if c.section_id == "chapter-01"]
    assert len(chunks) >= 2
    first_raw_start = section.content_start
    second_raw_start = first_raw_start + 30
    while book.body_text[first_raw_start].isspace():
        first_raw_start += 1
    while book.body_text[second_raw_start].isspace():
        second_raw_start += 1
    assert chunks[0].start_char == first_raw_start
    assert chunks[1].start_char == second_raw_start


def test_chunks_never_cross_section_boundaries_and_invalid_parameters_fail(tmp_path):
    book = synthetic_book(tmp_path)
    chunks = build_book_chunks(book, 40, 10)
    sections = {section.section_id: section for section in book.sections}
    assert all(chunk.end_char <= sections[chunk.section_id].end_char for chunk in chunks)
    for size, overlap in [(0, 0), (10, -1), (10, 10)]:
        with pytest.raises(ValueError):
            build_book_chunks(book, size, overlap)


def test_sentence_spans_preserve_unicode_whitespace_and_section_offsets(tmp_path):
    book = synthetic_book(tmp_path)
    spans = book_sentence_spans(book)
    assert spans
    assert any("Æ" in book.body_text[s.start_char:s.end_char] for s in spans)
    for span in spans:
        section = next(s for s in book.sections if s.section_id == span.section_id)
        assert section.content_start <= span.start_char < span.end_char <= section.end_char
        assert book.body_text[span.start_char:span.end_char].strip()


def chunk(chunk_id, text, start):
    return BookChunk(chunk_id=chunk_id, doc_id="doc", section_id="s", heading="S", kind="chapter",
                     start_char=start, end_char=start + len(text), text=text, chunk_size=100, overlap=0,
                     parser_version="prince-sections-v1", normalizer_version="lf-v1")


def test_book_tokens_freeze_repetitions_numbers_unknown_words_and_negation():
    assert book_tokens("Cat cat 1469 not no never without") == ["cat", "cat", "1469", "not", "no", "never", "without"]
    assert book_tokens("the and is") == []


def test_bm25_matches_independent_cat_dog_oracle_and_distinct_query_terms():
    chunks = [chunk("a", "cat cat dog", 0), chunk("b", "cat fish", 10), chunk("c", "dog bird", 20)]
    index = build_book_index(chunks)
    results = retrieve_book_candidates("cat", index)
    idf = math.log(1.6)
    avgdl = 7 / 3
    expected_a = idf * (2 * 2.5) / (2 + 1.5 * (0.25 + 0.75 * (3 / avgdl)))
    expected_b = idf * (1 * 2.5) / (1 + 1.5 * (0.25 + 0.75 * (2 / avgdl)))
    assert [r.chunk.chunk_id for r in results] == ["a", "b"]
    assert results[0].score == pytest.approx(expected_a)
    assert results[1].score == pytest.approx(expected_b)
    assert results[0].score > results[1].score > 0
    assert [(r.chunk.chunk_id, r.score) for r in retrieve_book_candidates("cat cat", index)] == [(r.chunk.chunk_id, r.score) for r in results]


def test_frequency_length_effect_zero_tokens_and_empty_index():
    more = chunk("more", "cat cat dog", 0)
    less = chunk("less", "cat dog dog", 10)
    blank = chunk("blank", "!!!", 20)
    index = build_book_index([more, less, blank])
    assert index.n == 2
    assert index.average_document_length == 3
    scores = retrieve_book_candidates("cat", index)
    assert scores[0].chunk.chunk_id == "more"
    empty = build_book_index([])
    assert empty.n == 0
    assert retrieve_book_candidates("cat", empty) == []
    assert retrieve_book_candidates("the and", index) == []


def test_stable_ties_use_source_location_and_results_are_positive_finite():
    later = chunk("later", "wolf fox", 50)
    earlier = chunk("earlier", "wolf fox", 10)
    results = retrieve_book_candidates("wolf", build_book_index([later, earlier]))
    assert [r.chunk.chunk_id for r in results] == ["earlier", "later"]
    assert all(math.isfinite(r.score) and r.score > 0 for r in results)
    assert [r.rank for r in results] == [1, 2]


def test_absent_query_terms_do_not_create_candidates():
    index = build_book_index([chunk("a", "known term", 0)])
    assert retrieve_book_candidates("unknown 999", index) == []
