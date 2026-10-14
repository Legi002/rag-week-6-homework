from pathlib import Path

import pytest

from src.book_corpus import load_book_corpus
from src.book_rag import build_book_answer
from src.book_retrieval import build_book_chunks, build_book_index
from tests.book_fixture import fixture_body, fixture_manifest, make_fixture_text


def make_book(tmp_path: Path, chapter_one: str):
    body = fixture_body().replace("Synthetic chapter 1 begins with Prince material.", chapter_one, 1)
    raw = make_fixture_text(body)
    path = tmp_path / "book.txt"
    path.write_text(raw, encoding="utf-8", newline="")
    book = load_book_corpus(path, manifest=fixture_manifest(raw))
    chunks = build_book_chunks(book, 400, 80)
    return book, build_book_index(chunks)


def answer(tmp_path, text, question, top_k=3):
    book, index = make_book(tmp_path, text)
    return build_book_answer(question, book, index, top_k=top_k)


def test_terms_split_across_sentences_never_combine(tmp_path):
    result = answer(tmp_path, "Alpha appears here. Beta appears later.", "alpha beta")
    assert result.refused
    assert result.refusal_reason == "NO_ADMISSIBLE_SENTENCE"


def test_unknown_and_numeric_terms_are_retained(tmp_path):
    unknown = answer(tmp_path, "Machiavelli was born in Florence in 1469.", "Machiavelli 1469 zzyzx")
    assert unknown.refused
    numeric = answer(tmp_path, "Machiavelli was born in Florence in 1469.", "Machiavelli 1469")
    assert not numeric.refused
    assert "1469" in numeric.answer


def test_negated_and_hypothetical_questions_refuse_with_distinct_reasons(tmp_path):
    text = "Machiavelli was born in Florence in 1469."
    negated = answer(tmp_path, text, "Was Machiavelli not born in Florence?")
    hypothetical = answer(tmp_path, text, "If Machiavelli was born in Florence, what happened?")
    assert negated.refused and negated.refusal_reason == "UNSUPPORTED_POLARITY"
    assert hypothetical.refused and hypothetical.refusal_reason == "UNSUPPORTED_HYPOTHETICAL"


def test_overlong_sentence_is_not_admitted(tmp_path):
    text = "quasar " + ("ordinary words " * 140) + " nebula."
    result = answer(tmp_path, text, "quasar nebula")
    assert result.refused
    assert result.refusal_reason == "NO_ADMISSIBLE_SENTENCE"


def test_counted_list_requires_a_real_n_item_colon_list(tmp_path):
    listed = "The five errors: weakened city, powerful neighbor, foreign force, absent prince, missing colonies."
    accepted = answer(tmp_path, listed, "What five errors?")
    assert not accepted.refused
    assert len(accepted.accepted_excerpts) == 1
    mention_only = answer(tmp_path, "The five errors were serious and costly.", "What five errors?")
    wrong_count = answer(tmp_path, "The five errors: weak city, strong neighbor.", "What five errors?")
    assert mention_only.refused and wrong_count.refused


def test_multiple_count_requests_refuse(tmp_path):
    text = "The five errors: weakened city, powerful neighbor, foreign force, absent prince, missing colonies."
    result = answer(tmp_path, text, "What five errors and three reasons?")
    assert result.refused
    assert result.refusal_reason == "NO_ADMISSIBLE_SENTENCE"


def test_why_and_when_require_same_sentence_cues(tmp_path):
    causeless = answer(tmp_path, "Raremerc are rareuseless and dangerous.", "Why are raremerc rareuseless?")
    causal = answer(tmp_path, "Raremerc are rareuseless because discipline matters.", "Why are raremerc rareuseless?")
    no_year = answer(tmp_path, "Rareperson was born in Florence.", "When was Rareperson born?")
    with_year = answer(tmp_path, "Rareperson was born in Florence in 1469.", "When was Rareperson born?")
    assert causeless.refused and causal.refused is False
    assert no_year.refused and with_year.refused is False


def test_empty_and_all_stop_word_queries_refuse(tmp_path):
    result = answer(tmp_path, "A prince rules. ", "the and what")
    assert result.refused
    assert result.refusal_reason == "EMPTY_QUERY"


