# Data Model: Week 6 RAG Homework

## Document

- `doc_id`: stable source identifier.
- `title`: human-readable source name.
- `text`: source content.
- Relationship: one document can produce zero or more passages.

## Passage (existing `Chunk`)

- `chunk_id`: unique identifier within the built corpus.
- `doc_id`: source document identifier.
- `title`: source title retained for display.
- `text`: bounded passage content.
- `answer_text`: complete source sentence or sentences that overlap the passage, used when assembling a readable grounded answer.
- Validation: each non-empty source passage is no longer than the configured character chunk size; chunk size is positive; overlap is non-negative and smaller than chunk size.

## Retrieval evidence (existing `RetrievalResult`)

- `chunk`: the supporting passage.
- `score`: deterministic lexical query coverage, ordered descending in retrieval output.
- Validation: output count is at most positive `k`; passages with no meaningful query-term overlap are excluded.

## Answer (existing `RagAnswer`)

- `answer`: grounded response text or refusal message.
- `citations`: passage IDs included as references in a supported answer.
- `refused`: whether evidence was insufficient.
- Invariant: refusal means citations are empty; supported citations identify retrieved passages included in the answer.
