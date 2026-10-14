# Implementation Plan: Local Prince Book Extension

**Branch**: `feat/extended-rag-homework` | **Date**: 2026-10-14 | **Spec**: [spec.md](spec.md)
**Input**: `specs/001-prince-book-rag/spec.md`
**Status**: Design validated with disposable experiments; application implementation has not started.

## Summary

Base the extension on completed homework commit `4c0e2b442bbcaeef1ffe7e1145400f310542112e` (`origin/001-rag-internal-feature`). Preserve its query-coverage scorer, public functions, default settings, `--show-retrieval`, complete-sentence answers and 32 inherited tests. Add a separate book pipeline for the verified July 24, 2026 Gutenberg edition. Rank character chunks with precisely defined BM25; admit exact source sentences with conservative lexical and evidence-shape gates. Keep candidate retrieval separate from answer admission. No model, hosted service, production code or fabricated implementation evidence belongs in this planning session.

## Technical Context

- **Language/Version**: Python 3.9+; existing builtin generic annotations are compatible. Test environment must support pinned pytest 8.3.3.
- **Dependencies**: Standard library at runtime; existing pytest requirement for development. Add no runtime dependency.
- **Storage**: Local user-supplied UTF-8 source; transient in-memory sections, chunks, statistics and sentence spans. No persisted index.
- **Testing**: Preserve inherited 32 checks; add focused unit/integration/CLI tests and an optional real-book acceptance run.
- **Platform/Type**: Existing Windows/macOS/Linux Python CLI.
- **Performance**: Query the researched 308,019-byte book within five seconds on the implementation machine at 800/120 and top-k 3; record machine and elapsed time, do not claim measured app performance now.
- **Scope**: One fingerprinted edition, 35 sections, 26 chapters; full source is never a committed fixture.

## Constitution Check

Design review passes: quotes cite exact source spans; local operation is self-contained; book-specific behavior is isolated; provenance and reproducibility are explicit; the completed homework remains the baseline. These are design checks, not assertions that the future implementation passes. The implementation must prove them through [validation.md](validation.md).

## Project Structure

```text
src/corpus.py              existing built-in corpus; unchanged
src/chunking.py            existing baseline chunking; unchanged
src/retrieval.py           existing baseline coverage scorer; unchanged
src/rag.py                 existing baseline answer path; unchanged
src/book_corpus.py         new edition validation, section parsing and book records
src/book_retrieval.py      new canonical windows, BM25 index and book query tokens
src/book_rag.py            new sentence admission, exact excerpts and book result
src/cli.py                 add local-file dispatch; preserve built-in output
tests/test_book_corpus.py
tests/test_book_retrieval.py
tests/test_book_rag.py
tests/test_cli.py          add book-path contract checks, retain inherited checks
tests/book_fixture.py      small synthetic source and injected test manifest
tests/test_book_acceptance.py optional real-source acceptance, no downloaded book fixture
evidence.md               preserve completed baseline evidence byte-for-byte
evidence-prince.md         produced from actual implementation output later
specs/001-prince-book-rag/ this plan, research, model, contracts, validation, tasks, handoff
```

**Structure Decision**: Use separate book modules rather than changing baseline data classes or scorer behavior. This prevents applying BM25 thresholds or source normalization to the built-in exercise. Source interface details are in [contracts/pipeline.md](contracts/pipeline.md).

## Phase 0: Research decisions

See [research.md](research.md) and [validation.md](validation.md). The actual source was inspected, fingerprinted and probed at 400/80 and 800/120. Research-agent findings were reconciled: single-sentence admission excludes unrelated birth references that broader windows admitted. Four canonical positives and seven negatives passed the design probe; a legitimate paraphrase is deliberately recorded as a false refusal.

## Phase 1: Resolved design

### 1. Source identity and canonical text

The production manifest accepts canonical full-source SHA-256 `948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368`. Decode strict UTF-8, remove at most one leading BOM, convert CRLF and CR to LF, and make no other changes. Hash the UTF-8 encoding of that full canonical source. Separately retain the raw byte hash.

Validate the header's ebook number 1232, title The Prince, Machiavelli author spelling, W. K. Marriott translator, English language, release date 2006-02-11 and update date 2026-07-24. The digest is authoritative; metadata alone cannot authenticate content. A changed edition fails with an actionable unsupported-edition error and requires a deliberate manifest/evaluation update. No CLI hash override or automatic fallback.

