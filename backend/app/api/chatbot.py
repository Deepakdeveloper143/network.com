from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Initialize Groq client
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print(f"Warning: Could not initialize Groq client: {e}")
    client = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    groq_api_key: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None

SYSTEM_PROMPT = """You are QuantumShieldAI, an expert cybersecurity assistant specializing in:
- Post-quantum cryptography
- Vulnerability assessment
- Prompt security and LLM protection
- Compliance standards (SOC 2, ISO 27001, NIST)
- Security best practices

Provide helpful, accurate, and practical security advice. Keep responses concise but informative."""

@router.post("/chatbot")
async def chat(request: ChatRequest):
    try:
        # Determine which API key to use
        api_key = request.groq_api_key or os.getenv("GROQ_API_KEY")
        
        if not api_key:
            return ChatResponse(
                response="⚠️ Groq API not configured. Please set GROQ_API_KEY in the .env file or provide it in the chat settings.",
                sources=["QuantumShieldAI Fallback"]
            )
        
        # Initialize Groq client with the selected API key
        groq_client = Groq(api_key=api_key)

        # Prepare messages with system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})

        # Call Groq API
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=request.temperature,
            max_tokens=1024
        )

        response = completion.choices[0].message.content

        return ChatResponse(
            response=response,
            sources=["Groq - Llama 3.1 8B Instant"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chatbot: {str(e)}")
