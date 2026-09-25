"""
Database connection and session management.

Dùng SQLAlchemy 2.0 (Async) kết hợp với driver `asyncpg`
để đạt hiệu năng I/O tối đa cho các ứng dụng AI/LLM.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import settings

# 1. Khởi tạo Async Engine
# Echo=True để log SQL query khi debug (nên tắt trên Production)
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,  # Dạng: postgresql+asyncpg://user:pass@localhost:5432/dbname
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Tự động kiểm tra connection sống/chết trước khi dùng
)

# 2. Tạo Session Factory bất đồng bộ
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Cần thiết cho async để truy cập thuộc tính sau commit
    autocommit=False,
    autoflush=False,
)


# 3. Base Class cho tất cả Model (User, ChatHistory, Document, Embeddings,...)
class Base(DeclarativeBase):
    pass


# 4. Dependency cấp Session cho FastAPI Endpoints
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency trả về một AsyncSession cho từng Request
    và tự động đóng session khi xử lý xong.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()