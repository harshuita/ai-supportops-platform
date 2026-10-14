from pathlib import Path

import ollama

import math
DOCUMENTS_DIR = Path(__file__).parent / "documents"
EMBEDDING_MODEL = "nomic-embed-text"


def load_documents() -> list[dict]:
    documents = []

    for path in DOCUMENTS_DIR.glob("*.txt"):
        text = path.read_text(encoding="utf-8").strip()

        if text:
            documents.append({
                "source": path.name,
                "text": text
            })

    return documents


def embed_text(text: str) -> list[float]:
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response["embeddings"][0]



def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float]
) -> float:
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_documents(
    query: str,
    top_k: int = 2
) -> list[dict]:
    documents = load_documents()

    if not documents:
        return []

    query_embedding = embed_text(query)
    results = []

    for document in documents:
        document_embedding = embed_text(document["text"])

        score = cosine_similarity(
            query_embedding,
            document_embedding
        )

        results.append({
            "source": document["source"],
            "text": document["text"],
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]
