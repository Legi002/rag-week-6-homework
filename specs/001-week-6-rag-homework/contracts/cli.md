# CLI Contract: RAG Homework Evidence

## Inputs

The existing command accepts a question, a corpus profile, chunk size, overlap, and top-k limit. `--show-retrieval` enables the evidence inspection section.

## Output

With `--show-retrieval`, output contains a `Retrieved evidence:` section. Each result has a one-based rank, chunk ID, numeric score, source title, and source passage text. An empty result set is reported explicitly.

The answer section shows the grounded answer or refusal. Grounded answer text uses complete source sentences when a retrieved passage ends mid-sentence. The profile, refusal state, and answer citation IDs remain visible. Supported answer citations must match IDs from the evidence section; refusals show `Citations: None`.

Without `--show-retrieval`, the command retains its existing answer, profile, refusal, and citation output.

## Reproducible scenarios

- Supported: `--corpus-profile training-rag --question "Why are citations important in RAG?" --top-k 2 --show-retrieval`
- Unsupported: `--corpus-profile training-rag --question "Who won the World Cup in 1958?" --top-k 2 --show-retrieval`
