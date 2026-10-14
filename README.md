# Week 6 RAG Homework Starter

This starter app helps students practice Week 6 concepts from the RAG lecture:

- corpus preparation
- chunking with overlap
- simple retrieval
- answer generation with citations
- refusal behavior when evidence is missing

## Learning goals

By the end of this homework, a student pair should be able to:

1. Explain how chunking strategy affects retrieval quality.
2. Implement a retrieval pipeline that returns top-k relevant chunks.
3. Return answers with explicit citations to source chunks.
4. Refuse unsupported questions instead of hallucinating.
5. Show evidence for one supported and one unsupported question.

## Project structure

```text
rag-week-6-homework-starter/
  src/
    corpus.py
    chunking.py
    retrieval.py
    rag.py
    cli.py
  tests/
    test_chunking.py
    test_retrieval.py
    test_rag.py
  docs/
    homework-checklist.md
  scripts/
    run_tests.sh
  requirements.txt
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run tests

```bash
./scripts/run_tests.sh
```

## Run demo CLI

```bash
python -m src.cli --question "What is retrieval augmented generation?"
python -m src.cli --question "Who won the world cup in 1958?"
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?"
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --show-retrieval
```

## Corpus profiles

- `default`: compact baseline corpus for Week 6 fundamentals.
- `training-rag`: profile mirroring examples with focus on citations, references, and LLM-as-a-judge framing.

## Homework tasks for students

1. **Outcome 1 (chunking impact):** tune chunking parameters in `src/chunking.py` and compare retrieval quality for the same query.
2. **Outcome 2 (top-k retrieval):** verify `src/retrieval.py` returns correctly ordered top-k relevant chunks.
3. **Outcome 3 (citations):** ensure `src/rag.py` returns grounded answers with explicit citations to chunk IDs.
4. **Outcome 4 (refusal):** ensure unsupported questions trigger refusal instead of hallucinated answers.
5. **Outcome 5 (evidence):** document one supported and one unsupported query with full retrieval and output evidence.

## Recommended evidence template (`evidence.md`)

Use this exact structure for easy review:

1. **Outcome 1: Chunking impact**
  - Config A:
  - Config B:
  - Retrieval difference summary:
2. **Outcome 2: Top-k retrieval**
  - Query:
  - Top-k output:
  - Why ranking is correct:
3. **Outcome 3: Citation quality**
  - Supported query:
  - Answer with citations:
  - Retrieved chunk IDs:
4. **Outcome 4: Refusal behavior**
  - Unsupported query:
  - Retrieved context:
  - Refusal output:
5. **Outcome 5: Final evidence pair**
  - Supported case command + output
  - Unsupported case command + output

Use `docs/homework-checklist.md` as submission guidance.
Use `--show-retrieval` to inspect ranked chunk IDs, scores, source titles, and text. Record the five homework outcomes and reproducible command output in the root `evidence.md` file.

## Optional local Prince corpus

The extension can search the English W. K. Marriott edition of *The Prince* (Project Gutenberg ebook 1232). Obtain the plain-text book manually from the [official ebook page](https://www.gutenberg.org/ebooks/1232) or [plain-text file](https://www.gutenberg.org/cache/epub/1232/pg1232.txt), then keep it outside this repository. The CLI works locally and does not download the book.

Only the researched edition updated July 24, 2026 is accepted. Its canonical source SHA-256 is `948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368`. A newer or edited copy needs a reviewed manifest and evaluation update.

On Windows PowerShell, point acceptance tests at your downloaded copy:

```powershell
$env:RAG_PRINCE_FILE = 'C:\path\to\pg1232.txt'
python -m src.cli --corpus-file $env:RAG_PRINCE_FILE --question "What were the five errors of Louis?" --chunk-size 800 --overlap 120 --top-k 3 --show-retrieval
python -m src.cli --corpus-file $env:RAG_PRINCE_FILE --question "Is it safer to be feared than loved?"
python -m src.cli --corpus-file $env:RAG_PRINCE_FILE --question "Why are mercenaries useless and dangerous?"
python -m src.cli --corpus-file $env:RAG_PRINCE_FILE --question "When was Nicolo Machiavelli born?"
python -m pytest -q
```

Book defaults are 800 characters, 120 overlap and top-k 2. Use 400/80 to compare the second planned configuration. `--show-retrieval` displays raw BM25 candidates separately from complete sentences admitted for quotation. BM25 scores rank passages; they are not answer confidence. Every citation points to an exact source sentence and its offsets.

The local quote policy favors traceable evidence over broad recall. It can refuse valid paraphrases such as `What five errors did Louis XII make in Italy?`, cannot combine evidence across sentences, and does not prove that a refused question has no answer in the book. Passing its lexical gates also does not guarantee arbitrary semantic correctness. See `specs/001-prince-book-rag/validation.md` and `evidence-prince.md` for the fixed cases and measured implementation results.
