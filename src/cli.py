import argparse

from .chunking import build_chunks
from .corpus import list_corpus_profiles, load_corpus
from .rag import build_grounded_answer
from .retrieval import retrieve_top_k


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Week 6 RAG homework starter")
    parser.add_argument("--question", required=True, help="Question to ask over the local corpus")
    parser.add_argument("--chunk-size", type=int, default=140, help="Chunk size in characters")
    parser.add_argument("--overlap", type=int, default=30, help="Chunk overlap in characters")
    parser.add_argument("--top-k", type=int, default=2, help="Number of retrieved chunks")
    parser.add_argument(
        "--corpus-profile",
        default="default",
        choices=list_corpus_profiles(),
        help="Corpus profile: default or training-rag",
    )
    parser.add_argument(
        "--show-retrieval",
        action="store_true",
        help="Show ranked retrieval evidence before the answer",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    corpus = load_corpus(args.corpus_profile)
    chunks = build_chunks(corpus, chunk_size=args.chunk_size, overlap=args.overlap)
    result = build_grounded_answer(args.question, chunks, top_k=args.top_k)
    retrieved = retrieve_top_k(args.question, chunks, k=args.top_k) if args.show_retrieval else []

    print("Question:")
    print(args.question)
    if args.show_retrieval:
        print("\nRetrieved evidence:")
        if not retrieved:
            print("  None")
        for rank, item in enumerate(retrieved, start=1):
            print(f"  Rank: {rank}")
            print(f"    Chunk ID: {item.chunk.chunk_id}")
            print(f"    Score: {item.score:.4f}")
            print(f"    Source: {item.chunk.title} ({item.chunk.doc_id})")
            print(f"    Text: {item.chunk.text}")
    print("\nAnswer:")
    print(result.answer)
    print("\nCorpus profile:", args.corpus_profile)
    print("\nRefused:", result.refused)
    print("Citations:", ", ".join(result.citations) if result.citations else "None")


if __name__ == "__main__":
    main()
