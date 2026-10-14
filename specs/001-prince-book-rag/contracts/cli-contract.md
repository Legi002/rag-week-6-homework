# CLI Contract: Local Prince Book Extension

## Baseline compatibility

Preserve completed-homework commands, output, public defaults and IDs:

```text
python -m src.cli --question "What is retrieval augmented generation?"
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --show-retrieval
python -m src.cli --corpus-profile training-rag --question "Who won the World Cup in 1958?" --show-retrieval
```

The built-in scorer is meaningful-query coverage with default 0.5 filtering, not the starter's overlap scorer. CLI defaults remain 140/30/top-k 2. Existing retrieval display is opt-in. Preserve exact refusal wording and complete-sentence baseline answers; do not route BM25 through baseline rag.py.

## Book selection

```text
python -m src.cli --corpus-file PATH --question QUESTION
  [--chunk-size N] [--overlap N] [--top-k N] [--show-retrieval]
```

- `--corpus-file` selects the manifest-validated local English edition. No download, URLs as input, model calls or automatic edition fallback.
- Explicit `--corpus-profile` and `--corpus-file` conflict, including explicit `--corpus-profile default`. If both are omitted, use the baseline default profile. Use parse sentinels to distinguish an omitted profile from explicit selection.
- Book defaults: chunk size 800, overlap 120, top-k 2. Built-in defaults stay unchanged. Resolve each omitted setting after dispatch; an explicit small chunk with omitted overlap may therefore be invalid and must receive a clear parameter error, not silent overlap adjustment.
- Parameter validation: size > 0, 0 <= overlap < size, top-k > 0. An empty/all-stop-word book question is a conservative refusal, not a parser crash.

## Book output

Always show Question, Corpus profile `prince-book`, source title/translator, full canonical source/body digests, parser/token/admission versions, chunk settings, BM25 k1/b, Answer, Refused and Citations. The positive answer heading is `Matching source excerpts:` and quotes exact text only. Show a References section for admitted excerpt IDs, section kind/heading, exact half-open source offsets and origin chunk ID. Display no unsupported factual synthesis.

With `--show-retrieval`, show two separately labelled sections before the answer:

1. `Raw ranked candidates:` at most k indexed windows, with rank, chunk ID, BM25 score, section/kind, source offsets and exact text. A rejected topical candidate can appear here on refusal.
2. `Accepted answer evidence:` at most k unique complete sentences, with excerpt ID, origin chunk ID/score, policy version, exact source offsets/text. Show `None` if no excerpt is admitted. An accepted excerpt may originate below raw top-k because admission inspects all positive candidates.

Only accepted excerpt IDs appear in answer Citations. Candidate IDs never become citations by being displayed. Refusal shows the existing `I do not have enough grounded evidence in the provided corpus to answer that question.` plus `The local quote policy did not admit evidence; this does not prove the book lacks an answer.` and a stable diagnostic reason. Citations is None. Empty accepted evidence is compatible with nonempty raw candidates.

## Exit codes and errors

- 0: supported quotation or ordinary conservative refusal.
- 2: argparse selection conflict, invalid size/overlap/top-k, missing/unreadable/nonfile input, invalid UTF-8, malformed marker/header/structure or unsupported edition. Write a concise `error:` diagnostic to stderr without a traceback; stdout must not contain an answer or partial corpus evidence on failed load.
- A changed digest explains that only the researched edition is supported and a reviewed manifest/evaluation update is needed. Do not suggest bypassing validation.

Do not retrofit new book input/error/output rules onto unrelated legacy commands. In particular, built-in output must retain the inherited contract and all 32 tests.
