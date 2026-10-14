import argparse
import sys
from typing import Optional, Sequence

from .chunking import build_chunks
from .corpus import list_corpus_profiles, load_corpus
from .rag import build_grounded_answer
from .retrieval import retrieve_top_k


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Week 6 RAG homework starter")
    parser.add_argument("--question", required=True, help="Question to ask over the local corpus")
    parser.add_argument("--chunk-size", type=int, default=None, help="Chunk size in characters")
    parser.add_argument("--overlap", type=int, default=None, help="Chunk overlap in characters")
    parser.add_argument("--top-k", type=int, default=None, help="Number of retrieved chunks")
    parser.add_argument(
        "--corpus-profile", default=None, choices=list_corpus_profiles(),
        help="Corpus profile: default or training-rag",
    )
    parser.add_argument("--corpus-file", help="Path to the verified local English Prince source")
    parser.add_argument("--show-retrieval", action="store_true", help="Show ranked retrieval evidence before the answer")
    return parser


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.corpus_file is not None and args.corpus_profile is not None:
        parser.error("--corpus-profile and --corpus-file cannot be selected together")
    return args


def _print_legacy(args: argparse.Namespace) -> int:
    profile = args.corpus_profile if args.corpus_profile is not None else "default"
    chunk_size = args.chunk_size if args.chunk_size is not None else 140
    overlap = args.overlap if args.overlap is not None else 30
    top_k = args.top_k if args.top_k is not None else 2
    corpus = load_corpus(profile)
    chunks = build_chunks(corpus, chunk_size=chunk_size, overlap=overlap)
    result = build_grounded_answer(args.question, chunks, top_k=top_k)
    retrieved = retrieve_top_k(args.question, chunks, k=top_k) if args.show_retrieval else []

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
    print("\nCorpus profile:", profile)
    print("\nRefused:", result.refused)
    print("Citations:", ", ".join(result.citations) if result.citations else "None")
    return 0


def _print_book(args: argparse.Namespace) -> int:
    from .book_corpus import BookInputError, load_book_corpus
    from .book_rag import build_book_answer
    from .book_retrieval import BookConfigurationError, build_book_chunks, build_book_index

    chunk_size = args.chunk_size if args.chunk_size is not None else 800
    overlap = args.overlap if args.overlap is not None else 120
    top_k = args.top_k if args.top_k is not None else 2
    if chunk_size <= 0:
        raise BookConfigurationError("chunk_size must be > 0")
    if overlap < 0:
        raise BookConfigurationError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise BookConfigurationError("overlap must be smaller than chunk_size")
    if top_k <= 0:
        raise BookConfigurationError("top_k must be > 0")

    book = load_book_corpus(args.corpus_file)
    chunks = build_book_chunks(book, chunk_size=chunk_size, overlap=overlap)
    index = build_book_index(chunks)
    result = build_book_answer(args.question, book, index, top_k=top_k)

    print("Question:")
    print(args.question)
    print("\nCorpus profile: prince-book")
    print("Source: %s (translator: %s)" % (result.source_title, result.translator))
    print("Source SHA-256: %s" % result.source_sha256)
    print("Body SHA-256: %s" % result.body_sha256)
    print("Parser version: %s" % result.parser_version)
    print("Token policy: %s" % result.token_policy_version)
    print("Admission policy: %s" % result.admission_policy_version)
    print("Chunk size: %d" % result.chunk_size)
    print("Overlap: %d" % result.overlap)
    print("Top-k: %d" % result.top_k)
    print("BM25 k1/b: %.2f/%.2f" % (result.bm25_k1, result.bm25_b))

    if args.show_retrieval:
        print("\nRaw ranked candidates:")
        raw_candidates = result.ranked_candidates[:top_k]
        if not raw_candidates:
            print("  None")
        for item in raw_candidates:
            chunk = item.chunk
            print("  Rank: %d" % item.rank)
            print("    Chunk ID: %s" % chunk.chunk_id)
            print("    BM25 score: %.8f" % item.score)
            print("    Section: %s (%s)" % (chunk.section_id, chunk.kind))
            print("    Heading: %s" % chunk.heading)
            print("    Source offsets: [%d, %d)" % (chunk.start_char, chunk.end_char))
            print("    Text: %s" % chunk.text)
        print("\nAccepted answer evidence:")
        if not result.accepted_excerpts:
            print("  None")
        for excerpt in result.accepted_excerpts[:top_k]:
            print("  Excerpt ID: %s" % excerpt.excerpt_id)
            print("    Origin chunk ID: %s" % excerpt.origin_chunk_id)
            print("    Origin BM25 score: %.8f" % excerpt.origin_score)
            print("    Admission policy: %s" % excerpt.admission_policy_version)
            print("    Source offsets: [%d, %d)" % (excerpt.start_char, excerpt.end_char))
            print("    Text: %s" % excerpt.text)

    print("\nAnswer:")
    print(result.answer)
    if result.refusal_reason:
        print("Refusal reason:", result.refusal_reason)
    print("\nRefused:", result.refused)
    print("Citations:", ", ".join(result.citations) if result.citations else "None")
    if result.accepted_excerpts:
        print("\nReferences:")
        for excerpt in result.accepted_excerpts:
            print("  Excerpt ID: %s" % excerpt.excerpt_id)
            print("    Section: %s (%s)" % (excerpt.section_id, excerpt.kind))
            print("    Heading: %s" % excerpt.heading)
            print("    Source offsets: [%d, %d)" % (excerpt.start_char, excerpt.end_char))
            print("    Origin chunk ID: %s" % excerpt.origin_chunk_id)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    if args.corpus_file is None:
        return _print_legacy(args)
    from .book_corpus import BookInputError
    from .book_retrieval import BookConfigurationError
    try:
        return _print_book(args)
    except (BookInputError, BookConfigurationError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
