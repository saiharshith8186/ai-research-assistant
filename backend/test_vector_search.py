
from app.services.vector_search_service import search_documents

query = "What technical skills and programming languages does this candidate have?"

print(f"\nSearching for: {query}\n")

results = search_documents(
    query=query,
    limit=5,
    document_id=3
)

if not results:
    print("No matching document chunks found.")
else:
    for index, result in enumerate(results, start=1):
        print(f"Result {index}")
        print(f"Document: {result['filename']}")
        print(f"Page: {result['page_number']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Text: {result['text'][:400]}")
        print("-" * 60)
