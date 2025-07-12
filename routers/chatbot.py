import os
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

from .auth import get_current_user

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

class ChatbotRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500,
                         description="The user's message to the chatbot.")

class ChatbotResponse(BaseModel):
    response: str = Field(..., description="The chatbot's generated response.")

chatbot_router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@chatbot_router.post("/ask", response_model=ChatbotResponse)
async def ask_chatbot(
    request: ChatbotRequest,
    
):
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are ReWear Bot, a helpful assistant for a community clothing exchange platform. Provide information, styling tips, or answer questions related to sustainable fashion, clothing swaps, and second-hand items."},
                {"role": "user", "content": request.message}
            ]
        )

        chatbot_response_content = completion.choices[0].message.content
        return ChatbotResponse(response=chatbot_response_content)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error communicating with the chatbot service: {e}"
        )