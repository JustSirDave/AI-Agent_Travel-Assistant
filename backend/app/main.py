from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Set your OpenAI API key in your environment or use dotenv
openai.api_key = os.getenv("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")

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# System prompt for travel assistant
SYSTEM_PROMPT = "You are a helpful travel assistant. Reply concisely and informatively."

# Helper function to interact with GPT-4
def get_gpt_reply(user_input: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Endpoint to handle chat
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    reply = get_gpt_reply(payload.message)
    return {"reply": reply}  
