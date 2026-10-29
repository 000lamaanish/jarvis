
# from fastapi import FastAPI

# app = FastAPI(title="JARVIS AI Assistant")


# @app.get("/")
# def home():
#     return {
#         "assistant": "JARVIS",
#         "status": "online",
#         "message": "All systems operational."
#     }


# @app.get("/health")
# def health():
#     return {"status": "healthy"}






import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import initialize_database, save_message, get_recent_messages

app = FastAPI(title="JARVIS AI Assistant")
initialize_database()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "assistant": "JARVIS",
        "status": "online",
        "message": "All systems operational."
    }


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest):
    # Save the user's message permanently
    save_message("user", request.message)

    # Retrieve recent conversation history from SQLite
    history = get_recent_messages(limit=10)

    messages = [
        {
            "role": "system",
            "content": (
                "You are JARVIS, a helpful personal AI assistant. "
                "Be clear, intelligent, polite, and concise. "
                "Use the conversation history to answer questions "
                "about information the user shared earlier."
            )
        }
    ] + history

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()
        result = response.json()
        reply = result["message"]["content"]

        # Save JARVIS's response permanently
        save_message("assistant", reply)

        return {
            "assistant": "JARVIS",
            "reply": reply
        }

    except requests.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail=f"Could not communicate with Ollama: {error}"
        ) from error
