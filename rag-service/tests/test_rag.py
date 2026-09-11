import pytest

from rag_service.rag import (
    RagAnswer,
    build_context,
    validate_rag_answer,
)
from rag_service.retrieval import RetrievedChunk

# context 包含 source ID
def make_chunk() -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id="CHUNK-001",
        document_id="DOC-001",
        section_id="SECTION-001",
        title="Test Guide",
        section_title="Test Section",
        text="Licenses may be reassigned after 90 days.",
        source="fictional://test",
        score=0.9,
    )


def test_build_context_contains_source_id():
    context = build_context([make_chunk()])

    assert 'id="CHUNK-001"' in context
    assert "Licenses may be reassigned" in context
  
# valid citation  
def test_validate_rag_answer_accepts_valid_citation():
    chunk = make_chunk()

    answer = RagAnswer(
        answerable=True,
        answer="The license may be reassigned.",
        citation_ids=["CHUNK-001"],
    )

    validated = validate_rag_answer(
        answer,
        [chunk],
    )

    assert validated == answer

# hallucinated citation
def test_validate_rag_answer_rejects_invalid_citation():
    chunk = make_chunk()

    answer = RagAnswer(
        answerable=True,
        answer="The license may be reassigned.",
        citation_ids=["FAKE-999"],
    )

    with pytest.raises(
        ValueError,
        match="invalid citations",
    ):
        validate_rag_answer(
            answer,
            [chunk],
        )

# answer 没 citation        
def test_answerable_response_requires_citation():
    chunk = make_chunk()

    answer = RagAnswer(
        answerable=True,
        answer="The license may be reassigned.",
        citation_ids=[],
    )

    with pytest.raises(ValueError):
        validate_rag_answer(
            answer,
            [chunk],
        )
        
# refusal 被 normalize
def test_unanswerable_response_is_normalized():
    chunk = make_chunk()

    answer = RagAnswer(
        answerable=False,
        answer="Maybe I don't know.",
        citation_ids=["CHUNK-001"],
    )

    validated = validate_rag_answer(
        answer,
        [chunk],
    )

    assert validated.answerable is False
    assert validated.citation_ids == []