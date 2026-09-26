from fastapi import APIRouter, HTTPException, status
from src.schemas.chat import (
    ChatRequest, 
    ChatResponse, 
    ConversationCreate, 
    ConversationResponse
)
from src.services.chat import chat_service

router = APIRouter(
    prefix="/chat",
    tags=["Chat & Prediction Engine"]
)

@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(payload: ConversationCreate):
    """API Tạo một cuộc hội thoại mới"""
    return await chat_service.create_conversation(payload)

@router.post("/message", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_message(payload: ChatRequest):
    """API Gửi tin nhắn và nhận phản hồi dự đoán"""
    if not payload.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nội dung tin nhắn không được để trống."
        )
    return await chat_service.process_chat(payload)