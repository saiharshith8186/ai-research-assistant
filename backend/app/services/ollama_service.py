
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
                    "role": "system",
                    "content": (
                        "You are an accurate AI Research Assistant. "
                        "Follow the user's task instructions carefully. "
                        "Use only information supported by the "
                        "provided document context. "
                        "Do not invent facts. "
                        "Distinguish programming languages, "
                        "frameworks, libraries, and runtimes correctly. "
                        "Cite relevant sources using [Source 1], "
                        "[Source 2], etc. "
                        "If information is unavailable, say so."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            options={
                "temperature": 0,
                "num_predict": 700,
            },
        )

        return response.message.content or ""

    except Exception:
        logger.exception("Ollama answer generation failed")
        raise
