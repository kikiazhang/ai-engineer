import json
from dataclasses import dataclass
from pathlib import Path

from rag_service.embedding_cache import (
    get_cached_embedding,
    load_embedding_cache,
    save_embedding_cache,
)
from rag_service.embeddings import EMBEDDING_MODEL, embed_text
from rag_service.search import search

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INDEX_FILE = PROJECT_ROOT / "data" / "index_fixed.json"
CACHE_FILE = PROJECT_ROOT / "data" / "embedding_cache.json"


# query time retrieval result
@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    document_id: str
    section_id: str
    title: str
    section_title: str
    text: str
    source: str
    score: float


def load_index(
    index_file: Path = INDEX_FILE,
) -> list[dict]:
    with index_file.open(encoding="utf-8") as file:
        return json.load(file)


def retrieve_chunks(
    query: str,
    top_k: int = 3,
    index_file: Path = INDEX_FILE,
) -> list[RetrievedChunk]:

    index = load_index()

    documents_fixed = [
        {
            "id": item["chunk_id"],
            "title": item["title"],
            "text": item["text"],
        }
        for item in index
    ]
    document_vectors = [item["vector"] for item in index]
    by_chunk_id = {item["chunk_id"]: item for item in index}
    cache = load_embedding_cache(CACHE_FILE)

    query_vector, _ = get_cached_embedding(
        text=query,
        model=EMBEDDING_MODEL,
        task_type="RETRIEVAL_QUERY",
        cache=cache,
        embed_fn=embed_text,
    )

    results = search(
        query_vector=query_vector,
        documents=documents_fixed,
        document_vectors=document_vectors,
        top_k=top_k,
    )

    save_embedding_cache(
        CACHE_FILE,
        cache,
    )

    retrieved = []

    for result in results:
        item = by_chunk_id[result.document_id]

        retrieved.append(
            RetrievedChunk(
                chunk_id=item["chunk_id"],
                document_id=item["document_id"],
                section_id=item["section_id"],
                title=item["title"],
                section_title=item["section_title"],
                text=item["text"],
                source=item["source"],
                score=result.score,
            )
        )

    return retrieved
