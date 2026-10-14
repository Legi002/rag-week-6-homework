# Data Model: Local Prince Book Extension

All records below belong to the new book pipeline. Existing Document, Chunk, RetrievalResult and RagAnswer remain unchanged.

## BookManifest

An immutable profile constant carrying ebook ID, identity fields, release/update dates, canonical full-source/body hashes, normalizer `lf-v1`, parser `prince-sections-v1`, and expected ordered section keys. Production accepts only the researched edition. Tests inject a fixture manifest through the Python loader API; users have no CLI bypass.

## BookCorpus

- `doc_id`: `pg1232-` plus full canonical full-source SHA-256.
- `title`, `author`, `translator`, `language`, `ebook_id`, `release_date`, `updated_date`: parsed and manifest-validated metadata, not hard-coded replacements for input values.
- `source_url`: `https://www.gutenberg.org/ebooks/1232`.
- `download_url`: `https://www.gutenberg.org/cache/epub/1232/pg1232.txt` (acquisition record; application makes no network request).
- `raw_sha256`, `source_sha256`, `body_sha256`: exact byte, canonical full-source and canonical delimiter-interior digests.
- `body_text`: exact LF-normalized marker interior, retaining whitespace and Unicode.
- `sections`: ordered SourceSection records; excluded source ranges are not silently assigned to another section.
- `imported_at_utc`: optional run-provenance timestamp, excluded from stable IDs/ranking and deterministic console evidence.

Researched identity: English, ebook 1232, The Prince, Niccolo/Niccolo-with-accent Machiavelli as actually parsed, W. K. Marriott, release 2006-02-11, updated 2026-07-24. The canonical hash validates the exact spelling and contents; do not accept arbitrary alternate text merely because metadata resembles this description.

```text
raw_sha256    = 33496a305f7a4b933784fb5aec95f920fbc3d4687794817e4cc444aa6578d2e4
source_sha256 = 948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368
body_sha256   = 347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1
body length   = 282640 Unicode characters
```

## SourceSection

Fields: `section_id`, display `heading`, `kind`, `heading_start`, `content_start`, `end_char`, parent `doc_id`. Kinds are editorial-note, front-matter, chapter, appendix. `0 <= heading_start <= content_start < end_char <= len(body_text)`; ranges are ordered and nonoverlapping. Canonical source headings remain in body_text; only display headings join multiline text.

Expected ordered keys and exact source anchors:

| Keys | Source heading/anchor | Kind |
|---|---|---|
| editorial-note | `_ Nicolo Machiavelli, born at Florence` at line start | editorial-note |
| introduction | `INTRODUCTION` | front-matter |
| youth | `YOUTH — Æt. 1-25—1469-94` | front-matter |
| office | `OFFICE — Æt. 25-43—1494-1512` | front-matter |
| literature-death | `LITERATURE AND DEATH — Æt. 43-58—1512-27` | front-matter |
| man-works | `THE MAN AND HIS WORKS` | front-matter |
| dedication | `DEDICATION` | front-matter |
| chapter-01 through chapter-26 | bare Roman chapter marker; optional footnote suffix | chapter |
| appendix-valentino | first uppercase line `DESCRIPTION OF THE METHODS ADOPTED BY THE DUKE VALENTINO WHEN MURDERING`; collect three title lines | appendix |
| appendix-castruccio | `THE LIFE OF CASTRUCCIO CASTRACANI OF LUCCA` | appendix |

Match front anchors as complete unindented lines; their contents-list duplicates are indented. The note starts at its anchor and ends before INTRODUCTION. Chapter/appendix content starts after their gathered title lines. Front content starts after its single heading line. DEDICATION ends before the standalone THE PRINCE banner, which is excluded. The final appendix ends at len(body_text). Chapter I heading offset is 27890; XXVI is 201877; appendix starts are 209907 and 223990. These are measured edition checks, not offsets to hard-code into the parser.

Do not infer that an editorial passage was written by the book's author. Kind and source-edition labels make editorial content distinguishable; keep source bylines and notes.

## BookChunk and SentenceSpan

BookChunk fields: `chunk_id`, `doc_id`, `section_id`, heading/kind, `start_char`, `end_char`, exact `text`, chunk-size/overlap and parser/normalizer versions. Size is positive; overlap is nonnegative and smaller than size. `content_start <= start_char < end_char <= section.end_char`; `text == body_text[start_char:end_char]`.

SentenceSpan stores section key and exact half-open body offsets. Sentence text is derived by slicing, never by collapsing whitespace. A sentence cannot cross a section boundary. A sentence intersecting a retrieval chunk may extend beyond that chunk; it remains a separate evidence record.

Identifier format uses only ASCII letters/digits/hyphens:

```text
chunk_id = pg1232-{full source_sha256}-p1-c{size}-o{overlap}-{section_id}-w{start}-{end}
excerpt_id = pg1232-{full source_sha256}-p1-c{size}-o{overlap}-{section_id}-s{start}-{end}
```

No short digest is used as the identity key. Changing canonical source, parser or chunk configuration changes identifiers; line-ending/BOM equivalents do not. Changing question or top-k does not change chunk IDs. Never reuse one ID for different source slices within a run.

## BookIndex and BookRetrievalResult

BookIndex stores nonempty chunks, token Counters, df, N, average retained-token length, book token-policy version and k1/b. Zero-token chunks are omitted from N/df/avgdl consistently. Index construction happens once per command.

BookRetrievalResult fields: `chunk`, finite positive `score`, stable `rank`. Sort by descending unrounded score, then source start, end and ID. The full positive ranked set is available to admission; raw display is capped separately by top-k.

## EvidenceExcerpt and BookAnswer

EvidenceExcerpt fields: `excerpt_id`, `section_id`, heading/kind, exact source offsets/text, coverage 1.0, selected origin chunk ID/score, and admission-policy version. `0 < len(text) <= 2000`; it is one complete intersecting sentence and passes all requested-content gates. Deduplicate by exact body hash and sentence offsets, keeping the best stable origin.

BookAnswer fields: `answer`, `citations`, `refused`, `ranked_candidates`, `accepted_excerpts`, `refusal_reason`, source/parameter metadata. Non-refusals quote only accepted excerpts; citations are exactly their IDs in output order. Refusals have zero accepted excerpts and zero answer citations, even if raw candidates exist. k is a positive maximum, not a required number of quotations.

Stable diagnostic reasons: EMPTY_QUERY, UNSUPPORTED_POLARITY, UNSUPPORTED_HYPOTHETICAL, NO_ADMISSIBLE_SENTENCE. Candidate explanations may additionally record missing terms, overlong sentence, counted-list failure or missing causal/date cue. Diagnostics describe the policy, not proof that the book lacks information.

## EvaluationCase

Fields in [evaluation-cases.json](evaluation-cases.json): case ID, literal question, category, expected refusal, eligible section keys and required evidence fragments. Supported fragment checks normalize whitespace only in the test comparison; the answer itself remains an exact source slice. A separate known-false-refusal category records an answerable paraphrase the literal policy rejects. Runtime must not load this case list to recognize or answer questions.
