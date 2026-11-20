
from app.services.database_service import get_connection


def save_document(filename, chunks, embeddings):
    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    if not chunks:
        raise ValueError("Cannot save a document without chunks.")

    with get_connection() as connection:
        with connection.cursor() as cursor:

            # Save document information
            cursor.execute(
                """
                INSERT INTO documents (filename)
                VALUES (%s)
                RETURNING id
                """,
                (filename,)
            )

            document_id = cursor.fetchone()[0]

            # Save chunks and embeddings
            for index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
            ):
                vector_string = "[" + ",".join(
                    str(float(value)) for value in embedding
                ) + "]"

                cursor.execute(
                    """
                    INSERT INTO document_chunks
                    (document_id, page_number,
                     chunk_index, content, embedding)
                    VALUES (%s, %s, %s, %s, %s::vector)
                    """,
                    (
                        document_id,
                        chunk["page_number"],
                        index,
                        chunk["text"],
                        vector_string
                    )
                )

        connection.commit()

    return document_id
