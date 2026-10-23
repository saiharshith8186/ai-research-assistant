
from app.services.embedding_service import generate_embeddings
from app.services.search_service import semantic_search


chunks = [
    {
        "page_number": 1,
        "text": "Regression testing verifies that existing functionality still works after software changes.",
    },
    {
        "page_number": 2,
        "text": "Load testing evaluates system performance under heavy user traffic.",
    },
    {
        "page_number": 3,
        "text": "Unit testing checks individual functions or components.",
    },
    {
        "page_number": 4,
        "text": "Regression tests help detect bugs introduced by recent code modifications.",
    },
]

texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(texts)

results = semantic_search(
    query="How do developers make sure old features still work after updating code?",
    chunks=chunks,
    embeddings=embeddings,
    top_k=2,
)

for result in results:
    print(f"Page: {result['page_number']}")
    print(f"Score: {result['similarity_score']}")
    print(f"Text: {result['text']}")
    print("-" * 50)
