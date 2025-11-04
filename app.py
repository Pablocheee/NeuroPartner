#!/usr/bin/env python3
"""
🚀 NeuroPartner - FastAPI приложение
"""

from fastapi import FastAPI
import asyncio
import os
import sys

# Создаем FastAPI приложение
app = FastAPI(title="NeuroPartner", version="1.0.0")

@app.get("/")
async def root():
    return {"ready": True, "status": "NeuroPartner AI System", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Остальной код NeuroPartner...
print("🌌 NeuroPartner FastAPI запущен!")
@app.post("/webhook")
async def telegram_webhook(update: dict):
    return {"status": "ok"}

from telegram import Update
from telegram.ext import Application

@app.post("/webhook")
async def telegram_webhook(update: dict):
    # Обработка сообщений от Telegram
    print(f"Получено сообщение: {update}")
    return {"status": "ok"}

from fastapi import Request

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        print(f"Telegram webhook received: {update}")
        
        # Простой ответ боту
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            # Ответное сообщение
            response = {
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": f"NeuroPartner получил: {text}"
            }
            return response
            
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error"}
