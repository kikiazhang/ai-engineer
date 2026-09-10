import json
from pathlib import Path

from rag_service.embeddings import embed_text
from rag_service.search import recall_at_k, search

EVAL_FILE = Path(__file__).parent / "retrieval_cases.json"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
EMBEDDINGS_FILE = PROJECT_ROOT / "data" / "embeddings.json"


def load_cases() -> list[dict]:
    with EVAL_FILE.open() as file:
        return json.load(file)


def get_documents() -> tuple[list[dict], list[list[float]]]:
    with EMBEDDINGS_FILE.open(encoding="utf-8") as file:
        index = json.load(file)

        documents = [
            {"id": item["id"], "title": item["title"], "text": item["text"]}
            for item in index
        ]

        document_vectors = [item["vector"] for item in index]

    return documents, document_vectors


def run_eval() -> None:
    cases = load_cases()
    documents, document_vectors = get_documents()

    if not cases:
        raise ValueError("No evaluation cases found")

    recall_1_scores = []
    recall_3_scores = []

    for case in cases:
        query_vector = embed_text(case["query"], task_type="RETRIEVAL_QUERY")
        relevant_ids = case["relevant_document_ids"]
        results = search(
            query_vector=query_vector,
            documents=documents,
            document_vectors=document_vectors,
            top_k=3,
        )
        retrieved_ids = [result.document_id for result in results]

        recall_1 = recall_at_k(retrieved_ids, relevant_ids, 1)
        recall_3 = recall_at_k(retrieved_ids, relevant_ids, 3)

        recall_1_scores.append(recall_1)
        recall_3_scores.append(recall_3)

        print(f"\nCase: {case['id']}")
        print(f"Query: {case['query']}")
        print(f"Expected: {relevant_ids}")

        for rank, result in enumerate(results, start=1):
            print(
                f"  {rank}. {result.document_id} | {result.score:.4f} | {result.title}"
            )

        print(f"Recall@1: {recall_1:.4f}")
        print(f"Recall@3: {recall_3:.4f}")

    mean_recall_1 = sum(recall_1_scores) / len(cases)
    mean_recall_3 = sum(recall_3_scores) / len(cases)

    print("\n=== Evaluation Summary ===")
    print(f"Cases: {len(cases)}")
    print(f"Mean Recall@1: {mean_recall_1:.4f}")
    print(f"Mean Recall@3: {mean_recall_3:.4f}")


if __name__ == "__main__":
    run_eval()
