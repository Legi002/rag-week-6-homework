# Tasks: Local Prince Book Extension

**Input**: spec.md, plan.md, research.md, data-model.md, contracts/, evaluation-cases.json and validation.md in this feature directory.
**Status**: Implementation in progress; actual results are recorded below.
**Tests**: Required by FR-011. Add observable-behavior tests before the corresponding new implementation. Preserve inherited checks.

## Rules for the implementation session

Read the constitution and every document listed above, plus quickstart.md and handoff.md. Work on feat/extended-rag-homework, based on completed homework 4c0e2b4. If documents conflict or inherited tests fail, stop and report. Do not broaden semantic scope, add a model, alter baseline scorers/defaults, use a demo question whitelist, or treat positive BM25 as answer confidence. Update result notes with actual checks, not assumed success. The full source remains outside Git.

## Phase 1: Setup

- [x] T001 Verify feature branch and completed-base ancestry, inspect working tree, and read governing documents in `.specify/memory/constitution.md` and `specs/001-prince-book-rag/`; stop on unexpected changes.
- [x] T002 Run the inherited 32-test preflight and baseline CLI evidence examples from `specs/001-prince-book-rag/quickstart.md`; record actual results in this `tasks.md` before writing application code.

## Phase 2: Foundation

- [x] T003 Add a small generated 35-section synthetic source and explicitly injected fixture manifest in `tests/book_fixture.py`; include metadata, marker structure, the XVIII footnote suffix, multiline headings and Unicode without bundling the real ebook.

## Phase 3: US1 - Verified local book (P1)

**Goal**: Load only the supported source and preserve the completed homework.
**Independent Test**: Production identity rejects synthetic/changed/other-book files; fixture loader accepts only its explicit manifest and parses the required structure.

- [x] T004 [US1] Add identity/input tests in `tests/test_book_corpus.py`: invalid UTF-8, absent/nonfile/unreadable path, marker/header/digest mismatch, BOM/CRLF equivalence and changed content with plausible metadata; use explicit fixture hashes for structural mutations.
- [x] T005 [US1] Add BookManifest, BookCorpus, SourceSection, BookInputError and `load_book_corpus` in `src/book_corpus.py`; enforce the production hashes and parsed identity from `data-model.md`, with no CLI override.
- [x] T006 [US1] Add parser tests in `tests/test_book_corpus.py` for exact ordered I-XXVI, XVIII.[1], uppercase-only multiline titles, contents/banner/license exclusion, all 35 sections, appendix bylines, and missing/duplicate/reordered/empty sections.
- [x] T007 [US1] Implement the section parser in `src/book_corpus.py`; enforce `0 <= heading_start <= content_start < end_char <= len(body_text)` and ordered nonoverlapping ranges; fail without guessed fallback sections.
- [x] T008 [US1] Run corpus/identity tests and the inherited suite, checking the scoped diff of `src/book_corpus.py` and `tests/test_book_corpus.py`; record results in this `tasks.md`.

## Phase 4: US2 - Ranked evidence and exact citations (P2)

**Goal**: Rank book windows independently from conservative source-sentence admission.
**Independent Test**: Controlled scores match an independent oracle; all admitted text is an exact source slice and citations reference only that text. Refusals can retain raw candidates.

- [x] T009 [US2] Add exact-window and sentence-span tests in `tests/test_book_retrieval.py`: Unicode, whitespace-adjusted offsets, unchanged raw step schedule, empty windows, no section crossings, configuration-sensitive IDs and invalid size/overlap.
- [x] T010 [US2] Add `build_book_chunks` in `src/book_retrieval.py` and `book_sentence_spans` in `src/book_corpus.py`; enforce `content_start <= start_char < end_char <= section.end_char` and `text == body_text[start_char:end_char]`; retain the inherited sentence-boundary rule without changing `src/chunking.py`.
- [x] T011 [US2] Add independent BM25 oracle, frequency/length, distinct-query-term, zero-token/empty index and stable-tie tests in `tests/test_book_retrieval.py`, using the controlled cat/dog example in `validation.md`.
- [x] T012 [US2] Implement frozen book-lexical-v1 tokens, BookIndex, BookRetrievalResult and all-positive retrieval in `src/book_retrieval.py`; use the exact positive-IDF formula, k1=1.5/b=0.75 and unrounded source tie breaks in plan.md.
- [x] T013 [US2] Add evidence-admission tests in `tests/test_book_rag.py`: terms split across sentences, unknown and numeric terms, negated/hypothetical queries, `0 < len(text) <= 2000`, actual counted list versus mention, causal/date guards, empty query and valid paraphrase false refusal.
- [x] T014 [US2] Implement book-evidence-v1 and `build_book_answer` in `src/book_rag.py`; full retained-term coverage must occur in one complete intersecting sentence; filter all positive candidates before top-k and never use stored case answers.
- [x] T015 [US2] Add citation tests in `tests/test_book_rag.py` for exact quoted slices, separately identified extended sentence evidence, deduplication, stable best origin, candidate below raw top-k, and refusal with candidates but no citations.
- [x] T016 [US2] Implement EvidenceExcerpt/BookAnswer records, full-digest identifiers, deterministic origin selection, source references and exact quote output in `src/book_rag.py`; refusals have zero accepted excerpts and zero answer citations.
- [x] T017 [US2] Run book retrieval/answer tests and inherited suite; inspect new-module changes in `src/book_retrieval.py` and `src/book_rag.py`, and record actual results in this `tasks.md`.

