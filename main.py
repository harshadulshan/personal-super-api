from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI(title="My Personal Super API", version="1.0")

OLLAMA_URL = "http://localhost:11434/api/generate"

class ChatRequest(BaseModel):
    message: str
    model: str = "mistral"

class CodeRequest(BaseModel):
    code: str
    model: str = "mistral"

@app.get("/")
def home():
    return {
        "name": "My Personal Super API",
        "version": "1.0",
        "status": "running",
        "endpoints": ["/chat", "/code/explain", "/code/fix", "/docs"]
    }

@app.post("/chat")
async def chat(req: ChatRequest):
    async with httpx.AsyncClient(timeout=120) as client:
        res = await client.post(OLLAMA_URL, json={
            "model": req.model,
            "prompt": req.message,
            "stream": False
        })
        data = res.json()
        return {
            "message": req.message,
            "reply": data["response"],
            "model": req.model
        }

@app.post("/code/explain")
async def explain_code(req: CodeRequest):
    prompt = f"Explain this code clearly step by step:\n\n{req.code}"
    async with httpx.AsyncClient(timeout=120) as client:
        res = await client.post(OLLAMA_URL, json={
            "model": req.model,
            "prompt": prompt,
            "stream": False
        })
        data = res.json()
        return {
            "original_code": req.code,
            "explanation": data["response"]
        }

@app.post("/code/fix")
async def fix_code(req: CodeRequest):
    prompt = f"Find and fix any bugs in this code. Show the fixed code and explain what was wrong:\n\n{req.code}"
    async with httpx.AsyncClient(timeout=120) as client:
        res = await client.post(OLLAMA_URL, json={
            "model": req.model,
            "prompt": prompt,
            "stream": False
        })
        data = res.json()
        return {
            "original_code": req.code,
            "fixed": data["response"]
        }
