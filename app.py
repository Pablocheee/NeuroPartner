from fastapi import FastAPI, Request
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

app = FastAPI(title="NeuroPartner")

# Настройка Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"🔧 GEMINI_API_KEY: {GEMINI_API_KEY}")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    print("✅ Gemini AI настроен")
else:
    print("❌ GEMINI_API_KEY не найден")

async def get_ai_response(message):
    try:
        if GEMINI_API_KEY:
            prompt = f"Ты - NeuroPartner, AI помощник. Пользователь: {message}"
            response = model.generate_content(prompt)
            return response.text
        else:
            return "AI временно недоступен"
    except Exception as e:
        return f"Ошибка AI: {e}"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            ai_response = await get_ai_response(text)
            return {"method": "sendMessage", "chat_id": chat_id, "text": ai_response}
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error"}

@app.get("/")
async def root():
    return {"message": "NeuroPartner API работает!"}

@app.get("/health")
async def health():
    return {"status": "ok", "ai": bool(GEMINI_API_KEY)}