## Phase 5: US3 - Reproducible CLI and evidence (P3)

**Goal**: Exercise the book path without changing baseline commands and produce genuine homework evidence.
**Independent Test**: All legacy CLI tests pass; fixed case content and exact citations pass at both settings and both limits; evidence is copied from actual commands.

- [x] T018 [US3] Preserve and extend baseline compatibility checks in `tests/test_cli.py`, including default/training-rag output, --show-retrieval, refusal, inherited defaults and existing citation IDs.
- [x] T019 [US3] Add synthetic book CLI checks in `tests/test_cli.py` for explicit-profile/file conflicts, omitted-value sentinels, book defaults, bad inputs/parameters, exit 2 without traceback/partial answer, opt-in separated candidate/accepted displays and exit 0 refusals.
- [x] T020 [US3] Add `--corpus-file` dispatch and book rendering in `src/cli.py` per `contracts/cli-contract.md`; keep legacy dispatch unchanged and reuse one saved book ranking for answer and display.
- [x] T021 [US3] Add optional real-book checks in `tests/test_book_acceptance.py` loading `evaluation-cases.json` only in the test layer; require RAG_PRINCE_FILE's production hash, exact quote/citation slices, all required fragments and explicit skip when input is absent.
- [x] T022 [US3] Run the 48 case/configuration/top-k combinations from `tests/test_book_acceptance.py` against the supported source, including both weather spellings, and record actual output/results in this `tasks.md`; a skipped run leaves real-source readiness incomplete.
- [x] T023 [US3] Create `evidence-prince.md` from actual implemented CLI output with all five homework outcomes, 400/80 versus 800/120, k2/k3, all four positive cases, seven negatives, edition/policy parameters and the separately labelled known false refusal; preserve `evidence.md`.
- [x] T024 [US3] Append source acquisition, supported-edition limits, local quote/refusal limitations, Windows environment guidance and book commands to `README.md`; preserve the existing baseline guidance and submission evidence.

## Phase 6: Polish and cross-cutting validation

- [x] T025 Run the full inherited/new suite and the real-source gate from `specs/001-prince-book-rag/validation.md`; record exact test counts, skips and failures here without calling absent-source skips passes.
- [x] T026 Review the diff against 4c0e2b4 for `src/`, `tests/`, `evidence.md` and `.venv/`: legacy modules/evidence and tracked virtual environment must be preserved; only the planned new book path and scoped CLI/tests/docs changes belong to this extension.
- [x] T027 Measure the 800/120/k3 book command from `specs/001-prince-book-rag/quickstart.md` on the implementation machine; record machine/time in `evidence-prince.md`, investigate exceeding the five-second target before declaring readiness.
- [x] T028 Reconcile actual behavior against every contract and content oracle in `specs/001-prince-book-rag/`; verify source fingerprints, no committed ebook or temporary probes, and no unsupported confidence claims in CLI/README/evidence.
- [x] T029 Update this `specs/001-prince-book-rag/tasks.md` with actual result notes and completed boxes; leave unrun work unchecked and distinguish known false refusals from absent-answer successes.
- [x] T030 Commit the reviewed feature source, tests and actual evidence/docs on feat/extended-rag-homework with a concrete implementation/validation summary; do not change main or publish unrelated files.

## Dependencies and execution order

