# Feature Specification: Week 6 RAG Homework

**Feature Branch**: `001-week-6-rag-homework`

**Created**: 2026-10-13

**Status**: Approved for implementation

**Input**: User description: "Implement plan/plan_to_implement.md"

## User Scenarios & Testing

### User Story 1 - Compare chunking configurations (Priority: P1)

A student runs the same question over the same corpus with two chunking configurations, inspects the retrieved passages, and explains the observed difference.

**Why this priority**: Comparing configurations teaches how chunk boundaries affect the evidence available to retrieval.

**Independent Test**: Run the citation question against the training corpus with chunk sizes 140/overlap 30 and 80/overlap 20. Compare the retrieved passage IDs and text.

**Acceptance Scenarios**:

1. **Given** the same corpus and question, **When** the student uses each configuration, **Then** both runs show their retrieved passages and configuration values.
2. **Given** the two retrieval outputs, **When** the student compares them, **Then** the observed difference can be explained without assuming that either configuration is always better.

### User Story 2 - Inspect ranked top-k evidence (Priority: P1)

A student asks a question and inspects a capped list of evidence passages ranked by relevance.

**Why this priority**: Ranked evidence is the basis for deciding whether a response is supported.

**Independent Test**: Retrieve evidence for a supported question with limits of two and three, then confirm order and count.

**Acceptance Scenarios**:

1. **Given** a question with matching evidence, **When** the student requests k results, **Then** at most k passages appear in descending score order.
2. **Given** a question that only shares common words with corpus passages, **When** the student retrieves evidence, **Then** those words alone do not make an unrelated passage relevant.
3. **Given** an empty question or invalid result limit, **When** retrieval is requested, **Then** it returns no evidence or reports the invalid limit clearly.

### User Story 3 - Cite grounded answers (Priority: P1)

A student asks a question supported by the corpus and receives an answer that identifies the source passages used.

**Why this priority**: Source references make the answer traceable and let students check its support.

**Independent Test**: Ask why citations are important in RAG and compare the answer references with the ranked evidence IDs.

**Acceptance Scenarios**:

1. **Given** a supported question, **When** the student requests an answer, **Then** the response contains a non-empty grounded answer and citation IDs.
2. **Given** the answer citations, **When** they are compared with retrieved evidence, **Then** every cited ID identifies a retrieved source passage whose text appears in the answer.
3. **Given** a retrieved passage that ends within a source sentence, **When** the answer is assembled, **Then** the answer presents the complete source sentence rather than the truncated passage fragment.

### User Story 4 - Refuse unsupported questions (Priority: P1)

A student asks a question unsupported by the corpus and receives a clear refusal without answer citations.

**Why this priority**: Refusal prevents the system from treating accidental word overlap as factual support.

**Independent Test**: Ask who won the 1958 World Cup against the training corpus and inspect the refusal and citation fields.

**Acceptance Scenarios**:

1. **Given** an unsupported question, **When** the student requests an answer, **Then** the response clearly states that the corpus lacks enough evidence.
2. **Given** an unsupported question with accidental overlap on common words, **When** the response is produced, **Then** it contains no citations.
3. **Given** no corpus passages, **When** any question is asked, **Then** the system refuses and returns no citations.

### User Story 5 - Reproduce homework evidence (Priority: P2)

A student records reproducible examples for chunking, top-k ranking, a supported cited answer, and an unsupported refusal.

**Why this priority**: Reproducible evidence lets a reviewer confirm all five homework outcomes from the delivered project.

**Independent Test**: Follow the evidence document commands and compare their visible outputs with the recorded evidence.

**Acceptance Scenarios**:

1. **Given** the evidence document, **When** a reviewer follows its commands, **Then** the supported example displays ranked passages and matching citations.
2. **Given** the evidence document, **When** a reviewer follows its unsupported example, **Then** it displays the retrieved evidence state, a refusal, and no citations.
3. **Given** both chunking configurations, **When** a reviewer follows the commands, **Then** the corpus and question remain the same while the configuration changes.

### Edge Cases

- Whitespace-only text produces no chunks.
- Chunk sizes must be positive, overlap must be non-negative and smaller than the chunk size, and k must be positive.
- Empty questions and questions made only of common words produce no retrieval evidence.
- A query with no supporting chunks returns a refusal and an empty citation list.

## Requirements

### Functional Requirements

- **FR-001**: Students MUST be able to compare retrieval evidence for the same question and corpus under two chunking configurations.
- **FR-002**: The system MUST return no more than the requested positive number of relevant passages, ordered from highest to lowest relevance.
- **FR-003**: Common words alone MUST NOT cause a passage to count as relevant evidence.
- **FR-004**: A supported answer MUST include source passage IDs that correspond to the retrieved evidence used in the answer.
- **FR-005**: An unsupported answer MUST clearly refuse and contain no citations.
- **FR-006**: Students MUST be able to inspect ranked passage IDs, relevance scores, source titles, and passage text in CLI output.
- **FR-007**: The submission evidence MUST include the two-configuration comparison, top-k examples, a supported cited answer, and an unsupported refusal with reproducible commands and outputs.
- **FR-008**: Grounded answers MUST use complete source sentences when retrieved passage boundaries cut through a sentence.

### Key Entities

- **Document**: A corpus source with an ID, title, and text.
- **Passage**: A bounded part of a document with its own ID and the source document's identifying metadata.
- **Retrieval evidence**: A passage and its relevance score in the ranked results for a question.
- **Answer**: A response with answer text, citation IDs, and a refused/supported state.

## Success Criteria

### Measurable Outcomes

- **SC-001**: For any valid k, displayed retrieval contains at most k results in descending score order.
- **SC-002**: The supported example has at least one citation, and each citation ID exactly matches a displayed retrieved passage ID.
- **SC-003**: The unsupported example is visibly refused and has zero citations, including when its wording shares common words with corpus passages.
- **SC-004**: The evidence document contains commands and outputs for both chunking configurations, top-k values two and three, and supported and unsupported questions.
- **SC-005**: Repeating an example with the same corpus, question, and settings produces the same chunk IDs, ranked order, and response state.
- **SC-006**: A supported answer contains complete sentences even when its ranked passage text ends mid-sentence.

## Assumptions

- Students use the supplied local corpus profiles, especially `training-rag` for citation and refusal examples.
- Corpus contents and lexical retrieval are deterministic; external models and services are outside this homework scope.
- The example chunking configurations are an experiment and do not imply a universally best size or overlap.
- The existing Python CLI remains the way students reproduce the examples.
