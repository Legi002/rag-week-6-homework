# Quickstart: Future Application Validation

These book commands describe the planned implementation. They are not executable feature claims today. Read validation.md for the already observed planning experiments.

## Environment and source

Use a working Python environment with requirements.txt installed. The inherited repository contains a tracked POSIX .venv; do not overwrite it with a Windows environment. For example, on Windows:

```powershell
py -3.12 -m venv "$env:TEMP\rag-week6-env"
$ragPython = "$env:TEMP\rag-week6-env\Scripts\python.exe"
& $ragPython -m pip install -r requirements.txt
& $ragPython -m pytest -q
```

Choose another installed supported Python if 3.12 is unavailable. On macOS/Linux use your own environment outside the repository and its python executable. The normal pytest command must pass the inherited checks before implementation.

Download the English Marriott text from the [official ebook page](https://www.gutenberg.org/ebooks/1232) or its [direct HTTPS plain-text link](https://www.gutenberg.org/cache/epub/1232/pg1232.txt) manually. Save it outside the repository. It must be the fingerprinted edition in data-model.md; a newer source is not automatically accepted. The application does not download it.

```powershell
$princeFile = 'C:\path with spaces\pg1232.txt'
$env:RAG_PRINCE_FILE = $princeFile
```

Substitute a real local path. No doubled backslashes or unquoted path are needed in a PowerShell argument.

## Preserve completed homework

```powershell
& $ragPython -m src.cli --question "What is retrieval augmented generation?"
& $ragPython -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --show-retrieval
& $ragPython -m src.cli --corpus-profile training-rag --question "Who won the World Cup in 1958?" --show-retrieval
```

Expected: existing output remains compatible; citations example works; unrelated World Cup query refuses with no citations. Inherited evidence.md remains intact.

## Supported book quotations

```powershell
& $ragPython -m src.cli --corpus-file $princeFile --question "What were the five errors of Louis?" --chunk-size 800 --overlap 120 --top-k 3 --show-retrieval
& $ragPython -m src.cli --corpus-file $princeFile --question "Is it safer to be feared than loved?" --show-retrieval
& $ragPython -m src.cli --corpus-file $princeFile --question "Why are mercenaries useless and dangerous?" --show-retrieval
& $ragPython -m src.cli --corpus-file $princeFile --question "When was Nicolo Machiavelli born?" --show-retrieval
```

Expected content: all five errors in chapter III; qualified comparison in XVII; claim plus reasons in XII; 3rd May 1469 in introduction/editorial note. Check exact quotations and reference offsets, not just section names. Raw candidate chunks and accepted source sentences are displayed separately.

## Difficult refusals and known recall limit

```powershell
& $ragPython -m src.cli --corpus-file $princeFile --question "What was the weather in Florence on 3rd May 1469?" --show-retrieval
& $ragPython -m src.cli --corpus-file $princeFile --question "At what exact time was Nicolo Machiavelli born?" --show-retrieval
& $ragPython -m src.cli --corpus-file $princeFile --question "What five errors did Louis XII make in Italy?" --show-retrieval
```

All refuse without answer citations. The first two request unsupported details; the third is an answerable paraphrase deliberately rejected by literal matching. Do not label that last refusal as proof of absent source evidence.

## Compare settings and run complete acceptance

Repeat the supported five-error command at 400/80 and 800/120 and top-k 2 and 3. Then run:

```powershell
& $ragPython -m pytest -q
& $ragPython -m pytest -q tests/test_book_acceptance.py
```

The optional acceptance file must report real passes when RAG_PRINCE_FILE is set; a skip means real-book acceptance remains unverified. It covers all fixed cases at both settings and both k values. Record actual commands, outputs, hashes and timing in evidence-prince.md. Do not fabricate an improvement or reuse disposable-probe scores as application evidence.