T001-T003 precede all story work. US1 supplies validated text/sections. US2 requires US1 and adds ranking before admission. US3 requires US2 and then creates actual evidence. Polish follows all stories. Within each behavior, tests precede implementation; result checks precede the next phase. Every numbered task is sequential unless a separate collaborator is explicitly authorized.

## Parallel opportunities

After T003, corpus input/section test cases can be drafted independently. After US1, chunk/ranking tests in test_book_retrieval.py and admission tests in test_book_rag.py can be drafted by separate authorized contributors. CLI test additions can be prepared while book modules are implemented after their contracts are fixed. No task is marked [P] because this handoff defaults to one implementation model and phases depend on verified predecessors.

## Implementation strategy

US1 is the first independently verified increment; US2 adds the useful query path; US3 completes the CLI/evidence deliverable. Do not stop after US1 and label the extension finished. The final gate includes actual source runs and all inherited tests. Total: 30 tasks; US1 5, US2 9, US3 7, setup/foundation/polish 9.

## Implementation results

- T001 (2026-10-14): branch `feat/extended-rag-homework`; completed baseline `4c0e2b4` is an ancestor; planning commit `df5028d` is present; initial worktree clean. Explicit Spec Kit feature selection resolved to `specs/001-prince-book-rag`. No applicable `AGENTS.md` was found in the repository or checked parents.
- T002 (2026-10-14): isolated Python 3.13.7 environment outside the repository; inherited preflight `32 passed`. The three documented baseline CLI examples returned exit 0; default query answered, training-rag citations answered with the inherited chunk citation, and World Cup query refused with no citations. The global Python 3.14 lacked pytest; the quickstart's temporary-environment setup resolved it.
- Source preparation: the external source has 308,019 bytes and raw SHA-256 `33496a305f7a4b933784fb5aec95f920fbc3d4687794817e4cc444aa6578d2e4`, matching the researched manifest. It remains outside the repository.
- T003-T008: added an offline synthetic 35-section source and identity/parser tests. The fixture includes Unicode, an XVIII footnote suffix, contents entries, multiline titles, bylines and outside license text. Production loading verified the real edition at 282,640 body characters and 35 sections. Corpus tests grew from 20 to 23 after the final structure review.
- T009-T017: added exact-window, sentence-span, independent BM25, admission and citation tests. The focused retrieval/answer run passed 23 tests; at that checkpoint the full suite had 75 passes.
- T018-T021: preserved baseline CLI coverage and added selection/default, rendering, invalid-input and synthetic book CLI checks. Added the optional real-source test matrix with 48 parameter combinations. The CLI-focused tests passed 10.
- T022: with `RAG_PRINCE_FILE` set to the manifest-matching edition, all 48 case/configuration/top-k acceptance tests passed. A separate run invoked the actual CLI 48 times and verified each expected answer or refusal.
- T023: generated `evidence-prince.md` from actual CLI output, including all fixed cases, representative quotations/refusals, inherited homework outcomes, source hashes and the known paraphrase false refusal. Original `evidence.md` remains untouched.
- T024: appended manual source acquisition, supported-edition, Windows setup, commands and quote-policy limitations to `README.md`.
- T025: final full suite with `RAG_PRINCE_FILE` set: 132 passed, 0 skipped, 0 failed. This includes all inherited tests and the 48 real-source acceptance combinations.
- T026: reviewed against `4c0e2b4`. Inherited `src/corpus.py`, `src/chunking.py`, `src/retrieval.py`, `src/rag.py`, `evidence.md`, and tracked `.venv/` are unchanged. `src/cli.py` is the only modified baseline source module; book behavior is isolated in three new modules.
- T027: timed the 800/120/k3 five-errors command at 0.376 seconds on Windows host `DURUT` with Python 3.13.7, below the five-second target.
- T028: reconciled identity, parser, offsets, BM25, admission, citations, CLI, errors and content oracles with both contracts and the plan. Verified raw/source/body fingerprints. The full ebook and temporary evidence generator remain outside Git. Results state the documented false refusal and limitations.
- T029: all completed task results are recorded. T030 remains pending until the reviewed commit exists.
- Final review update: the synthetic parser suite explicitly covers contents-list duplicates, outside-license exclusion, duplicate/reversed markers, and reordered chapters. The final full suite remains 132 passed with the real source configured.
- T030 (2026-10-14): committed reviewed extension changes on eat/extended-rag-homework as 5806b226faa685e6cb2288fdb9622005cf993e32; commit includes only the scoped source, tests, documentation, task results and actual evidence report.
