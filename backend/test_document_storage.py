
from app.services.embedding_service import generate_embeddings
from app.services.document_storage_service import save_document
from app.services.database_service import get_connection


chunks = [
    {
        "page_number": 1,
        "text": "Regression testing checks existing software functionality."
    },
    {
        "page_number": 2,
        "text": "Unit testing checks individual software components."
    }
]

# Generate embeddings locally
embeddings = generate_embeddings(
    [chunk["text"] for chunk in chunks]
)

# Save everything in PostgreSQL
document_id = save_document(
    filename="test_software_testing.pdf",
    chunks=chunks,
    embeddings=embeddings
)

print("Saved document ID:", document_id)

# Verify the saved data
with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT filename
            FROM documents
            WHERE id = %s
            """,
            (document_id,)
        )

        print("Filename:", cursor.fetchone()[0])

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM document_chunks
            WHERE document_id = %s
            """,
            (document_id,)
        )

        print("Stored chunks:", cursor.fetchone()[0])

print("Document storage test successful!")
