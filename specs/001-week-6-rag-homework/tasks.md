# Tasks: Week 6 RAG Homework

**Input**: Design documents from `specs/001-week-6-rag-homework/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/cli.md`, and `quickstart.md`.

**Tests**: Included because `plan/plan_to_implement.md` explicitly requests test-first implementation.

## Phase 1: User Story 1 - Compare chunking configurations (P1)

**Goal**: Validate chunk bounds, overlap, metadata, and a controlled retrieval comparison.

**Independent Test**: Focused chunking tests pass and the same citation query can be run under both configurations.

- [X] T001 [P] [US1] Add exact-overlap, bounds, whitespace, invalid-argument, and metadata/ID checks in `tests/test_chunking.py`.
- [X] T002 [US1] Add a deterministic same-query retrieval comparison for both configurations in `tests/test_retrieval.py`.
- [X] T003 [US1] Verify `src/chunking.py` against the focused tests; existing behavior already satisfies the requirements.

## Phase 2: User Story 2 - Inspect ranked top-k evidence (P1)

**Goal**: Return meaningful, descending, capped evidence and reject invalid k.

**Independent Test**: Focused retrieval tests verify ranks, limits two and three, invalid k, empty input, and generic-word-only overlap.

- [X] T004 [P] [US2] Add score ordering, top-k limits, invalid k, empty query, common-word overlap, and weak-match filtering cases in `tests/test_retrieval.py`.
- [X] T005 [US2] Implement meaningful-query-token filtering and deterministic query coverage scoring in `src/retrieval.py`.

## Phase 3: User Story 3 - Cite grounded answers (P1)

**Goal**: Tie every answer citation to the returned supporting passages.

**Independent Test**: The training-rag citation question returns answer text whose citation IDs exactly match retrieved passage IDs.

- [X] T006 [P] [US3] Strengthen `tests/test_rag.py` with grounded text and exact citation-to-retrieval correspondence assertions.
- [X] T007 [US3] Verify `src/rag.py` against the supported-answer test; existing behavior already cites exactly the retrieved chunks.

## Phase 4: User Story 4 - Refuse unsupported questions (P1)

**Goal**: Refuse when evidence is absent or irrelevant and return no citations.

**Independent Test**: The World Cup question and an empty corpus produce clear refusals with empty citations.

- [X] T008 [P] [US4] Add World Cup common-word-overlap and empty-corpus refusal cases in `tests/test_rag.py`.
- [X] T009 [US4] Verify `src/rag.py` with the unsupported cases; retrieval now excludes irrelevant evidence and the existing refusal path returns no citations.

## Phase 5: User Story 5 - Reproduce homework evidence (P2)

**Goal**: Display ranked evidence through the CLI and record actual reproducible outputs.

**Independent Test**: Subprocess CLI checks verify stable evidence fields for supported/unsupported examples, and `evidence.md` records all five outcomes.

- [X] T010 [P] [US5] Add CLI subprocess tests for supported and unsupported questions, evidence fields, and top-k values two and three in `tests/test_cli.py`.
- [X] T011 [US5] Add the optional ranked evidence display in `src/cli.py`.
- [X] T012 [US5] Run the four commands from `specs/001-week-6-rag-homework/quickstart.md` and record their observed outputs and comparison in root `evidence.md`.
- [X] T013 [US5] Update `README.md` with the evidence display option and submission artifact location.

## Phase 6: Polish and validation

- [X] T014 Run focused tests and `./scripts/run_tests.sh`; resolve any failures.
- [X] T015 Review `specs/001-week-6-rag-homework/tasks.md`, `specs/001-week-6-rag-homework/spec.md`, `evidence.md`, and the working tree diff for consistency.
- [X] T016 [US3] Add a regression case for complete source sentences when a passage ends mid-sentence in `tests/test_rag.py`.
- [X] T017 [US3] Preserve bounded passage text and assemble grounded answers from complete overlapping source sentences in `src/chunking.py` and `src/rag.py`.
- [X] T018 [US3] Document complete-sentence answer behavior in `specs/001-week-6-rag-homework/data-model.md`, `specs/001-week-6-rag-homework/plan.md`, and `specs/001-week-6-rag-homework/contracts/cli.md`.

## Dependencies and execution order

- US1 chunking checks come first; no chunking code change is expected unless a check fails.
- US2 establishes meaningful evidence before US3 and US4 validate answer behavior.
- US5 depends on stable retrieval and answer behavior, then produces the final evidence artifact.
- Tasks marked `[P]` are test additions in distinct test files; implementation tasks run after their respective tests.

## Implementation strategy

Work sequentially through US1 to US5, preserving passing starter behavior. Implement the smallest changes indicated by failures. Finish by running the focused and full suite, the reproducible CLI scenarios, and reviewing the evidence artifact.
