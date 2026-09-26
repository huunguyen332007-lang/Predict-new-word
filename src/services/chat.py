from datetime import datetime, timezone
from src.schemas.chat import (
    ChatRequest, 
    ChatResponse, 
    MessageResponse, 
    ConversationCreate, 
    ConversationResponse
)
from src.services.predictor import predictor_service

class ChatService:
    async def create_conversation(self, payload: ConversationCreate) -> ConversationResponse:
        """Tạo cuộc trò chuyện mới"""
        # TODO: Lưu conversation vào Database thông qua SQLAlchemy AsyncSession
        return ConversationResponse(
            id=101,
            title=payload.title
        )

    async def process_chat(self, payload: ChatRequest) -> ChatResponse:
        """Xử lý tin nhắn chat từ người dùng và sinh câu trả lời"""
        now = datetime.now(timezone.utc)

        # 1. Tạo object đại diện tin nhắn người dùng gửi
        user_msg = MessageResponse(
            id=1,
            role="user",
            content=payload.content,
            conversation_id=payload.conversation_id,
            created_at=now
        )

        # 2. Gọi Predictor hoặc LLM Engine để lấy phản hồi
        predicted_word, confidence = predictor_service.predict(payload.content)
        bot_content = f"Từ tiếp theo dự đoán: '{predicted_word}' (Độ tin cậy: {confidence:.2f})"

        # 3. Tạo object đại diện tin nhắn phản hồi từ Assistant
        assistant_msg = MessageResponse(
            id=2,
            role="assistant",
            content=bot_content,
            conversation_id=payload.conversation_id,
            created_at=datetime.now(timezone.utc)
        )

        # TODO: Lưu cả 2 messages vào Database

        return ChatResponse(
            user_message=user_msg,
            assistant_message=assistant_msg
        )

chat_service = ChatService()