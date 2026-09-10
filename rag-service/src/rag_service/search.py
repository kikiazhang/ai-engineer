import math
from dataclasses import dataclass


@dataclass
class SearchResult:
    document_id: str
    title: str
    text: str
    score: float


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must be the same length")

    if not a:
        raise ValueError("Vectors must not be empty")

    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors must not be zero vectors")

    return dot_product / (norm_a * norm_b)


def recall_at_k(retrieved_ids: list[str], relevant_ids: list[str], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be a positive integer")

    relevant_set = set(relevant_ids)

    if not relevant_set:
        raise ValueError("relevant_ids must not be empty")

    retrieved_set = set(retrieved_ids[:k])
    relevant_retrieved = retrieved_set & relevant_set

    return len(relevant_retrieved) / len(relevant_set)


def search(
    query_vector: list[float],
    documents: list[dict],
    document_vectors: list[list[float]],
    top_k: int = 5,
) -> list[SearchResult]:
    if top_k <= 0:
        raise ValueError("top_k must be a positive integer")

    if len(documents) != len(document_vectors):
        raise ValueError("Documents and document_vectors must have the same length")

    scored_results = []
    for i, vector in enumerate(document_vectors):
        score = cosine_similarity(query_vector, vector)
        doc = documents[i]
        scored_results.append(
            SearchResult(
                document_id=doc["id"], title=doc["title"], text=doc["text"], score=score
            )
        )

    scored_results.sort(key=lambda x: x.score, reverse=True)
    return scored_results[:top_k]


if __name__ == "__main__":
    vector_a = [1, 0]
    vector_b = [1, 0]
    similarity = cosine_similarity(vector_a, vector_b)
    print(f"Cosine similarity: {similarity}")

    vector_c = [1, 0]
    vector_d = [0, 1]
    similarity = cosine_similarity(vector_c, vector_d)
    print(f"Cosine similarity: {similarity}")

    vector_e = [1, 0]
    vector_f = [-1, 0]
    similarity = cosine_similarity(vector_e, vector_f)
    print(f"Cosine similarity: {similarity}")
