# Quickstart: Week 6 RAG Homework

Run from the repository root with the project dependencies installed.

## Chunking comparison

```bash
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 140 --overlap 30 --top-k 2 --show-retrieval
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 80 --overlap 20 --top-k 2 --show-retrieval
```

Compare the configuration, retrieved IDs, scores, and passage text. Record the actual difference; neither configuration is assumed to be better.

## Top-k comparison

```bash
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --top-k 2 --show-retrieval
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --top-k 3 --show-retrieval
```

Confirm result count and descending score order.

## Supported and unsupported journeys

```bash
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --top-k 2 --show-retrieval
python -m src.cli --corpus-profile training-rag --question "Who won the World Cup in 1958?" --top-k 2 --show-retrieval
```

The supported answer must cite displayed passage IDs. The unsupported answer must refuse and show no citations. See [the CLI contract](contracts/cli.md) and the completed root [evidence.md](../../evidence.md).
