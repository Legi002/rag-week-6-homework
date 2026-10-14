# RAG Week 6 Homework Constitution

## Core Principles

### I. Trace quotations to actual evidence

Answers MUST distinguish source quotation from generated inference. Every quotation MUST identify its corpus and supporting source location. Refusal MUST occur when the selected evidence policy does not admit support; a refusal MUST NOT be presented as proof that the corpus contains no possible answer.

### II. Keep source identity explicit

External corpus profiles MUST retain source and edition metadata with reproducible content identity. Source parsing MUST validate the supported input format and edition rather than silently assign hard-coded provenance to arbitrary text. A full downloaded corpus MUST NOT be committed as a development fixture.

### III. Keep responsibilities and scope explicit

Corpus loading, chunking, ranking, evidence admission and CLI rendering MUST remain separately testable. A dependency or service MUST have a documented learning or functional benefit. The default homework remains local; any future feature needing external services MUST document and justify that choice in its own reviewed plan. The current Prince extension is explicitly fully local and model-free by user choice.

### IV. Make claims reproducible

Evidence MUST record corpus identity, settings, ranked context, citations and refusal behavior. Tests MUST cover observable requirements, including negative cases. Planning experiments MUST be labelled separately from implementation results; unknown or unrun checks MUST NOT be reported as passes.

### V. Preserve completed homework

The baseline is the completed homework at 4c0e2b442bbcaeef1ffe7e1145400f310542112e. Its built-in profiles, public interfaces, default behavior, tests and original evidence MUST remain usable. Optional extension data or configuration MUST NOT be required for baseline commands.

## Additional Constraints

- The repository is a Python command-line learning exercise.
- Standard-library runtime code is preferred; an added dependency requires a stated reason.
- pytest is the existing test dependency. Tests use small controlled fixtures, not the full external book.
- User-provided files are inputs. Synced project reference material remains read-only.

## Development Workflow

Record requirements, a validated design, explicit contracts and acceptance criteria before implementation. Keep source scores separate from evidence sufficiency and test exact citations. Preserve passing baseline checks and record actual feature evidence after code exists. Stop and report conflicting governing documents instead of silently selecting a convenient interpretation.

## Governance

This is the initial committed project constitution, replacing an unratified template/draft. It is adopted for the extension branch on 2026-10-14. Amendments MUST describe affected behavior and update semantic versioning: incompatible principles require a major version, new guidance a minor version, and clarifications a patch. Feature plans MUST evaluate compliance and document justified exceptions. Do not impose a feature-specific service restriction on all future extensions without a deliberate amendment.

**Version**: 1.0.0 | **Ratified**: 2026-10-14 | **Last Amended**: 2026-10-14
