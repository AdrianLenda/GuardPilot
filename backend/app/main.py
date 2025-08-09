from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
import uuid
import os
import asyncio
import requests

from .database import init_db, get_session
from .models import ConversationLog
from .utils.pii_detection import detect_pii
from .utils.risk_classifier import classify_risk
from .utils.parquet_logger import append_log
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class LLMRequest(BaseModel):
    conversation_id: str | None = None
    messages: list[Message]

class LLMResponse(BaseModel):
    conversation_id: str
    reply: str

app = FastAPI()

@app.on_event("startup")
def on_startup() -> None:
    init_db()

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

async def call_llm(messages: list[Message]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        def _call() -> str:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            data = {
                "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                "messages": [m.dict() for m in messages],
                "temperature": 0.7,
            }
            response = requests.post(url, json=data, headers=headers, timeout=60)
            response.raise_for_status()
            resp_json = response.json()
            return resp_json["choices"][0]["message"]["content"]
        return await asyncio.to_thread(_call)
    else:
        joined = " ".join(m.content for m in messages)
        return f"Echo: {joined}"

@app.post("/proxy", response_model=LLMResponse)
async def proxy(request: LLMRequest, session: Session = Depends(get_session)) -> LLMResponse:
    conv_id = request.conversation_id or str(uuid.uuid4())
    if not request.messages:
        raise HTTPException(status_code=400, detail="No messages provided")
    prompt = request.messages[-1].content
    reply = await call_llm(request.messages)
    combined = f"{prompt} {reply}"
    detected = detect_pii(combined)
    pii_detected = len(detected) > 0
    risk_level, tags = classify_risk(combined)
    log_entry = ConversationLog(
        conversation_id=conv_id,
        prompt=prompt,
        response=reply,
        risk_level=risk_level,
        tags=tags,
        pii_detected=pii_detected,
        detected_pii=detected,
    )
    session.add(log_entry)
    session.commit()
    session.refresh(log_entry)
    append_log(log_entry.dict())
    return LLMResponse(conversation_id=conv_id, reply=reply)

@app.get("/logs")
def get_logs(
    conversation_id: str | None = None,
    session: Session = Depends(get_session),
) -> list[ConversationLog]:
    stmt = select(ConversationLog)
    if conversation_id:
        stmt = stmt.where(ConversationLog.conversation_id == conversation_id)
    return session.exec(stmt).all()

@app.get("/risk_incidents")
def get_risk_incidents(session: Session = Depends(get_session)) -> list[ConversationLog]:
    stmt = select(ConversationLog).where(
        ConversationLog.pii_detected | (ConversationLog.risk_level == "high-risk")
    )
    return session.exec(stmt).all()
