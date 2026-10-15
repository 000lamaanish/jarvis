
from fastapi import FastAPI

app = FastAPI(title="JARVIS AI Assistant")


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
