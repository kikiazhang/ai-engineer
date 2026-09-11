from rag_service.rag import answer_question


def main() -> None:
    questions = [
        (
            "Can an employee receive a reassigned "
            "license before 90 days?"
        ),
        (
            "Does capacity validation automatically "
            "purchase more seats?"
        ),
        "Can a trial subscription be renewed?",
        (
            "What information should be recorded "
            "in a license audit log?"
        ),
        "What color is the CEO's car?",
        "What is the exact cancellation fee?",
        "Can I reassign a license after 30 days?",
    ]

    for question in questions:
        print("\n" + "=" * 80)
        print(f"Question: {question}")

        answer = answer_question(question)

        print(f"Answerable: {answer.answerable}")
        print(f"Answer: {answer.answer}")
        print(f"Citations: {answer.citation_ids}")


if __name__ == "__main__":
    main()