import pytest

from rag_service.search import recall_at_k


def test_recall_at_k_all_relevant_found():
    assert (
        recall_at_k(
            ["A", "B", "C"],
            ["A", "C"],
            3,
        )
        == 1.0
    )


def test_recall_at_k_partial_recall():
    assert (
        recall_at_k(
            ["A", "B", "C"],
            ["A", "C"],
            1,
        )
        == 0.5
    )


def test_recall_at_k_no_relevant_found():
    assert (
        recall_at_k(
            ["A", "B"],
            ["C"],
            2,
        )
        == 0.0
    )


def test_recall_at_k_does_not_double_count_duplicates():
    assert (
        recall_at_k(
            ["A", "A", "B"],
            ["A", "C"],
            3,
        )
        == 0.5
    )


def test_recall_at_k_rejects_invalid_k():
    with pytest.raises(ValueError):
        recall_at_k(["A"], ["A"], 0)


def test_recall_at_k_rejects_empty_ground_truth():
    with pytest.raises(ValueError):
        recall_at_k(["A"], [], 1)
