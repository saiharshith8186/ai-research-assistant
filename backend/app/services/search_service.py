
import numpy as np

from app.services.embedding_service import generate_embeddings


def semantic_search(
    query: str,
    chunks: list[dict],
    embeddings: list[list[float]],
    top_k: int = 5,
) -> list[dict]:

    if not query.strip() or not chunks or not embeddings:
        return []

    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings must have the same length.")

    # Convert the user's question into an embedding
    query_embedding = np.array(
        generate_embeddings([query])[0],
        dtype=np.float32,
    )

    document_embeddings = np.array(
        embeddings,
        dtype=np.float32,
    )

    # Embeddings are already normalized.
    # Dot product therefore gives cosine similarity.
    similarity_scores = document_embeddings @ query_embedding

    # Find the highest-scoring chunks
    top_indices = np.argsort(similarity_scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        index = int(index)

        results.append({
            "page_number": chunks[index]["page_number"],
            "text": chunks[index]["text"],
            "similarity_score": round(
                float(similarity_scores[index]), 4
            ),
        })

    return results
