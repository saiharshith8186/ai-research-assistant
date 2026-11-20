
from app.services.rag_service import answer_question

print("Testing the complete RAG pipeline...\n")

question = "What technical skills are mentioned in this candidate's resume?"

result = answer_question(
    question=question,
    document_id=3,
    limit=5,
)

print("QUESTION:")
print(result["question"])

print("\nAI GENERATED ANSWER:")
print(result["answer"])

print("\nSOURCES USED:")
for source in result["sources"]:
    print(
        f"Source {source['source_number']}: "
        f"{source['filename']} | "
        f"Page {source['page_number']} | "
        f"Similarity: {source['similarity']}"
    )
