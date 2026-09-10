import pytest

from rag_service.search import cosine_similarity, search


def test_search_returns_most_similar_document():
    documents = [
        {"id": "A", "title": "A", "text": "A"},
        {"id": "B", "title": "B", "text": "B"},
    ]
    vectors = [[1.0, 0.0], [0.0, 1.0]]

    results = search(
        query_vector=[1.0, 0.0],
        documents=documents,
        document_vectors=vectors,
        top_k=1,
    )

    assert results[0].document_id == "A"


def test_cosine_similarity_same_direction():
    assert cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)


def test_cosine_similarity_orthogonal():
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)


def test_cosine_similarity_dimension_mismatch():
    with pytest.raises(ValueError):
        cosine_similarity([1, 0], [1, 0, 0])


def test_cosine_similarity_zero_vector():
    with pytest.raises(ValueError):
        cosine_similarity([0, 0], [1, 0])


def test_search_rejects_mismatched_lengths():
    documents = [
        {"id": "A", "title": "A", "text": "A"},
    ]

    with pytest.raises(ValueError):
        search(
            query_vector=[1.0, 0.0],
            documents=documents,
            document_vectors=[
                [1.0, 0.0],
                [0.0, 1.0],
            ],
        )
