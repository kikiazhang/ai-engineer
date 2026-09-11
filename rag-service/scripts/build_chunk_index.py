import json
from pathlib import Path

from rag_service.chunking import Chunk, build_chunks
from rag_service.embedding_cache import (
    get_cached_embedding,
    load_embedding_cache,
    save_embedding_cache,
)
from rag_service.embeddings import (
    EMBEDDING_MODEL,
    embed_text,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LONG_POLICIES_FILE = PROJECT_ROOT / "data" / "long_policies.json"
INDEX_FIXED_FILE = PROJECT_ROOT / "data" / "index_fixed.json"
INDEX_PARAGRAPH_FILE = PROJECT_ROOT / "data" / "index_paragraph.json"
CACHE_FILE = PROJECT_ROOT / "data" / "embedding_cache.json"


def load_long_policies() -> list[dict]:
    with LONG_POLICIES_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def build_chunk_index(strategy: str, chunk_size: int, overlap: int = 0) -> list[Chunk]:
    """
    This method focus on load documents, chunk, embed, cache, create records, persist index.
    Chunk the input text into fixed-size spans with optional overlap.

    Args:
        strategy (str): The chunking strategy to use.
        chunk_size (int): The size of each chunk.
        overlap (int): The number of characters to overlap between chunks.

    Returns:
        list[tuple[int, int]]: A list of tuples representing the start and end indices of each chunk.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    if overlap < 0:
        raise ValueError("overlap must be a non-negative integer")
    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")

    documents = load_long_policies()

    chunks = build_chunks(
        documents, strategy=strategy, chunk_size=chunk_size, overlap=overlap
    )

    cache = load_embedding_cache(CACHE_FILE)

    cache_hits = 0
    cache_misses = 0

    records = []
    for chunk in chunks:
        vector, cache_hit = get_cached_embedding(
            text=f"{chunk.title}\n{chunk.section_title}\n{chunk.text}",
            model=EMBEDDING_MODEL,
            task_type="RETRIEVAL_DOCUMENT",
            cache=cache,
            embed_fn=embed_text,
        )

        if cache_hit:
            cache_hits += 1
        else:
            cache_misses += 1

        record = {
            "chunk_id": chunk.chunk_id,
            "document_id": chunk.document_id,
            "section_id": chunk.section_id,
            "title": chunk.title,
            "section_title": chunk.section_title,
            "text": chunk.text,
            "source": chunk.source,
            "version": chunk.version,
            "tenant_id": chunk.tenant_id,
            "start_char": chunk.start_char,
            "end_char": chunk.end_char,
            "vector": vector,
        }
        records.append(record)

    if strategy == "fixed":
        with INDEX_FIXED_FILE.open("w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)
    elif strategy == "paragraph":
        with INDEX_PARAGRAPH_FILE.open("w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)

    save_embedding_cache(cache_file=CACHE_FILE, cache=cache)
    print(f"Cache hits: {cache_hits}")
    print(f"Cache misses: {cache_misses}")

    return chunks


if __name__ == "__main__":
    build_chunk_index(
        strategy="fixed",
        chunk_size=240,
        overlap=40,
    )

    build_chunk_index(
        strategy="paragraph",
        chunk_size=240,
        overlap=0,
    )
