
from app.services.database_service import get_connection
from app.services.embedding_service import generate_embeddings


def search_documents(query: str, limit: int = 5, document_id: int | None = None):
    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not 1 <= limit <= 20:
        raise ValueError("Limit must be between 1 and 20.")

    # Convert the user's question into a 384-dimensional vector
    query_embedding = generate_embeddings([query])[0]

    vector_string = "[" + ",".join(
        str(float(value)) for value in query_embedding
    ) + "]"

    # Search stored embeddings using pgvector
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    dc.document_id,
                    d.filename,
                    dc.page_number,
                    dc.content,
                    1 - (dc.embedding <=> %s::vector) AS similarity
                FROM document_chunks dc
                JOIN documents d ON dc.document_id = d.id
                WHERE (%s::bigint IS NULL OR dc.document_id = %s::bigint)
                ORDER BY dc.embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    vector_string,
                    document_id,
                    document_id,
                    vector_string,
                    limit,
                ),
            )

            rows = cursor.fetchall()

    return [
        {
            "document_id": row[0],
            "filename": row[1],
            "page_number": row[2],
            "text": row[3],
            "similarity": round(float(row[4]), 4),
        }
        for row in rows
    ]
