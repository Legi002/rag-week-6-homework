import json
import os
from pathlib import Path
import re
import subprocess
import sys

import pytest

from src.book_corpus import load_book_corpus
from src.book_rag import build_book_answer
from src.book_retrieval import build_book_chunks, build_book_index


ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = ROOT / "specs" / "001-prince-book-rag" / "evaluation-cases.json"
CASES = json.loads(CASE_FILE.read_text(encoding="utf-8"))["cases"]
CONFIGURATIONS = [(400, 80), (800, 120)]
TOP_K_VALUES = [2, 3]
ACCEPTANCE_PARAMS = [(case, config, top_k) for case in CASES for config in CONFIGURATIONS for top_k in TOP_K_VALUES]


def normalize(text: str) -> str:
    return " ".join(text.split())


@pytest.fixture(scope="module")
def real_book():
    path = os.environ.get("RAG_PRINCE_FILE")
    if not path:
        pytest.skip("RAG_PRINCE_FILE is not set; real-book acceptance is unverified")
    book = load_book_corpus(path)
    expected = json.loads(CASE_FILE.read_text(encoding="utf-8"))["source_sha256"]
    assert book.source_sha256 == expected
    return book


@pytest.fixture(scope="module")
def real_indexes(real_book):
    return {(size, overlap): build_book_index(build_book_chunks(real_book, size, overlap)) for size, overlap in CONFIGURATIONS}


@pytest.mark.parametrize("case,configuration,top_k", ACCEPTANCE_PARAMS, ids=[
    "%s-%s-%s" % (case["case_id"], config[0], k) for case, config, k in ACCEPTANCE_PARAMS
])
def test_real_book_cases_at_both_configs_and_limits(real_book, real_indexes, case, configuration, top_k):
    result = build_book_answer(case["question"], real_book, real_indexes[configuration], top_k=top_k)
    assert result.refused is case["expected_refused"], case["case_id"]
    assert len(result.accepted_excerpts) <= top_k
    assert result.citations == tuple(excerpt.excerpt_id for excerpt in result.accepted_excerpts)
    for excerpt in result.accepted_excerpts:
        assert real_book.body_text[excerpt.start_char:excerpt.end_char] == excerpt.text
        assert excerpt.section_id in [section.section_id for section in real_book.sections]
        assert excerpt.origin_chunk_id in [candidate.chunk.chunk_id for candidate in result.ranked_candidates]
    if case["category"] == "supported":
        assert not result.refused
        assert all(excerpt.section_id in case["expected_sections"] for excerpt in result.accepted_excerpts)
        quoted = normalize(" ".join(excerpt.text for excerpt in result.accepted_excerpts)).lower()
        for fragment in case["required_fragments"]:
            assert normalize(fragment).lower() in quoted, (case["case_id"], fragment, quoted)
        if case["case_id"] == "supported-five":
            assert "destroyed the minor powers" in quoted
            assert "did not send colonies" in quoted
        if case["case_id"] == "supported-birth":
            assert "1469" in quoted and "1527" not in quoted
    elif case["category"] == "negative":
        assert result.refused
        assert not result.accepted_excerpts
        assert not result.citations
    else:
        assert case["category"] == "known_false_refusal"
        assert result.refused
        assert not result.citations


def test_real_cli_handles_five_thousand_digit_count_without_traceback(real_book):
    question = "9" * 5000 + " errors"
    completed = subprocess.run(
        [sys.executable, "-m", "src.cli", "--corpus-file", os.environ["RAG_PRINCE_FILE"], "--question", question],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert completed.returncode == 0
    assert "Refused: True" in completed.stdout
    assert "Citations: None" in completed.stdout
    assert "Traceback" not in completed.stdout
    assert "Traceback" not in completed.stderr
