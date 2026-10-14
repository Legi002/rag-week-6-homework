# Validation Plan and Observed Planning Results

## Evidence boundary

Date: 2026-10-14. Application implementation has not started. The checks below distinguish disposable design experiments, inherited baseline tests and future application acceptance. Never copy planning results into evidence-prince.md as if they were application CLI output.

## Observed before implementation

- Isolated copies of Git source were tested without changing the original repository: main at 5afed23 passed 9 checks; completed homework at 4c0e2b4 passed 32.
- The completed training-rag World Cup command correctly refused; the starter returned unrelated quoted material. The completed source is the required base.
- Source inspection verified 26 chapter markers, 35 indexed sections, 282640 canonical body characters, all three fingerprints and all-uppercase title handling. XVIII's footnote suffix and the first appendix's three-line title are accounted for.
- A disposable experiment on all 35 sections, preserving canonical source text, validated the chosen BM25 formula and single-sentence/count/causal/date admission rules. Each configuration ran the same 12 cases: four positives, seven negatives and one tracked false refusal. All 24 expected outcomes passed. This is not an application test suite.

| Configuration | Nonempty chunks in probe | Average retained tokens | Supported cases | Negative cases | Known false refusal |
|---|---:|---:|---:|---:|---:|
| 400 / 80 | 875 | 33.341714 | 4/4 admitted | 7/7 refused | 1/1 recorded |
| 800 / 120 | 421 | 64.410926 | 4/4 admitted | 7/7 refused | 1/1 recorded |

Five errors came from chapter III, the comparison from XVII, mercenary reasons from XII. Birth quotations came from INTRODUCTION and the editorial note, both correctly attributed source regions. The weather case also used 3rd rather than 3, confirming refusal is not explained solely by ordinal token mismatch.

The temporary probe and downloaded source live outside the homework repository. Its count figures are regression clues, not a substitute for the implementation's source-slice assertions and content oracles. Broader semantic answerability and application speed have not been established.

## Mandatory synthetic checks for implementation

The seven negative cases are policy-refusal checks, not seven claims of absent source information. In particular, the birth-date evidence can inform an answer about a wrong year or negated premise, but this local mode deliberately does not perform that reasoning. The separately tracked paraphrase measures literal-matching recall. Do not call refusals to these cases proof that the book has no answer.

| Area | Required checks | Test location |
|---|---|---|
| Identity and input | missing/nonfile/unreadable path, invalid UTF-8, empty text, another book, changed content with plausible metadata, malformed/duplicate/reversed markers, source mismatch, BOM/CRLF equivalence | tests/test_book_corpus.py |
| Parser | exact I-XXVI order; missing, duplicate and reordered chapters; XVIII suffix; uppercase-only multiline titles; six front sections, note and appendices; excluded contents/banner/license; byline retention | tests/test_book_corpus.py |
| Locations | Unicode offsets; exact chunk slices after trim; unchanged step schedule; no cross-section windows; sentence offsets exact; ID changes with source/parser/configuration and stays stable for identical inputs | tests/test_book_retrieval.py |
| Ranking | independently calculated BM25 scores on small controlled chunks; length/frequency effects; repeated query words do not inflate score; absent terms and zero-token index; stable ties; finite positive results | tests/test_book_retrieval.py |
| Admission | full terms in one sentence; words split across sentences refuse; unknown/numeric/negation terms retained; empty and hypothetical requests; sentence >2000 chars; real n-item colon list vs mention/count mismatch; why without causal cue and when without year refuse | tests/test_book_rag.py |
| Citations | only accepted excerpts cited; exact canonical quote slices; best-origin stable tie; duplicates removed before k; positive candidate below raw top-k can become accepted; refusal can retain raw candidates without citations | tests/test_book_rag.py |
| CLI | all inherited commands/output tests; omitted vs explicit default profile; profile/file conflict; defaults by selected mode; invalid parameters/load stderr exit 2; book answer/refusal exit 0; candidate/accepted sections separate and opt-in | tests/test_cli.py |

Use a generated small synthetic 35-section source and explicit fixture manifest. Tests that mutate the fixture to check parser failures must update that fixture's hash deliberately, so they reach the parser instead of stopping at edition mismatch. Also separately prove the production manifest rejects that synthetic source. Do not weaken the actual CLI's manifest.

Controlled BM25 oracle: chunks `cat cat dog`, `cat fish`, `dog bird`, query `cat`; N=3, df(cat)=2, avgdl=7/3, IDF=ln(1.6), k1=1.5/b=0.75. Independently calculate the expected first two scores, require the first > second > 0, and third absent. Verify `cat cat` has identical scores. Add a zero-token chunk and prove statistics do not change. Do not compute expected values by calling the scorer being tested.

## Optional real-book acceptance tests

Read RAG_PRINCE_FILE when available. Absence must produce an explicit skip, not a pass. The production hash must match. Read the fixed cases in evaluation-cases.json from the test/evaluation layer only; runtime never loads them.

Run all 12 cases at both configurations and k=2 and k=3: 48 case/configuration/limit combinations. Supported cases must satisfy every required fragment within admitted exact quotes from an eligible section. Whitespace may be normalized for fragment comparisons only. Do not accept a chapter match, score or bare word overlap as the oracle.

For each result assert citations exactly match admitted excerpt IDs and every quote is the identified source slice; raw and accepted counts are separately <=k in console display; refusal has zero citations. Canonical five-error evidence must include all five clauses. The comparison must retain its qualification; mercenaries must include reasons; the birth case must include 1469, not a death-year excerpt. Assert the paraphrase case is labelled a known false refusal in the evidence report.

## Completion gate for implementation

1. Inherited preflight passes before new code: 32 tests, completed base ancestor, clean feature branch.
2. Synthetic checks and all inherited tests pass after implementation; real-book cases pass or remain explicitly unverified if the source is unavailable. Final readiness requires the real-book run, not a skipped run.
3. CLI evidence from actual runs is written to evidence-prince.md with all five outcome sections, edition hashes, parameter/policy versions and commands. Preserve evidence.md.
4. Measure book command latency at 800/120/k3 on the implementation machine; target five seconds, report actual timing and machine, investigate a failure before claiming readiness.
5. Review diff against 4c0e2b4: new book modules/tests and scoped CLI/docs changes only; baseline modules, full ebook, virtual environment, secrets and temporary probes are not extension changes.

No implementation result is premarked complete in tasks.md. The implementation session records actual commands/results as it finishes each phase.
