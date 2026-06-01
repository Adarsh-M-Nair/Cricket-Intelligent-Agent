from fastapi import APIRouter
from pydantic import BaseModel

from rag.rag_pipeline import ask_cricket_agent

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: QuestionRequest):

    result = ask_cricket_agent(
        request.question
    )

    return result