Require exactly one standalone START marker and one END marker naming THE PRINCE, with START before END. `body_text` is the exact substring immediately after the START line's newline and immediately before the END line. Do not strip it. Its researched digest is `347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1`, length 282,640 Unicode characters. Offsets always refer to this text, never to raw bytes or whitespace-collapsed display text.

For automated fixtures, inject a `BookManifest` carrying the fixture's own hash and expected source structure through the Python loader API; the CLI always uses the production manifest. Changing a test fixture requires updating only its explicit test manifest, not production identity.

### 2. Source sections

Chapter marker regex, applied with MULTILINE to canonical body text: `^CHAPTER ([IVXLCDM]+)\.(?:\[\d+\])?$`. Require exactly I through XXVI, once each in order. This excludes same-line contents entries and admits XVIII's footnote suffix. Immediately following a chapter marker, collect contiguous nonblank `line.isupper()` title lines; stop at the first blank or mixed-case narrative line. At least one title line is required. Join title lines only for display, preserving canonical text. XII and XIV need not equal their contents-list titles.

Index exactly 35 ordered sections: the editorial biographical note before INTRODUCTION; the six unindented front headings INTRODUCTION, YOUTH, OFFICE, LITERATURE AND DEATH, THE MAN AND HIS WORKS, DEDICATION; 26 chapters; and the Duke Valentino and Castruccio appendices. Exact full front-heading labels and appendix anchors are recorded in [data-model.md](data-model.md). Collect the first appendix's three uppercase heading lines. Byline text after the blank separator is content, not part of its title.

Exclude the book title/contents before the editorial note, the standalone THE PRINCE banner after DEDICATION, and material outside the Gutenberg delimiters. Retain footnotes and editorial passages, visibly labelled by section kind. A section stores heading start, narrative content start and end before the next source heading; DEDICATION ends before the excluded banner. Unexpected, missing, duplicate, reordered or empty section structures fail clearly; there is no guessed-section fallback.

### 3. Character windows and exact sentence spans

Book defaults are 800 characters/120 overlap/top-k 2. Built-in CLI defaults remain 140/30/2 and `build_chunks()` retains its inherited Python default of 80/30. Explicit book settings accept positive chunk size and `0 <= overlap < chunk_size`; top-k must be positive. Advance untrimmed window starts by `chunk_size-overlap`, and stop when the untrimmed end reaches the section end. Trim only boundary whitespace by adjusting stored offsets; never advance the next window from a trimmed start. Skip empty windows and zero-retained-token windows from BM25 statistics.

Windows begin at each section's content start and cannot cross its end. Every chunk satisfies `text == body_text[start_char:end_char]`. Sentence spans use the inherited sentence-boundary rule `[.!?](?=\s|$)` on the untouched section content, with leading whitespace skipped and an unterminated tail retained. Offsets are then shifted into the canonical body. This deliberately simple rule is not general prose understanding; abbreviations and closing quotes may reduce recall. Do not silently replace it without updating parser/policy versions and acceptance results.

The answer is a complete sentence intersecting a positively ranked chunk, not that chunk's truncated text. It may extend beyond a character window but must remain within the same section. The distinct `EvidenceExcerpt` and exact citation offsets make that extension visible. See the data model for deterministic chunk/excerpt IDs containing edition, parser version and chunk configuration.

### 4. BM25 ranking, fixed precisely

Book token policy `book-lexical-v1`: apply the existing ASCII regex `[a-zA-Z0-9]+`, lowercase, remove the inherited STOP_WORDS except retain `not`, `no`, `never`, `without`. Keep numbers and unknown query terms. No stemming, synonyms, entity aliases, ordinal normalization or silent dropping of absent terms. This is a separate tokenizer; do not edit the baseline tokenizer or stop list. Snapshot the inherited stop list into the new book policy so later baseline changes cannot silently change book evidence.

Use `k1=1.5`, `b=0.75`, natural logarithm, retained-token lengths and actual token frequencies. N is the number of nonempty book chunks; df counts chunks containing a term; overlapping chunks are separate documents. Query terms are distinct, while document frequency counts retain repetitions.

```text
idf(t) = ln(1 + (N - df(t) + 0.5) / (df(t) + 0.5))
score(q,d) = sum_t_in_distinct_query idf(t) * tf(t,d) * (k1+1)
             / (tf(t,d) + k1 * (1-b + b*dl(d)/avgdl))
```

