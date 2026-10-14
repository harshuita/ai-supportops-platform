from app.rag.retrieval import search_documents

questions = [
    "How long do I have to ask for a refund?",
    "My package arrived broken. What should I do?",
    "How long does delivery take?"
]

for question in questions:
    print(f"\nQuestion: {question}")

    results = search_documents(question, top_k=2)

    for result in results:
        print(
            f"{result['source']} "
            f"(score: {result['score']:.3f})"
        )
        print(result["text"])