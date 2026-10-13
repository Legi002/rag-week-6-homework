# Implementation Plan: Week 6 RAG Homework

**Branch**: `001-week-6-rag-homework` | **Date**: 2026-10-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-week-6-rag-homework/spec.md`

## Summary

Complete the five homework outcomes using the existing deterministic local RAG pipeline. Add focused coverage for chunk boundaries, ranked retrieval, complete-sentence citations, refusal, and CLI journeys; adjust lexical relevance so common words cannot support an unrelated answer; add an optional CLI evidence display; and record reproducible outputs in root `evidence.md`.

## Technical Context

**Language/Version**: Python 3.12 (compatible with the existing Python 3 project)

**Primary Dependencies**: Python standard library; pytest for the existing test suite

**Storage**: Local in-memory corpus profiles in `src/corpus.py`

**Testing**: pytest via `./scripts/run_tests.sh`; focused files under `tests/`

**Target Platform**: Local command line on Python-supported platforms

**Project Type**: Python library and command line demo

**Performance Goals**: Process the supplied small corpus synchronously without external calls.

**Constraints**: Deterministic local behavior; preserve existing public function and CLI defaults; no external model or service.

**Scale/Scope**: Four short corpus documents, character-based chunks, and homework-sized queries.

## Constitution Check

The constitution contains template placeholders and is unratified, as noted in `plan/plan_to_implement.md`. No approved constitution gates apply. This plan follows the explicit project direction: keep the pipeline deterministic and local, preserve interfaces, and use test-first changes.

## Design Decisions

- Exclude common English stop words from query relevance so incidental terms such as “the” and “in” cannot create evidence.
- Score the fraction of distinct meaningful query terms present in a passage, and require at least 0.5 coverage by default. This directly rewards evidence that covers more of the question and filters passages that only mention a broad topic word.
- Keep the current refusal text and cite only the passages returned by retrieval. A refusal has no citations.
- Keep retrieval passages within their configured character bounds, while retaining the complete source sentence context for answer text when a passage boundary cuts through a sentence.
- Add `--show-retrieval` as an opt-in CLI section with stable rank, passage ID, score, title, and text fields.
- Treat the two chunk configurations as an observed comparison. Do not claim that shorter or longer chunks are generally better.

## Project Structure

```text
src/
├── chunking.py       # splitting and passage metadata
├── retrieval.py      # lexical token relevance and ranked top-k
├── rag.py            # grounded answer and refusal behavior
└── cli.py            # optional ranked retrieval display
tests/
├── test_chunking.py
├── test_retrieval.py
├── test_rag.py
└── test_cli.py
evidence.md           # completed student evidence template
specs/001-week-6-rag-homework/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/cli.md
├── checklists/requirements.md
└── tasks.md
```

**Structure Decision**: Keep the single existing Python project. The feature extends existing modules and tests, and the homework requires no new package or service.

## Implementation Sequence

1. Add chunking behavior tests and preserve the implementation where it already satisfies them.
2. Add retrieval tests for score order, k limits, invalid k, empty/common-word questions, and the controlled chunk comparison; then adjust scoring only where a test exposes a gap.
3. Add supported citation, World Cup refusal, and empty-evidence tests; change answer behavior only if retrieval still admits unsupported evidence.
4. Add subprocess CLI tests for supported and unsupported examples, then implement the opt-in ranked evidence display.
5. Capture actual outputs from the prescribed commands in `evidence.md`, and run focused and full checks.

## Risks and Mitigations

- A manually chosen stop-word list can miss common terms. Tests cover the generic words in the specified unsupported question, while meaningful domain terms stay eligible.
- Chunk boundaries may split words because chunking is character-based. The comparison documents actual observed output and retains this existing behavior.
- Relevance scores change scale when they become query coverage. CLI output labels them as relative lexical relevance scores and keeps the scoring deterministic.
