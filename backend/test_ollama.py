
from app.services.ollama_service import generate_answer

print("Testing Ollama with Qwen 2.5 3B...\n")

question = "Explain Retrieval-Augmented Generation in two sentences."

answer = generate_answer(question)

print("Question:", question)
print("\nAI Answer:")
print(answer)
