from fastapi import FastAPI
from src.core.config import settings
from src.routers import chat

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

# Tích hợp Chat Router
app.include_router(chat.router)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok", "app_name": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)