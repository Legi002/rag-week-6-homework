# Handoff to the Implementation Session

Repository: `C:\Users\AleksA\Documents\Codex\2026-10-13\https-github-com-legi002-rag-week\work\rag-week-6-homework`
Branch: `feat/extended-rag-homework`
Completed baseline: `4c0e2b442bbcaeef1ffe7e1145400f310542112e`
Feature directory: `specs/001-prince-book-rag`

The user authorized planning only in the current session. Application implementation is for a later session. The source base is now the completed homework; planning files resolve scoring, refusal, parsing, provenance, offsets and validation. Planning experiments passed their documented cases, but no implementation task or future CLI command has been completed.

## Prompt for the next session

Implement the local Prince book extension with `$speckit-implement` in the repository and branch above. Read `.specify/memory/constitution.md` and every file in `specs/001-prince-book-rag/`, including both contracts, evaluation-cases.json, validation.md and tasks.md. Then do T001-T030 in order, writing the specified behavior tests before their implementation. Preserve all 32 inherited tests and the completed baseline scorer/defaults/--show-retrieval/complete-sentence output/evidence.md. Stop and report if the baseline preflight fails or the documents conflict.

Use only the standard library at runtime. Book scores are BM25 ranking signals; exact one-sentence quotations are separately admitted by the documented conservative policy. Do not add a model, hidden source aliases, demo-question whitelist or universal semantic-answerability claim. Source slices and fingerprints are mandatory. The book stays outside Git and no application network download is needed.

Implement the optional source tests; obtain the supported edition locally for the final real-book checks. Do not label skipped source tests as passes. Generate evidence-prince.md from real application commands, including the known Louis XII/make false refusal. Report actual tests, case results, performance, commit and remaining limitations. Commit only reviewed extension files on this branch.

## Spec Kit feature selection

The installed core resolves its feature from a per-checkout pointer or explicit directory, independently from the Git branch name. The current pointer is `.specify/feature.json` with `specs/001-prince-book-rag`. A fresh checkout must select this directory explicitly; do not accidentally use the inherited `specs/001-week-6-rag-homework`.

For Git Bash commands launched from PowerShell, use a login shell so its standard tools are available, and set the explicit directory when needed:

```powershell
$env:SPECIFY_FEATURE_DIRECTORY = 'specs/001-prince-book-rag'
& 'C:\Program Files\Git\bin\bash.exe' -lc './.specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks'
```

Read root/project instructions applicable in the new session as well. The local path is outside the mirrored project's default writable roots; use the normal approval flow for repository writes rather than relocating or bypassing permissions.
