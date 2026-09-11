import json
from pathlib import Path

from rag_service.rag import answer_question
from rag_service.retrieval import RetrievedChunk

EVAL_FILE = Path(__file__).parent / "rag_cases.json"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_FIXED_FILE = PROJECT_ROOT / "data" / "index_fixed.json"

def load_cases() -> list[dict]:
    with EVAL_FILE.open(encoding="utf-8") as file:
        return json.load(file)
    
def answerability_correct(
    actual: bool,
    expected: bool,
) -> bool:
    return actual == expected

def citations_are_valid(
    citation_ids: list[str],
    retrieved_chunk_ids: list[str],
) -> bool:
    retrieved_set = set(retrieved_chunk_ids)

    return all(
        citation_id in retrieved_set
        for citation_id in citation_ids
    )
    
def citations_cover_expected_documents(
    citation_ids: list[str],
    chunks: list[RetrievedChunk],
    expected_document_ids: list[str],
) -> bool:
    if not expected_document_ids:
        return not citation_ids

    chunk_by_id = {
        chunk.chunk_id: chunk
        for chunk in chunks
    }

    cited_document_ids = {
        chunk_by_id[citation_id].document_id
        for citation_id in citation_ids
        if citation_id in chunk_by_id
    }

    return (
        set(expected_document_ids)
        <= cited_document_ids
    )

def run_eval() -> None:
    cases = load_cases()
    
    answerability_pass_count = 0
    citation_valid_count = 0
    citation_coverage_count = 0
    manual_groundedness_count = 0

    groundedness_failures = []

    for case in cases:
        question = case["question"]
        
        rag_result = answer_question(
            question=question,
            top_k=3,
        )
        answer = rag_result.answer
        
        if answerability_correct(answer.answerable, case["expected_answerable"]):
            answerability_pass_count += 1
            
        answerability_pass = answerability_correct(
            answer.answerable,
            case["expected_answerable"],
        )
        
        retrieved_chunk_ids = [
            chunk.chunk_id
            for chunk in rag_result.retrieve_chunks
        ]
           
        citation_valid = citations_are_valid(
            answer.citation_ids,
            retrieved_chunk_ids,
        )

        citation_source_coverage = citations_cover_expected_documents(
            answer.citation_ids,
            rag_result.retrieve_chunks,
            case["expected_document_ids"],
        )
        if citation_valid:
            citation_valid_count += 1
        if citation_source_coverage:
            citation_coverage_count += 1
            
        print(f"\nCase: {case['id']}")
        print(f"Question: {case['question']}")
        print(
            f"Expected answerable: "
            f"{case['expected_answerable']}"
        )
        print(
            f"Actual answerable: "
            f"{answer.answerable}"
        )
        print(f"Answerability check: {'PASS' if answerability_pass else 'FAIL'}")
        print(
            f"Citation ID validity: "
            f"{'PASS' if citation_valid else 'FAIL'}"
        )

        print(
            f"Citation source coverage: "
            f"{'PASS' if citation_source_coverage else 'FAIL'}"
        )
        print(f"Answer: {answer.answer}")
        print(f"Citations: {answer.citation_ids}")
        print("Retrieved chunks:")

        for chunk in rag_result.retrieve_chunks:
            print(
                f"- {chunk.chunk_id} "
                f"| {chunk.section_id} "
                f"| {chunk.score:.4f}"
            )
    
        manual_groundedness = input("Manual groundedness: (y/n)").strip().lower()
        grounded = manual_groundedness in {
            "yes",
            "y",
            "true",
            "t",
            "1",
        }
        if grounded:
            manual_groundedness_count += 1
        else:
            groundedness_failures.append(case['id'])
            
    answerability_correct_rate = answerability_pass_count / len(cases)
    citation_validity_rate = citation_valid_count / len(cases)
    citation_source_coverage_rate = citation_coverage_count / len(cases)
    manual_groundedness_rate = manual_groundedness_count / len(cases)
    
    print("\n=== RAG Evaluation Summary === ")
    print(f"Cases: {len(cases)}")
    print(f"Answerability accuracy: "
          f"{answerability_pass_count} / {len(cases)}"
          f"({answerability_correct_rate: 0.1f})")
    print(f"Citation ID Validity: "
          f"{citation_valid_count} / {len(cases)}"
          f"({citation_validity_rate: 0.1f})")
    print("Citation Expected-Source Coverage: "
          f"{citation_coverage_count} / {len(cases)}"
          f"({citation_source_coverage_rate: 0.1f})")
    print(f"Manual Groundedness: "
        f"{manual_groundedness_count} / {len(cases)}"
        f"({manual_groundedness_rate: 0.1f})")
    print("Groundedness failures:")
    for groundedness_failure in groundedness_failures:
        print(f"- {groundedness_failure}")

if __name__ == "__main__":
    run_eval()  
            