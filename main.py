from fastapi import FastAPI
from database import close_db, connect_db 
from routers.auth import auth_router
from routers.chatbot import chatbot_router

app = FastAPI(
    title="ReWear API",
    description="Backend API for the ReWear Community Clothing Exchange platform.",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(chatbot_router)

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on application startup."""
    print("Application starting up...")
    connect_db()

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on application shutdown."""
    print("Application shutting down. Database connection closed.")
    close_db()