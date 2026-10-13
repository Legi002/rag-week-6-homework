import re
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> str:
    completed = subprocess.run(
        [sys.executable, "-m", "src.cli", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


@pytest.mark.parametrize("top_k", [2, 3])
def test_cli_shows_ranked_evidence_and_matching_citations_for_supported_query(top_k: int) -> None:
    output = run_cli(
        "--corpus-profile", "training-rag",
        "--question", "Why are citations important in RAG?",
        "--top-k", str(top_k),
        "--show-retrieval",
    )

    assert "Corpus profile: training-rag" in output
    assert "Retrieved evidence:" in output
    assert "Rank: 1" in output
    assert re.search(r"Chunk ID: tr-doc-\d+-chunk-\d+", output)
    assert re.search(r"Score: [0-9]+\.[0-9]{4}", output)
    assert "Source:" in output
    assert "Text:" in output
    retrieved_ids = re.findall(r"Chunk ID: ([\w-]+)", output)
    citation_line = re.search(r"Citations: (.+)", output)
    assert retrieved_ids
    assert citation_line is not None
    citations = citation_line.group(1).split(", ")
    assert citations == retrieved_ids
    assert len(retrieved_ids) <= top_k
    assert "Refused: False" in output


def test_cli_shows_empty_evidence_and_refusal_for_unsupported_query() -> None:
    output = run_cli(
        "--corpus-profile", "training-rag",
        "--question", "Who won the World Cup in 1958?",
        "--top-k", "2",
        "--show-retrieval",
    )

    assert "Retrieved evidence:" in output
    assert "  None" in output
    assert "Refused: True" in output
    assert "Citations: None" in output


def test_cli_keeps_retrieval_evidence_hidden_by_default() -> None:
    output = run_cli(
        "--corpus-profile", "training-rag",
        "--question", "Why are citations important in RAG?",
    )
    assert "Retrieved evidence:" not in output
    assert "Citations:" in output
