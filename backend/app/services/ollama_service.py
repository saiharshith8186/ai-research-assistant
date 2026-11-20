
import logging
from ollama import chat

logger = logging.getLogger(__name__)

MODEL_NAME = "qwen2.5:3b"


def generate_answer(prompt: str) -> str:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        response = chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": 0.2,
                "num_predict": 300,
            },
        )

        return response.message.content

    except Exception:
        logger.exception("Ollama answer generation failed")
        raise
