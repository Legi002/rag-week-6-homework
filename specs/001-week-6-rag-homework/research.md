# Research: Week 6 RAG Homework

## Decision 1: Deterministic lexical relevance

**Decision**: Filter common English stop words from the query and score a passage by the proportion of distinct remaining query terms it contains. By default, require at least 0.5 query-term coverage for a passage to be returned.

**Rationale**: The starter counts all query tokens, including generic words such as “the” and “in”, and divides by passage length. That allows unsupported questions to pass the low relevance cutoff due to incidental overlap. Query-term coverage is deterministic, easy to inspect, and directly reflects how much of a question's meaningful vocabulary a passage supports. The minimum coverage filters a broad topic match such as “RAG” alone from a citation-specific question, while a one-term question such as “What is RAG?” can still return matching evidence.

**Alternatives considered**:

- Keep raw token overlap and raise the global threshold: this remains sensitive to generic words and passage length.
- Add external embeddings or a model: outside the local, deterministic homework scope.
- Add inverse document frequency: more complex than needed for four short, fixed documents.

## Decision 2: Inspect evidence through an opt-in CLI flag

**Decision**: Add `--show-retrieval`; print rank, chunk ID, score, source title, and passage text when requested.

**Rationale**: The CLI already exposes profile, chunking, and k settings, but only prints final answer citations. An optional evidence section makes the homework comparison reviewable without changing the default transcript.

**Alternatives considered**:

- Always print evidence: adds output to existing CLI runs unnecessarily.
- Add a separate inspection command: duplicates CLI setup and makes the evidence journey harder to reproduce.

## Decision 3: Preserve current chunking and answer contracts

**Decision**: Keep character-based chunking and the existing answer/refusal type. Add tests first and change these modules only if a stated behavior fails.

**Rationale**: Current code already validates chunk size/overlap, returns source metadata, caps results at k, and forms citations from retrieved chunk IDs. The demonstrated gap is generic-token relevance and missing CLI evidence visibility.

**Alternatives considered**:

- Rewrite chunking or response structure: unnecessary for the acceptance criteria and risks breaking the starter interfaces.
