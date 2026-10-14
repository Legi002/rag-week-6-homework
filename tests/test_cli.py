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


def test_legacy_default_profile_and_parameter_defaults_remain_selected():
    from src.cli import parse_args
    args = parse_args(["--question", "What is RAG?"])
    assert args.corpus_profile is None
    assert args.corpus_file is None
    assert args.chunk_size is None
    assert args.overlap is None
    assert args.top_k is None


def test_explicit_profile_and_book_file_conflict_includes_default_profile():
    from src.cli import main
    with pytest.raises(SystemExit) as caught:
        main(["--corpus-profile", "default", "--corpus-file", "book.txt", "--question", "test"])
    assert caught.value.code == 2


def test_synthetic_book_cli_defaults_and_separated_opt_in_displays(tmp_path, monkeypatch, capsys):
    from src import cli
    from src.book_corpus import load_book_corpus as actual_loader
    from tests.book_fixture import fixture_manifest, make_fixture_text

    raw = make_fixture_text()
    path = tmp_path / "book.txt"
    path.write_text(raw, encoding="utf-8", newline="")
    synthetic_book = actual_loader(path, manifest=fixture_manifest(raw))
    monkeypatch.setattr(__import__("src.book_corpus", fromlist=["load_book_corpus"]), "load_book_corpus", lambda _path: synthetic_book)
    rc = cli.main(["--corpus-file", str(path), "--question", "Machiavelli born 1469"])
    output = capsys.readouterr().out
    assert rc == 0
    assert "Corpus profile: prince-book" in output
    assert "Chunk size: 800" in output
    assert "Overlap: 120" in output
    assert "Top-k: 2" in output
    assert "Source SHA-256: " + synthetic_book.source_sha256 in output
    assert "Raw ranked candidates:" not in output
    assert "Matching source excerpts:" in output
    assert "References:" in output

    rc = cli.main(["--corpus-file", str(path), "--question", "What was the weather?", "--show-retrieval"])
    output = capsys.readouterr().out
    assert rc == 0
    assert output.index("Raw ranked candidates:") < output.index("Accepted answer evidence:") < output.index("Answer:")
    assert "Refused: True" in output
    assert "Citations: None" in output
    assert "The local quote policy did not admit evidence" in output


def test_book_cli_bad_file_and_parameters_exit_two_without_partial_answer(tmp_path, capsys):
    from src import cli
    missing = tmp_path / "missing.txt"
    rc = cli.main(["--corpus-file", str(missing), "--question", "test"])
    captured = capsys.readouterr()
    assert rc == 2
    assert captured.out == ""
    assert captured.err.startswith("error:")
    assert "Traceback" not in captured.err

    rc = cli.main(["--corpus-file", str(missing), "--question", "test", "--chunk-size", "50"])
    captured = capsys.readouterr()
    assert rc == 2
    assert captured.out == ""
    assert "error:" in captured.err


def test_legacy_cli_output_and_python_defaults_are_unchanged(monkeypatch, capsys):
    from src import cli

    captured = {}
    original = cli.build_chunks
    def observe(documents, chunk_size=80, overlap=30):
        captured["chunk_size"] = chunk_size
        captured["overlap"] = overlap
        return original(documents, chunk_size=chunk_size, overlap=overlap)
    monkeypatch.setattr(cli, "build_chunks", observe)
    rc = cli.main(["--question", "What is retrieval augmented generation?"])
    output = capsys.readouterr().out
    assert rc == 0
    assert captured == {"chunk_size": 140, "overlap": 30}
    assert "Corpus profile: default" in output
    assert "Refused: False" in output
    assert "Citations: doc-1-chunk-0" in output


def test_explicit_legacy_parameters_and_retrieval_display_stay_compatible():
    output = run_cli(
        "--corpus-profile", "training-rag", "--question", "Why are citations important in RAG?",
        "--chunk-size", "140", "--overlap", "30", "--top-k", "2", "--show-retrieval",
    )
    assert "Retrieved evidence:" in output
    assert "Chunk ID: tr-doc-1-chunk-0" in output
    assert "Citations: tr-doc-1-chunk-0" in output
