import os
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="GhostWriter AI API",
    description="Generate product marketing copy with a locally hosted open-weight model.",
    version="1.0.0",
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")


class ProductRequest(BaseModel):
    product_name: str = Field(min_length=1, max_length=120)
    category: str = Field(default="", max_length=120)
    features: str = Field(min_length=1, max_length=3000)
    audience: str = Field(default="", max_length=300)
    price: str = Field(default="", max_length=80)
    offer: str = Field(default="", max_length=500)
    platform: str = Field(default="Instagram", max_length=80)
    tone: str = Field(default="Friendly", max_length=80)
    language: str = Field(default="English", max_length=40)
    call_to_action: str = Field(default="Message us to order", max_length=200)


@app.get("/")
def home():
    return {
        "name": "GhostWriter AI API",
        "status": "running",
        "model": OLLAMA_MODEL,
        "docs": "/docs",
    }


@app.get("/health")
def health():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        response.raise_for_status()
        models = [item.get("name", "") for item in response.json().get("models", [])]
        return {"api": "ok", "ollama": "reachable", "configured_model": OLLAMA_MODEL, "available_models": models}
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Ollama is not reachable. Start Ollama and check OLLAMA_URL.")


@app.post("/generate")
def generate_sales_kit(data: ProductRequest):
    prompt = f"""
You are GhostWriter AI, a practical marketing copy assistant for small businesses.
Create a useful, honest sales kit using only the facts supplied below.
Do not invent certifications, health benefits, materials, discounts, shipping promises, reviews, or product specifications.
If a detail is missing, leave it out rather than making it up.
Write in {data.language}. Tone: {data.tone}. Main platform: {data.platform}.

PRODUCT DETAILS
Name: {data.product_name}
Category: {data.category or "Not specified"}
Features: {data.features}
Target customer: {data.audience or "Not specified"}
Price: {data.price or "Not specified"}
Offer: {data.offer or "Not specified"}
Call to action: {data.call_to_action or "Contact us to order"}

Return a polished Markdown sales kit with these headings:
## Product title
## Short product description
## Full product description
## Social media caption
## Hashtags
## Promotional message
## Three alternative hooks

Keep it clear, specific, and suitable for a small seller. Mention the price only if supplied.
Avoid exaggerated promises and do not claim that the product is the best.
"""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7},
            },
            timeout=180,
        )
        response.raise_for_status()
        body = response.json()
        sales_kit = body.get("response", "").strip()
        if not sales_kit:
            raise HTTPException(status_code=502, detail="The model returned an empty response.")
        return {"sales_kit": sales_kit, "model": OLLAMA_MODEL, "provider": "Ollama"}
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="The model request timed out. Try again.")
    except requests.ConnectionError:
        raise HTTPException(status_code=503, detail="Cannot connect to Ollama. Start Ollama and ensure the model is installed.")
    except requests.HTTPError as exc:
        message = "Ollama returned an error."
        if exc.response is not None:
            try:
                message = exc.response.json().get("error", message)
            except Exception:
                pass
        raise HTTPException(status_code=502, detail=message)
