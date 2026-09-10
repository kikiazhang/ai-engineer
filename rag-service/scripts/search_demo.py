import json
from pathlib import Path

from rag_service.embeddings import embed_text
from rag_service.search import search

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EMBEDDINGS_FILE = PROJECT_ROOT / "data" / "embeddings.json"
INDEX_FIXED_FILE = PROJECT_ROOT / "data" / "index_fixed.json"
INDEX_PARAGRAPH_FILE = PROJECT_ROOT / "data" / "index_paragraph.json"


def load_embeddings() -> list[dict]:
    with EMBEDDINGS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def load_index_fixed() -> list[dict]:
    with INDEX_FIXED_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def load_index_paragraph() -> list[dict]:
    with INDEX_PARAGRAPH_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def main():
    index = load_embeddings()

    documents = [
        {"id": item["id"], "title": item["title"], "text": item["text"]}
        for item in index
    ]

    document_vectors = [item["vector"] for item in index]

    query = "Can I transfer my license to another employee?"
    query_vector = embed_text(query, task_type="RETRIEVAL_QUERY")

    results = search(
        query_vector=query_vector,
        documents=documents,
        document_vectors=document_vectors,
        top_k=3,
    )

    for result in results:
        print(f"\nDocument: {result.document_id}")
        print(f"Title: {result.title}")
        print(f"Score: {result.score:.4f}")
        print(f"Text: {result.text}")


def main_with_adapter():
    querys = [
        "Can an employee receive a reassigned license before 90 days?",
        "Does capacity validation automatically purchase more seats?",
        "What information should be recorded in a license audit log?",
        "Can a trial subscription be renewed?",
    ]
    for query in querys:
        query_vector = embed_text(query, task_type="RETRIEVAL_QUERY")
        print(f"Query: {query}")

        index_fixed = load_index_fixed()

        documents_fixed = [
            {"id": item["chunk_id"], "title": item["title"], "text": item["text"]}
            for item in index_fixed
        ]

        document_fixed_vectors = [item["vector"] for item in index_fixed]
        fixed_results = search(
            query_vector=query_vector,
            documents=documents_fixed,
            document_vectors=document_fixed_vectors,
            top_k=3,
        )

        print("Fixed-size chunk search result:")
        fixed_by_chunk_id = {
            item["chunk_id"]: item
            for item in index_fixed
        }
        for rank, result in enumerate(fixed_results, start=1):
            index_item = fixed_by_chunk_id[result.document_id]
            print(f"\nRank: {rank}")
            print(f"Chunk id: {index_item['chunk_id']} ")
            print(f"Section id: {index_item['section_id']}")
            print(f"Document id: {index_item['document_id']}")
            print(f"Score: {result.score:.4f}")
            print(f"Text: {result.text}")

        # Now, let's search using the paragraph-based index
        index_paragraph = load_index_paragraph()

        documents_paragraph = [
            {"id": item["chunk_id"], "title": item["title"], "text": item["text"]}
            for item in index_paragraph
        ]

        document_paragraph_vectors = [item["vector"] for item in index_paragraph]
        paragraph_results = search(
            query_vector=query_vector,
            documents=documents_paragraph,
            document_vectors=document_paragraph_vectors,
            top_k=3,
        )

        print("Paragraph-based search result:")
        for rank, result in enumerate(paragraph_results, start=1):
            for index_item in index_paragraph:
                if index_item["chunk_id"] == result.document_id:
                    print(f"\nRank: {rank}")
                    print(f"Chunk id: {index_item['chunk_id']} ")
                    print(f"Section id: {index_item['section_id']}")
                    print(f"Document id: {index_item['document_id']}")
                    print(f"Score: {result.score:.4f}")
                    print(f"Text: {result.text}")


if __name__ == "__main__":
    main_with_adapter()
