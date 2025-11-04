#!/usr/bin/env python3
"""
🚀 NeuroPartner - FastAPI приложение
"""

from fastapi import FastAPI, Request
import os

app = FastAPI(title="NeuroPartner", version="1.0.0")

@app.get("/")
async def root():
    return {"ready": True, "status": "NeuroPartner AI System", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        print(f"Telegram webhook received")
        
        # Простой ответ
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            return {
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": f"NeuroPartner получил: {text}"
            }
            
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error"}

print("🌌 NeuroPartner FastAPI запущен!")
