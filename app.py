import google.generativeai as genai
import os

# Настройка Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

async def get_ai_response(message):
    """Получить ответ от AI"""
    try:
        if GEMINI_API_KEY:
            prompt = f"""Ты - NeuroPartner, AI помощник для достижения целей. 
Пользователь написал: {message}

Ответь практично и полезно, предложи следующий шаг."""
            response = model.generate_content(prompt)
            return response.text
        else:
            return "AI временно недоступен. Расскажи о своей цели!"
    except Exception as e:
        return f"Ошибка AI: {e}"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            # Получить AI ответ
            ai_response = await get_ai_response(text)
            
            return {
                "method": "sendMessage", 
                "chat_id": chat_id,
                "text": ai_response
            }
            
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error"}
