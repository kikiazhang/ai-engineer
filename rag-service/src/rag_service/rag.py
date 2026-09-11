import os
from dataclasses import dataclass

from google import genai
from pydantic import BaseModel, Field

from rag_service.retrieval import RetrievedChunk, retrieve_chunks

GENERATION_MODEL = os.getenv(
    "GENERATION_MODEL",
    "gemini-3.1-flash-lite",
)

class RagAnswer(BaseModel):
    answerable: bool = Field(
        description=(
            "True only when the provided sources contain "
            "enough information to answer the question."
        )
    )

    answer: str = Field(
        description=(
            "Answer based only on the provided sources."
        )
    )

    citation_ids: list[str] = Field(
        description=(
            "Exact SOURCE ids supporting the answer. "
            "Must only contain ids from the provided context."
        )
    )
    
@dataclass(frozen=True)
class RagResult:
    answer: RagAnswer
    retrieve_chunks: list[RetrievedChunk]

def build_context(
    chunks: list[RetrievedChunk],
) -> str:
    sources = []
    
    for chunk in chunks:
        source = (
            f'<SOURCE id="{chunk.chunk_id}" '
            f'document_id="{chunk.document_id}" '
            f'section_id="{chunk.section_id}">\n'
            f"Title: {chunk.title}\n"
            f"Section: {chunk.section_title}\n"
            f"{chunk.text}\n"
            "</SOURCE>"
        )
        sources.append(source)
        
    return "\n\n".join(sources)

def build_prompt(
    question: str,
    context: str,
) -> str:
    return f"""
You are an enterprise licensing policy assistant.

RULES:
- Answer only from the provided SOURCES.
- Do not use outside knowledge.
- Do not invent licensing rules.
- If the sources do not contain enough information,
  set answerable to false.
- citation_ids must contain only exact SOURCE ids
  from the provided SOURCES.
- Cite only sources that directly support the answer.
- Do not infer permissions, guarantees, or conclusions
  that are not explicitly supported by the sources.
- Distinguish necessary conditions from sufficient
  conditions. If a source says an action requires
  approval, do not assume that approval guarantees
  the action is permitted.
- When the sources are partially informative but do
  not fully support a yes/no conclusion, explain the
  known rule and explicitly state what the sources
  do not establish.

SOURCES:

{context}

QUESTION:

{question}

Determine whether the sources contain enough evidence.
If they do, answer the question and cite the supporting
sources.
""".strip()

def generate_answer(
    question: str,
    chunks: list[RetrievedChunk],
) -> RagAnswer:
    context = build_context(chunks)
    prompt = build_prompt(question, context)
    
    with genai.Client() as client:
        interaction = client.interactions.create(
            model=GENERATION_MODEL,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": RagAnswer.model_json_schema(),
            }
        )
        
    return RagAnswer.model_validate_json(
        interaction.output_text
    )

REFUSAL_MESSAGE = (
    "I don't have enough information in the provided "
    "sources to answer this question."
)

def validate_rag_answer(
    answer: RagAnswer,
    chunks: list[RetrievedChunk],
) -> RagAnswer:
    valid_source_ids = {
        chunk.chunk_id
        for chunk in chunks
    }
    invalid_ids = (
        set(answer.citation_ids)
        - valid_source_ids
    )
    
    if invalid_ids:
        raise ValueError(
            f"Model returned invalid citations: "
            f"{sorted(invalid_ids)}"
        )
        
    if answer.answerable and not answer.citation_ids:
        raise ValueError(
            "Answerable responses must include citation."
        )
        
    if not answer.answerable:
        return RagAnswer(
            answerable=False,
            answer=REFUSAL_MESSAGE,
            citation_ids=[],
        )
        
    return answer

def answer_question(
    question: str,
    top_k: int = 3,
) -> RagResult:
    chunks = retrieve_chunks(
        query=question,
        top_k=top_k,
    )
    answer = generate_answer(
        question=question,
        chunks=chunks,
    )
    validated_answer = validate_rag_answer(
        answer=answer,
        chunks=chunks,
    )
    return RagResult(
        answer=validated_answer,
        retrieve_chunks=chunks
    )