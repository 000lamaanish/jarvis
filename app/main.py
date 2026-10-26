
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

app = FastAPI(title="JARVIS AI Assistant")

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
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are JARVIS, a helpful personal AI assistant. "
                            "Be clear, intelligent, polite, and concise."
                        )
                    },
                    {
                        "role": "user",
                        "content": request.message
                    }
                ],
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()
        result = response.json()

        return {
            "assistant": "JARVIS",
            "reply": result["message"]["content"]
        }

    except requests.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail=f"Could not communicate with Ollama: {error}"
        ) from error
