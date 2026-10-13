# Week 6 RAG Homework Evidence

1. **Outcome 1: Chunking impact**
   - **Query and corpus**: `Why are citations important in RAG?` against `training-rag` for both runs.
   - **Config A**: `chunk_size=140`, `overlap=30`.
     - Command: `python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 140 --overlap 30 --top-k 2 --show-retrieval`
     - Retrieved evidence: rank 1, `tr-doc-1-chunk-0`, score `0.6667`, title `RAG with Citations`.
     - Text: `RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transpare`
   - **Config B**: `chunk_size=80`, `overlap=20`.
     - Command: `python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 80 --overlap 20 --top-k 2 --show-retrieval`
     - Retrieved evidence: rank 1, `tr-doc-1-chunk-0`, score `0.6667`, title `RAG with Citations`.
     - Text: `RAG with citations should retrieve relevant documents with source metadata and i`
   - **Retrieval difference summary**: Both settings select the same source passage ID and score, while the smaller chunk exposes a shorter excerpt. The larger chunk includes more surrounding context for this question; this single comparison does not establish that larger chunks are always better. Both runs return one result because the other candidates do not meet the minimum meaningful-query coverage threshold.

2. **Outcome 2: Top-k retrieval**
   - **Query**: `Why are citations important in RAG?`
   - **Top-k output**:
     - With `--top-k 2`: rank 1 is `tr-doc-1-chunk-0` at `0.6667`; one result is returned.
     - With `--top-k 3`: rank 1 is `tr-doc-1-chunk-0` at `0.6667`; one result is returned.
     - Commands:

       ```bash
       python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --top-k 2 --show-retrieval
       python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --top-k 3 --show-retrieval
       ```

   - **Why ranking is correct**: The top passage contains two of the question's three meaningful terms (`citations` and `RAG`), so its score is `2/3`. A passage that only mentions the broad term `RAG` scores `1/3` and is filtered. `k` is a maximum result count; it does not add weak evidence to fill the list.

3. **Outcome 3: Citation quality**
   - **Supported query**: `Why are citations important in RAG?`
   - **Answer with citations**: The grounded answer includes the complete source sentences “RAG with citations should retrieve relevant documents with source metadata and include references in the answer.” and “Citations improve transparency and trust because users can verify evidence.” with `[tr-doc-1-chunk-0]`.
   - **Retrieved chunk IDs**: `tr-doc-1-chunk-0`. The answer citation exactly matches the displayed retrieval ID.

4. **Outcome 4: Refusal behavior**
   - **Unsupported query**: `Who won the World Cup in 1958?`
   - **Retrieved context**: None. The query has no meaningful term overlap with the local corpus.
   - **Refusal output**: `I do not have enough grounded evidence in the provided corpus to answer that question.` Citations: `None`.

5. **Outcome 5: Final evidence pair**
   - **Supported case command + output**:

     ```bash
     python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --top-k 2 --show-retrieval
     ```

     ```text
     Question:
     Why are citations important in RAG?

     Retrieved evidence:
       Rank: 1
         Chunk ID: tr-doc-1-chunk-0
         Score: 0.6667
         Source: RAG with Citations (tr-doc-1)
         Text: RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transpare

     Answer:
     Grounded response based on retrieved context:
     [tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.

     Corpus profile: training-rag

     Refused: False
     Citations: tr-doc-1-chunk-0
     ```

   - **Unsupported case command + output**:

     ```bash
     python -m src.cli --corpus-profile training-rag --question "Who won the World Cup in 1958?" --top-k 2 --show-retrieval
     ```

     ```text
     Question:
     Who won the World Cup in 1958?

     Retrieved evidence:
       None

     Answer:
     I do not have enough grounded evidence in the provided corpus to answer that question.

     Corpus profile: training-rag

     Refused: True
     Citations: None
     ```
