import json
from pathlib import Path

from rag_service.embedding_cache import (
    get_cached_embedding,
    load_embedding_cache,
    save_embedding_cache,
)
from rag_service.embeddings import (
    EMBEDDING_MODEL,
    embed_text,
)
from rag_service.search import recall_at_k, search

EVAL_FILE = Path(__file__).parent / "retrieval_cases_multiple_levels.json"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_FIXED_FILE = PROJECT_ROOT / "data" / "index_fixed.json"
INDEX_PARAGRAPH_FILE = PROJECT_ROOT / "data" / "index_paragraph.json"
CACHE_FILE = PROJECT_ROOT/ "data" / "embedding_cache.json"

def load_cases() -> list[dict]:
    with EVAL_FILE.open() as file:
        return json.load(file)


def load_index_fixed() -> list[dict]:
    with INDEX_FIXED_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def load_index_paragraph() -> list[dict]:
    with INDEX_PARAGRAPH_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def run_eval() -> None:
    cases = load_cases()
    fixed_recall_1_scores = []
    fixed_recall_3_scores = []
    paragraph_recall_1_scores = []
    paragraph_recall_3_scores = []
    fixed_section_recall_1_scores = []
    fixed_section_recall_3_scores = []
    paragraph_section_recall_1_scores = []
    paragraph_section_recall_3_scores = []
    
    cache = load_embedding_cache(CACHE_FILE)

    for case in cases:
        query = case["query"]
        relevant_ids = case["relevant_document_ids"]
        relevant_section_ids = case["relevant_section_ids"]
        query_vector, _ = get_cached_embedding(
            text=query,
            model=EMBEDDING_MODEL,
            task_type="RETRIEVAL_QUERY",
            cache=cache,
            embed_fn=embed_text,
        )
        
        print(f"\nCase: {case['id']}")
        print(f"Query: {case['query']}")
        print(f"Expected: {relevant_ids}")

        index_fixed = load_index_fixed()

        documents_fixed = [
            {"id": item["chunk_id"], "title": item["title"], "text": item["text"]}
            for item in index_fixed
        ]
        fixed_by_chunk_id = {
            item["chunk_id"]: item
            for item in index_fixed
        }

        document_fixed_vectors = [item["vector"] for item in index_fixed]
        fixed_results = search(
            query_vector=query_vector,
            documents=documents_fixed,
            document_vectors=document_fixed_vectors,
            top_k=3,
        )

        retrieved_document_ids = [
            fixed_by_chunk_id[result.document_id]["document_id"]
            for result in fixed_results
        ]
        retrieved_section_ids = [
            fixed_by_chunk_id[result.document_id]["section_id"]
            for result in fixed_results
        ]

        recall_1 = recall_at_k(retrieved_document_ids, relevant_ids, 1)
        recall_3 = recall_at_k(retrieved_document_ids, relevant_ids, 3)
        section_recall_1 = recall_at_k(retrieved_section_ids, relevant_section_ids, 1)
        section_recall_3 = recall_at_k(retrieved_section_ids, relevant_section_ids, 3)

        fixed_recall_1_scores.append(recall_1)
        fixed_recall_3_scores.append(recall_3)
        fixed_section_recall_1_scores.append(section_recall_1)
        fixed_section_recall_3_scores.append(section_recall_3)

        print("Fixed-size chunk search result:")
        for rank, result in enumerate(fixed_results, start=1):
            print(
                f"  {rank}. {result.document_id} | {result.score:.4f} | {result.title}"
            )

        print(f"Recall@1: {recall_1:.4f}")
        print(f"Recall@3: {recall_3:.4f}")

        # Now, let's search using the paragraph-based index
        index_paragraph = load_index_paragraph()

        documents_paragraph = [
            {"id": item["chunk_id"], "title": item["title"], "text": item["text"]}
            for item in index_paragraph
        ]
        fixed_by_chunk_id = {
            item["chunk_id"]: item
            for item in index_paragraph
        }

        document_paragraph_vectors = [item["vector"] for item in index_paragraph]
        paragraph_results = search(
            query_vector=query_vector,
            documents=documents_paragraph,
            document_vectors=document_paragraph_vectors,
            top_k=3,
        )

        retrieved_document_ids = [
            fixed_by_chunk_id[result.document_id]["document_id"]
            for result in paragraph_results
        ]
        retrieved_section_ids = [
            fixed_by_chunk_id[result.document_id]["section_id"]
            for result in paragraph_results
        ]

        recall_1 = recall_at_k(retrieved_document_ids, relevant_ids, 1)
        recall_3 = recall_at_k(retrieved_document_ids, relevant_ids, 3)
        section_recall_1 = recall_at_k(retrieved_section_ids, relevant_section_ids, 1)
        section_recall_3 = recall_at_k(retrieved_section_ids, relevant_section_ids, 3)

        paragraph_recall_1_scores.append(recall_1)
        paragraph_recall_3_scores.append(recall_3)
        paragraph_section_recall_1_scores.append(section_recall_1)
        paragraph_section_recall_3_scores.append(section_recall_3)

        print("Paragraph-based search result:")
        for rank, result in enumerate(paragraph_results, start=1):
            print(
                f"  {rank}. {result.document_id} | {result.score:.4f} | {result.title}"
            )

        print(f"Recall@1: {recall_1:.4f}")
        print(f"Recall@3: {recall_3:.4f}")

    mean_fixed_recall_1 = sum(fixed_recall_1_scores) / len(cases)
    mean_fixed_recall_3 = sum(fixed_recall_3_scores) / len(cases)
    mean_paragraph_recall_1 = sum(paragraph_recall_1_scores) / len(cases)
    mean_paragraph_recall_3 = sum(paragraph_recall_3_scores) / len(cases)
    
    mean_section_fixed_recall_1 = sum(fixed_section_recall_1_scores) / len(cases)
    mean_section_fixed_recall_3 = sum(fixed_section_recall_3_scores) / len(cases)
    mean_section_paragraph_recall_1 = sum(paragraph_section_recall_1_scores) / len(cases)
    mean_section_paragraph_recall_3 = sum(paragraph_section_recall_3_scores) / len(cases)

    print("\n=== Evaluation Summary ===")
    print(f"Cases: {len(cases)}")
    print(f"Mean Recall@1 (Fixed): {mean_fixed_recall_1:.4f}")
    print(f"Mean Recall@3 (Fixed): {mean_fixed_recall_3:.4f}")
    print(f"Mean Recall@1 (Paragraph): {mean_paragraph_recall_1:.4f}")
    print(f"Mean Recall@3 (Paragraph): {mean_paragraph_recall_3:.4f}")
    
    print(f"Mean Recall by section@1 (Fixed): {mean_section_fixed_recall_1:.4f}")
    print(f"Mean Recall by section@3 (Fixed): {mean_section_fixed_recall_3:.4f}")
    print(f"Mean Recall by section@1 (Paragraph): {mean_section_paragraph_recall_1:.4f}")
    print(f"Mean Recall by section@3 (Paragraph): {mean_section_paragraph_recall_3:.4f}")
    
    save_embedding_cache(cache_file=CACHE_FILE, cache=cache)


if __name__ == "__main__":
    run_eval()