def test_known_paraphrase_false_refusal_is_not_answered_by_aliasing(tmp_path):
    text = "Louis XII made five errors in Italy."
    result = answer(tmp_path, text, "What five errors did Louis XII make in Italy?")
    assert result.refused


def test_quotes_are_complete_source_sentences_under_2000_characters(tmp_path):
    sentence = "Alpha beta are supported in this complete sentence."
    book, index = make_book(tmp_path, sentence)
    result = build_book_answer("alpha beta", book, index, top_k=3)
    assert not result.refused
    excerpt = result.accepted_excerpts[0]
    assert 0 < len(excerpt.text) <= 2000
    assert book.body_text[excerpt.start_char:excerpt.end_char] == excerpt.text
    assert excerpt.text == sentence


def test_exact_quote_citation_and_extended_sentence_location(tmp_path):
    from src.book_rag import build_book_answer
    from src.book_retrieval import build_book_chunks, build_book_index

    sentence = "Zebra quasar " + ("ordinary source wording " * 5) + " nebula ends here."
    book, _ = make_book(tmp_path, sentence)
    chunks = build_book_chunks(book, 45, 10)
    index = build_book_index(chunks)
    result = build_book_answer("zebra nebula", book, index, top_k=3)
    assert not result.refused
    excerpt = result.accepted_excerpts[0]
    assert excerpt.text == sentence
    assert book.body_text[excerpt.start_char:excerpt.end_char] == excerpt.text
    assert result.citations == (excerpt.excerpt_id,)
    origin = next(chunk for chunk in index.chunks if chunk.chunk_id == excerpt.origin_chunk_id)
    assert origin.start_char > excerpt.start_char or origin.end_char < excerpt.end_char
    assert excerpt.excerpt_id.startswith("pg1232-" + book.source_sha256)


def test_overlapping_chunks_deduplicate_sentence_and_select_best_origin(tmp_path):
    from src.book_rag import build_book_answer
    from src.book_retrieval import build_book_chunks, build_book_index, retrieve_book_candidates

    sentence = "Rarealpha rarebeta " + ("shared wording " * 12) + " raregamma."
    book, _ = make_book(tmp_path, sentence)
    index = build_book_index(build_book_chunks(book, 55, 35))
    results = retrieve_book_candidates("rarealpha rarebeta raregamma", index)
    result = build_book_answer("rarealpha rarebeta raregamma", book, index, top_k=3)
    assert not result.refused
    matching = [e for e in result.accepted_excerpts if e.text == sentence]
    assert len(matching) == 1
    excerpt = matching[0]
    intersecting = [r for r in results if r.chunk.section_id == excerpt.section_id and r.chunk.start_char < excerpt.end_char and r.chunk.end_char > excerpt.start_char]
    assert excerpt.origin_score == max(r.score for r in intersecting)


def test_candidate_below_raw_top_k_can_supply_admitted_list(tmp_path):
    from src.book_rag import build_book_answer
    from src.book_retrieval import build_book_chunks, build_book_index, retrieve_book_candidates

    body = fixture_body().replace("Synthetic chapter 1 begins with Prince material.", "Five errors five errors five errors.", 1)
    body = body.replace("Synthetic chapter 2 begins with Prince material.", "The five errors: weakened city, powerful neighbor, foreign force, absent prince, missing colonies.", 1)
    raw = make_fixture_text(body)
    path = tmp_path / "book.txt"
    path.write_text(raw, encoding="utf-8", newline="")
    from src.book_corpus import load_book_corpus
    book = load_book_corpus(path, manifest=fixture_manifest(raw))
    index = build_book_index(build_book_chunks(book, 65, 5))
    ranked = retrieve_book_candidates("What five errors?", index)
    accepted = build_book_answer("What five errors?", book, index, top_k=1)
    assert ranked
    assert accepted.ranked_candidates[0].chunk.chunk_id == ranked[0].chunk.chunk_id
    assert not accepted.refused
    assert len(accepted.accepted_excerpts) == 1
    assert "weakened city" in accepted.accepted_excerpts[0].text


def test_refusal_can_keep_raw_candidates_without_citations(tmp_path):
    result = answer(tmp_path, "The weather in Florence was windy in 1469.", "What temperature was the weather in Florence in 1469?")
    assert result.refused
    assert result.ranked_candidates
    assert result.accepted_excerpts == ()
    assert result.citations == ()
