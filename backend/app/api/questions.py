
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.rag_service import answer_question

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/questions",
    tags=["questions"],
)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)
    document_id: int | None = Field(default=None, gt=0)
    limit: int = Field(default=5, ge=1, le=20)


@router.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        result = answer_question(
            question=request.question,
            document_id=request.document_id,
            limit=request.limit,
        )
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        logger.exception("RAG question answering failed")
        raise HTTPException(
            status_code=500,
            detail="Unable to answer the question.",
        )
