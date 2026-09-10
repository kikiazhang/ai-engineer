import pytest

from rag_service.chunking import build_chunks, fixed_size_spans, paragraph_spans
from rag_service.embedding_cache import get_cached_embedding


def test_fixed_size_spans_with_overlap():
    spans = fixed_size_spans(
        "ABCDEFGHIJ",
        chunk_size=4,
        overlap=1,
    )

    assert spans == [(0, 4), (3, 7), (6, 10)]


def test_fixed_size_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        fixed_size_spans(
            "hello",
            chunk_size=4,
            overlap=4,
        )


def test_empty_text_returns_no_chunks():
    assert fixed_size_spans("", 100) == []
    assert paragraph_spans("", 100) == []


text = "First paragraph.\n\nSecond paragraph."


def test_paragraph_spans_within_chunk_size():
    spans = paragraph_spans(text, chunk_size=100)
    assert spans == [(0, 35)]


def test_paragraph_spans_exceeding_chunk_size():
    spans = paragraph_spans(text, chunk_size=10)
    assert spans == [(0, 10), (10, 16), (18, 28), (28, 35)]


document = [
    {
        "text": text,
        "document_id": "GUIDE-001",
        "title": "Enterprise License Administration Guide",
        "source": "fictional://licensing/admin-guide",
        "version": "1.0",
        "tenant_id": "demo",
        "sections": [
            {
                "section_id": "reassignment",
                "title": "Employee Reassignment",
                "text": "First paragraph.\n\nSecond paragraph.",
            }
        ],
    }
]


def test_build_chunks_with_paragraph_strategy():
    chunks = build_chunks(document, strategy="paragraph", chunk_size=20)
    assert len(chunks) == 2
    assert chunks[0].text == "First paragraph."
    assert chunks[1].text == "Second paragraph."


def test_build_chunks_with_fixed_strategy():
    chunks = build_chunks(document, strategy="fixed", chunk_size=15, overlap=0)
    assert len(chunks) == 3
    assert chunks[0].text == "First paragraph"
    assert chunks[1].text == ".\n\nSecond parag"
    assert chunks[2].text == "raph."


def test_build_chunks_rejects_invalid_strategy():
    with pytest.raises(ValueError):
        build_chunks(document, strategy="invalid", chunk_size=10)


def test_build_chunks_return_same_results_every_time():
    chunks1 = build_chunks(document, strategy="fixed", chunk_size=4, overlap=1)
    chunks2 = build_chunks(document, strategy="fixed", chunk_size=4, overlap=1)
    assert [c.chunk_id for c in chunks1] == [c.chunk_id for c in chunks2]


def test_build_chunks_with_metadata():
    chunks = build_chunks(document, strategy="fixed", chunk_size=5)
    assert all(chunk.document_id == "GUIDE-001" for chunk in chunks)
    assert all(
        chunk.title == "Enterprise License Administration Guide" for chunk in chunks
    )
    
def test_embedding_cache_reuses_existing_vector():
    calls = 0

    def fake_embed(
        text: str,
        task_type: str,
    ) -> list[float]:
        nonlocal calls
        calls += 1
        return [1.0, 2.0]

    cache = {}

    first, first_hit = get_cached_embedding(
        text="hello",
        model="test-model",
        task_type="RETRIEVAL_DOCUMENT",
        cache=cache,
        embed_fn=fake_embed,
    )

    second, second_hit = get_cached_embedding(
        text="hello",
        model="test-model",
        task_type="RETRIEVAL_DOCUMENT",
        cache=cache,
        embed_fn=fake_embed,
    )

    assert first == second
    assert first_hit is False
    assert second_hit is True
    assert calls == 1
    
def test_embedding_cache_change_text():
    calls = 0
    
    def fake_embed(
        text: str,
        task_type: str,
    ) -> list[float]:
        nonlocal calls
        calls += 1
        return [float(calls), 2.0]

    cache = {}

    first, first_hit = get_cached_embedding(
        text="hello",
        model="test-model",
        task_type="RETRIEVAL_DOCUMENT",
        cache=cache,
        embed_fn=fake_embed,
    )

    second, second_hit = get_cached_embedding(
        text="hello Anna",
        model="test-model",
        task_type="RETRIEVAL_DOCUMENT",
        cache=cache,
        embed_fn=fake_embed,
    )

    assert first != second
    assert first_hit is False
    assert second_hit is False
    assert calls == 2
    
def test_embedding_cache_change_model():
    calls = 0
    
    def fake_embed(
        text: str,
        task_type: str,
    ) -> list[float]:
        nonlocal calls
        calls += 1
        return [float(calls), 2.0]

    cache = {}

    first, first_hit = get_cached_embedding(
        text="hello",
        model="test-model",
        task_type="RETRIEVAL_DOCUMENT",
        cache=cache,
        embed_fn=fake_embed,
    )

    second, second_hit = get_cached_embedding(
        text="hello",
        model="test-model-2",
        task_type="RETRIEVAL_DOCUMENT",
        cache=cache,
        embed_fn=fake_embed,
    )

    assert first != second
    assert first_hit is False
    assert second_hit is False
    assert calls == 2
    
def test_embedding_cache_change_task():
    calls = 0
    
    def fake_embed(
        text: str,
        task_type: str,
    ) -> list[float]:
        nonlocal calls
        calls += 1
        return [float(calls), 2.0]

    cache = {}

    first, first_hit = get_cached_embedding(
        text="hello",
        model="test-model",
        task_type="RETRIEVAL_DOCUMENT",
        cache=cache,
        embed_fn=fake_embed,
    )

    second, second_hit = get_cached_embedding(
        text="hello",
        model="test-model",
        task_type="RETRIEVAL_QUERY",
        cache=cache,
        embed_fn=fake_embed,
    )

    assert first != second
    assert first_hit is False
    assert second_hit is False
    assert calls == 2