Terms absent from a chunk contribute zero. N=0, avgdl=0 or an empty query gives no ranked results, not division by zero. Keep finite positive scores and sort by `(-score, start_char, end_char, chunk_id)` before any display rounding. Never use 0.01, 0.02 or 0.5 as BM25 confidence cutoffs. Scores change with chunk settings and are not comparable confidence probabilities.

### 5. Conservative evidence admission, separate from ranking

Policy `book-evidence-v1`, applied before selecting the answer top-k:

1. Build the distinct retained query-term set. Empty/all-stop-word questions refuse. Preserve unknown terms even if none occur in the index.
2. Inspect raw query words before stop-word removal. Negated questions containing `not/no/never/without`, or counterfactual cues `if/suppose/hypothetical`, refuse rather than attempt polarity or hypothetical reasoning. This deliberately causes some valid refusals.
3. Visit all positive BM25 candidates, not just the first k. Inspect complete sentences intersecting each candidate. A sentence must be at most 2,000 canonical characters and contain every retained query term: coverage exactly 1.0. Never pool terms across sentences, a whole chapter, or multiple chunks.
4. If the query requests a counted list, detect one cardinal word one through ten or a positive integer immediately followed by an English plural noun ending in s. Multiple count requests refuse. Require the same sentence to contain the corresponding count and noun (at most two intervening adjective words), followed by a colon and a real list. Split the colon tail on commas/semicolons, requiring exactly n nonempty items, each with at least two retained tokens. A mere mention of n errors fails. Unsupported list grammars refuse; do not insert hard-coded book answers or question whitelists.
5. A question beginning with `why` additionally requires a causal cue `because/for/since` in that same sentence. A question beginning with `when` requires a four-digit year in the same sentence. These are bounded lexical guards, not claims of complete semantic reasoning.
6. Deduplicate eligible sentences by exact `(body_sha256,start_char,end_char)`. Each excerpt uses the highest scoring intersecting candidate as its origin; break equal-score origin ties with the same source ordering. Sort excerpts by `(-origin_score,start_char,end_char,excerpt_id)` and return at most k.
7. Quote the exact source slice, with an excerpt citation and origin-chunk metadata. If no sentence passes, use the existing refusal wording and no answer citations. Include the book-policy explanation: failure to admit evidence does not prove the source lacks an answer.

Raw candidates remain inspectable under `--show-retrieval`, even for refusal. Label them separately from accepted excerpts; candidate IDs must never leak into the answer's citation list. A positive answer heading is `Matching source excerpts:` rather than a claim that arbitrary questions have been semantically solved.

Limitations are deliberate: literal inflection/regnal numerals can cause false refusal; one-sentence admission omits cross-sentence explanations; list punctuation can defeat counting; positive admission still does not prove arbitrary semantic answerability. General reasoning, synonym expansion and model-based verification are deferred. The selected local mode guarantees exact quotation and the specified gates, not universal answer correctness.

### 6. Integration and validation

Keep legacy `load_corpus`, `build_chunks`, `retrieve_top_k`, `build_grounded_answer`, their signatures and built-in output unchanged. CLI parses corpus selection and chunk settings with `None` sentinels, then dispatches either the inherited path (140/30 defaults) or the new book path (800/120 defaults). Resolve explicit profile/file conflicts without treating an implicit default as explicit selection. Do not call baseline rag.py with BM25 scores. Book query executes ranking once and shares its results between answer and retrieval output.

Use [contracts/cli-contract.md](contracts/cli-contract.md) for exit codes/output and [contracts/pipeline.md](contracts/pipeline.md) for functions. Run synthetic fixture tests without internet. Optional real-source tests use `RAG_PRINCE_FILE` and the pinned manifest; absent input skips those tests explicitly, never reports a real-book pass. Use [evaluation-cases.json](evaluation-cases.json) and content oracles in [validation.md](validation.md).

## Implementation Sequence

Follow [tasks.md](tasks.md) in order: baseline preflight; identity/parser tests then loader; offset/chunk and BM25 tests then index; admission/citation tests then book answers; CLI compatibility tests then dispatch; real-book cases at both configurations; actual evidence report and final full suite. Write tests before the corresponding new behavior. If inherited preflight fails, stop; do not hide baseline failures inside extension changes.

## Complexity Tracking

No unjustified constitution violation. Three book-specific modules isolate score scales and provenance. Full edition pinning trades easy import of newer editions for reproducibility; strict quote admission trades recall for transparency. Revisit these decisions only through a new evaluated feature, not silent implementation-time broadening.
