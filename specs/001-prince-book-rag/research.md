# Research: Local Prince Book Extension

## 1. Correct baseline

Decision: extend commit `4c0e2b442bbcaeef1ffe7e1145400f310542112e`, retaining 32 tests, query-coverage retrieval, complete-sentence output, --show-retrieval and evidence.md. The earlier draft branched from `5afed23`, which had only nine tests and returned a cited response to the unrelated World Cup question in training-rag. The completed branch correctly refused it. No starter scorer is a compatibility requirement.

## 2. Edition and parsing

Decision: support the official English Marriott edition updated 2026-07-24, fingerprinted after BOM removal and LF normalization. The downloaded review copy was 308,019 bytes. Structural inspection found 26 chapter markers, six front sections, two appendices and one editorial note. Contents headings are distinct from bare body markers; XVIII includes [1]. Display headings use only contiguous uppercase lines; the first appendix has three title lines. Canonical source offsets are retained before any display formatting.

Alternative: accept any Gutenberg text with plausible metadata. Rejected because that can misattribute changed or forged text and makes citation reproduction unreliable. Future edition changes require an explicit profile/evaluation update; the current CLI does not bypass identity validation.

Primary sources: [ebook page](https://www.gutenberg.org/ebooks/1232), [official plain text](https://www.gutenberg.org/cache/epub/1232/pg1232.txt). Full source/body hashes and exact parser decisions are in plan.md and data-model.md. The source was obtained for a disposable design review, not bundled into the repository or downloaded by the application.

## 3. Exact ranking formula

Decision: positive-IDF BM25, k1=1.5, b=0.75, retained-token frequencies and length, distinct query terms, fixed tie breaks. The nonnegative IDF formula matches the variant documented by [Apache Lucene](https://lucene.apache.org/core/9_12_2/core/org/apache/lucene/search/similarities/BM25Similarity.html); 1.5 is our explicit design choice, not Lucene's 1.2 default. The [Stanford IR textbook](https://nlp.stanford.edu/IR-book/html/htmledition/okapi-bm25-a-non-binary-model-1.html) describes term-frequency saturation and length normalization. Use only the standard library.

Alternative: retain simple coverage for both corpora. It is less code but does not explore richer ranking. Alternative: add embeddings/model services. Outside the user-selected local quoted-answer scope. Neither BM25 rank nor a positive score proves answerability.

## 4. Separate admission from ranking

Decision: book-evidence-v1 requires full retained-term coverage in one complete source sentence, at most 2000 characters, with explicit counted-list, causal and date guards. Preserve numeric and negation information; refuse negated and hypothetical questions. Quote admitted source slices only. Inspect all positive candidates before capping accepted evidence and deduplicate exact sentence locations.

Experiments showed why broader policies fail: BM25 can rank the birth passage for a weather question, and full-window coverage can join Nicolo Machiavelli mentions to someone else's birth information. The introduction mentions five errors without enumerating them. Single-sentence admission plus a generic actual-counted-list check removes these observed cases. Do not introduce book-specific handlers or a four-question answer whitelist.

The user explicitly selected fully local quoted answers with conservative refusal and documented limits. Canonical questions use literal source vocabulary. The answerable Louis XII/make paraphrase is a known false refusal because this policy has no regnal-name aliases or stemming. One-sentence coverage still cannot prove arbitrary semantic answerability; exact source quotation and demonstrated refusal cases are the honest scope.

## 5. Canonical text and citations

Decision: use an unchanged canonical body with exact half-open Unicode character offsets. Trimming moves the stored window bounds; it never changes the step schedule. Complete sentences are distinct evidence excerpts with their own IDs/offsets and an origin chunk link. This avoids the misleading claim that a citation to a bounded window necessarily covers an expanded sentence.

Alternative: use the existing whitespace-collapsing baseline chunker for the book. Rejected because it destroys canonical line boundaries and cannot supply the new offsets unchanged. Baseline behavior remains untouched.

## 6. Validation and handoff

Research agents investigated source layout/provenance and scoring/refusal independently as the Spec Kit plan workflow requires. Their results were reconciled in the final disposable probe on all 35 indexed sections. Both 400/80 and 800/120 produced the required four supported quotations and refused seven negative cases. The paraphrase refusal is tracked separately, not counted as an unsupported-book success. See validation.md for exact experiment scope and the unrun application checks.

Use synthetic fixture manifests for unit tests. Do not commit the real book or copy experimental scores into evidence-prince.md as if the CLI ran. The implementation must generate its own evidence from the fixed case list, preserve existing evidence.md, run all inherited tests and compare exact quote content.
