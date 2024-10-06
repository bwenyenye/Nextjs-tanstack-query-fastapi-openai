from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os 

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3005"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class Message(BaseModel):
    message: str

chat_history = []

@app.post("/chat")
async def chat(message: Message):
    chat_history.append({"role": "user", "content": message.message})
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )
    ai_message = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": ai_message})
    return {"message": ai_message}

@app.get("/chat")
async def get_chat_history():
    return chat_history