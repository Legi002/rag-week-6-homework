# Pipeline Contract: Local Prince Book Extension

The three book modules are additions. Existing public baseline signatures and behavior stay intact.

## src/book_corpus.py

- Immutable BookManifest, BookCorpus and SourceSection records follow [data-model.md](../data-model.md).
- `load_book_corpus(path, *, manifest=PRINCE_MANIFEST) -> BookCorpus`: local strict UTF-8 read, canonicalization, marker/header/digest/section validation. Raises `BookInputError`, a ValueError subclass with an actionable message. Test fixture manifests are injected here; CLI has no manifest parameter.
- `book_sentence_spans(book) -> list[SentenceSpan]`: use the inherited boundary rule on canonical section content, yielding exact global body offsets. Parser errors never create guessed sections.
- PRINCE_MANIFEST carries the fingerprinted edition and ordered 35-section schema. No environment variable changes it.

## src/book_retrieval.py

- `book_tokens(text) -> list[str]`: frozen book-lexical-v1 policy; preserve repetitions. No baseline tokenizer mutation.
- `build_book_chunks(book, chunk_size=800, overlap=120) -> list[BookChunk]`: exact configured canonical slices; independent of legacy build_chunks defaults. Validate parameters before iterating.
- `build_book_index(chunks) -> BookIndex`: freeze counters, df/N/avgdl and k1=1.5/b=0.75 once. Empty index is valid.
- `retrieve_book_candidates(question, index) -> list[BookRetrievalResult]`: all positive finite BM25 results in stable order; no evidence or answer confidence decision and no early top-k truncation.

## src/book_rag.py

- `build_book_answer(question, book, index, top_k=2) -> BookAnswer`: validates k; calls retrieve_book_candidates once; admits only complete source sentences intersecting a result according to book-evidence-v1. Shares saved results with CLI.
- A single admitted sentence must contain every retained term, satisfy requested-count/causal/date checks, and be at most 2000 characters. Negated/hypothetical questions refuse. No query whitelist, stored factual answer, evaluation-case lookup or source-name alias table.
- Deduplicate sentence offsets, assign the best stable origin, sort and cap accepted excerpts by k. Keep full raw candidates available, separately capped for console display.
- Quotes are canonical source slices; citations refer to evidence excerpts, whose origin chunks and extended sentence locations are explicitly displayed. Do not pretend an extended sentence equals a smaller indexed window.

## src/cli.py dispatch

Add `--corpus-file` and use omitted-value sentinels for corpus/chunk selection. Built-in dispatch remains load_corpus -> build_chunks -> build_grounded_answer; inherited --show-retrieval path stays compatible. Book dispatch is load_book_corpus -> build_book_chunks -> build_book_index -> build_book_answer, followed by rendering the saved BookAnswer. Catch only book-input/configuration failures at that boundary, rendering stderr and exit 2; do not blanket-catch programmer errors.

Ranking, source identity, canonical offsets and admission are independently testable. No class conversions from BookRetrievalResult to baseline RetrievalResult are needed, and no baseline min_score is applied to a book result.
