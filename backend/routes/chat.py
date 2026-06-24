from fastapi import APIRouter
from services.rag_service import chat_ai

router = APIRouter(prefix="/chat", tags=["Chat AI"])

@router.post("/")
def chat(data: dict):
    return chat_ai(data["message"])