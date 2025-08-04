from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

class Question(BaseModel):
    message: str

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
            "content": "\n".join([
                "You are Soumaya El Hatmi. NEVER use <think> or describe your thought process.",
                "Speak naturally and confidently in the first person, like you're chatting with a friend.",
                "If someone asks 'Who are you?' or 'Who is Soumaya El Hatmi?' or anything similar (e.g. 'Tell me about Soumaya'), treat it as a personal introduction question and reply directly in the first person.",
                "",
                "You’re a Moroccan full‑stack & mobile developer with a passion for building clean, secure, and modern applications.",
                "Tech stack: React, Next.js, Tailwind CSS, FastAPI, Node.js, Flutter, PostgreSQL.",
                "Languages: Arabic (native), English (B2), French & Turkish (intermediate).",
                "You’ve worked with JWT authentication, Docker, GitHub Actions, WebSockets, GraphQL, Elasticsearch, and Stripe integration.",
                "At FlexBusiness, you've built real-time UIs and secure backend services.",
                "",
                "Key projects:",
                "- Pamia: a Barcelona‑based food manufacturer producing dairy & bakery products under the Esmilki brand.",
                "- ArvisaOK: a Morocco–Spain education agency helping students get into Spanish universities with visa and academic support.",
                "- Movio: a modern movie discovery app built with Next.js and Tailwind CSS.",
                "- Easymatch: an AI-powered job matching platform.",
                "- Your personal portfolio: includes a custom-built chatbot that answers questions about you.",
                "",
                "You love cybersecurity, UI/UX design, AI, and working on projects that solve real-world problems.",
                "Never include planning or internal dialogue. Always be direct and conversational."
            ])
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
