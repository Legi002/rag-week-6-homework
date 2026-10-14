# Feature Specification: Local Prince Book Extension

**Feature Branch**: `feat/extended-rag-homework`
**Created**: 2026-10-14
**Status**: Planned; implementation not started
**Input**: Extend the completed Week 6 homework using the suggested book, resolve the reviewed design gaps, and stop before implementation. The user selected fully local quoted answers with conservative refusal and documented limits.

## User Scenarios & Testing

### User Story 1 - Search a verified local book (Priority: P1)

A learner selects a downloaded copy of The Prince while retaining the completed homework and both built-in corpora.

**Why this priority**: The extension must build on the completed exercise, not replace it with the starter.
**Independent Test**: Existing homework examples still work; a verified book loads; a different book or unsupported edition fails clearly.

**Acceptance Scenarios**:
1. Given the completed homework, when no book is selected, all existing commands, evidence and defaults retain their behavior.
2. Given the researched English edition, when selected locally, the learner can search its 26 chapters, editorial material and two appendices.
3. Given another book, changed edition, missing file, invalid encoding or damaged structure, selection reports an actionable error rather than attributing that text to The Prince.

### User Story 2 - Inspect ranked evidence and exact citations (Priority: P2)

A learner sees ranked passages and can trace every quoted answer to exact text in the identified edition.

**Why this priority**: Book retrieval must be inspectable and citations must identify the actual quoted evidence.
**Independent Test**: Every answer citation resolves to a displayed accepted excerpt and its exact source location; ranked candidates may be displayed even when no answer is admitted.

**Acceptance Scenarios**:
1. Repeating the same question, edition and settings produces the same rankings and citation identifiers.
2. A supported question returns complete source quotations with section labels and exact source locations.
3. An unsupported weather, birth-time, salary or temperature question refuses with no answer citations even when topical candidates are retrieved.
4. Asking for five errors requires evidence containing the five listed items; an introductory mention of the errors is insufficient.
5. A conservative refusal can occur for a valid paraphrase; the output explains that insufficient admitted evidence does not prove the book lacks an answer.

### User Story 3 - Compare and reproduce results (Priority: P3)

A learner compares two chunking configurations and records supported and refused cases without inventing results.

**Why this priority**: The extension continues all five homework outcomes and produces a reviewable handoff.
**Independent Test**: The fixed evaluation cases are reproducible at both configurations and the completed baseline evidence remains intact.

**Acceptance Scenarios**:
1. Comparing the same questions at two configurations records settings, edition identity, ranked candidates, accepted quotations and refusals.
2. Results include the five-error list, loved/feared comparison, mercenary reasons and birth date, plus the difficult negative cases.
3. The report distinguishes planning experiments from results of the eventual implemented application.

### Edge Cases

- Contents-list headings resemble body headings; one chapter heading contains a footnote suffix.
- Source metadata claims the correct book but its contents differ.
- Line endings or a leading byte-order mark vary without changing the canonical edition.
- A chunk boundary cuts a sentence; whitespace trimming must not corrupt locations.
- Common words, numbers, negation, unknown terms and repeated query words must not create unsupported evidence.
- Several overlapping chunks identify the same sentence; it is quoted once.
- A sentence is too long, a requested list format is unsupported, or a paraphrase uses absent terms: refuse conservatively.

## Requirements

### Functional Requirements

- **FR-001**: Preserve the completed homework's two built-in corpora, public interfaces, CLI defaults, retrieval display option, complete-sentence answers, tests and original evidence.
- **FR-002**: Accept a local plain-text copy of the researched English edition of ebook 1232; validate its identity, edition and structure before using it.
- **FR-003**: Retain source title, author, translator, language, release/update dates, source addresses and content fingerprints.
- **FR-004**: Index the documented 35 source sections, excluding the contents list and license; distinguish chapters, editorial/front matter and appendices.
- **FR-005**: Make each chunk and admitted quotation resolvable to exact source text, a section and a configuration-sensitive identifier.
- **FR-006**: Rank passages deterministically with inspectable scores; scores are relevance signals, not confidence that a question is answered.
- **FR-007**: Return only complete, contiguous source quotations admitted by the documented conservative evidence policy. Do not synthesize new factual claims.
- **FR-008**: Refuse when evidence fails that policy. Refusals have no answer citations, and do not assert that the source contains no possible answer.
- **FR-009**: Display raw ranked candidates separately from admitted answer evidence when retrieval display is requested.
- **FR-010**: Invalid inputs produce concise errors and an unsuccessful command result; supported answers and conservative refusals are successful command executions.
- **FR-011**: Add focused automated checks for identity/parsing, source locations, ranking, evidence admission, CLI compatibility and the fixed evaluation cases; retain all 32 inherited tests.
- **FR-012**: Record two chunk configurations and top-k limits of two and three on the same identified edition in a separate book evidence report.
- **FR-013**: An explicitly selected built-in corpus and a book file are mutually exclusive; omitting both selects the existing default corpus.
- **FR-014**: The extension works offline after the learner obtains the source. The full downloaded book remains outside version control.

### Key Entities

- **Book source**: A verified edition, its provenance and exact canonical text.
- **Source section**: An ordered labelled source region with kind and locations.
- **Indexed chunk**: A configured source window used for ranking.
- **Evidence excerpt**: One admitted complete source sentence, its origin chunk and exact location.
- **Book result**: Raw candidates, admitted excerpts, quoted response or refusal, and citations.
- **Evaluation case**: A fixed question with required evidence content or expected refusal.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every inherited homework check passes and the original evidence is preserved.
- **SC-002**: The researched source exposes exactly 26 chapters and 35 indexed sections; contents and license text are excluded.
- **SC-003**: Every supported quotation and citation resolves to the exact identified source slice; repeated identical inputs reproduce identifiers.
- **SC-004**: All four canonical supported cases satisfy the content requirements at both comparison configurations, with no more quotations than the selected limit.
- **SC-005**: All seven fixed negative cases refuse with zero answer citations at both configurations; the known paraphrase false-refusal is reported separately.
- **SC-006**: A changed or misidentified edition is rejected; equivalent line endings and a leading byte-order mark do not change canonical source identity.
- **SC-007**: The report reproduces all five homework outcomes and clearly separates observed results from unrun implementation checks.

## Assumptions

- Scope is one English edition of The Prince, not a general document loader or semantic question-answering service.
- The learner downloads the source manually; the application does not fetch it.
- The user selected fully local quoted answers with conservative refusal. Literal matching sacrifices paraphrase recall and cannot guarantee arbitrary natural-language answerability.
- Broad semantic understanding, entity aliases, stemming and model integration are deferred features, not hidden implementation requirements.
- Planning experiments inform the design; implemented-feature acceptance remains for the next session.
