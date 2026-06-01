from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field

from rag.rag_pipeline import ask_cricket_agent

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)
class QuestionRequest(BaseModel):
    question: str
    top_k: int = Field(
        default=3,
        ge=1,
        le=10
    )

@router.post("/ask")
def ask_question(request: QuestionRequest):

    try:

        result = result = ask_cricket_agent(
    request.question,
    request.top_k
)

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )