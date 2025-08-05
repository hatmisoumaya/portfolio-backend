from fastapi import FastAPI
from pydantic import BaseModel
import requests, os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
prompt_content = os.getenv("PROMPT_TEXT")  

app = FastAPI()

class Question(BaseModel):
    message: str
    
@app.get("/")
def read_root():
    return {"message": "Backend is working!"}
@app.post("/ask")
def ask_user(question: Question):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "temperature": 0.9,
        "messages": [
            {
            "role": "system",
            "content": prompt_content  # Now this is guaranteed to be valid
        },
        {
            "role": "user",
            "content": question.message
        }
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    data = response.json()
    reply = data["choices"][0]["message"]["content"]
    return {"response": reply}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
