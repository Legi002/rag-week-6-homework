from dataclasses import dataclass
import re

from .chunking import Chunk


TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any",
    "are", "as", "at", "be", "because", "been", "before", "being", "below", "between",
    "both", "but", "by", "can", "could", "did", "do", "does", "doing", "down", "during",
    "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "her",
    "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into",
    "is", "it", "its", "itself", "just", "me", "more", "most", "my", "myself", "no", "nor",
    "not", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves",
    "out", "over", "own", "same", "she", "should", "so", "some", "such", "than", "that",
    "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "were",
    "what", "when", "where", "which", "while", "who", "whom", "why", "with", "would", "you",
    "your", "yours", "yourself", "yourselves",
}
DEFAULT_MIN_SCORE = 0.5


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    score: float


def lexical_score(query: str, chunk_text: str) -> float:
    q_tokens = [token for token in tokenize(query) if token not in STOP_WORDS]
    c_tokens = tokenize(chunk_text)
    if not q_tokens or not c_tokens:
        return 0.0

    q_set = set(q_tokens)
    c_set = set(c_tokens)
    return len(q_set & c_set) / len(q_set)


def retrieve_top_k(
    query: str,
    chunks: list[Chunk],
    k: int = 3,
    min_score: float = DEFAULT_MIN_SCORE,
) -> list[RetrievalResult]:
    if k <= 0:
        raise ValueError("k must be > 0")

    scored = [
        RetrievalResult(chunk=chunk, score=lexical_score(query, chunk.text))
        for chunk in chunks
    ]
    filtered = [item for item in scored if item.score >= min_score]
    filtered.sort(key=lambda item: item.score, reverse=True)
    return filtered[:k]
