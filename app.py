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
