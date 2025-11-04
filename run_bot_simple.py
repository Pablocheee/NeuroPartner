#!/usr/bin/env python3
\"\"\"
?? NeuroPartner - Упрощенный запуск
\"\"\"

import asyncio
import os
import sys

def setup_environment():
    \"\"\"Настройка окружения\"\"\"
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    class SimpleSettings:
        def __init__(self):
            self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            self.gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    return SimpleSettings()

async def test_gemini():
    \"\"\"Тест работы Gemini\"\"\"
    try:
        from infrastructure.external.GeminiClient import GeminiClient
        
        client = GeminiClient()
        if await client.is_available():
            print(\"? Gemini доступен!\")
            result = await client.process(\"Привет! Ответь коротко.\", {\"task_type\": \"general\"})
            print(f\"?? Gemini: {result['content'][:50]}...\")
            return True
        else:
            print(\"? Gemini недоступен\")
            return False
            
    except Exception as e:
        print(f\"? Ошибка теста Gemini: {e}\")
        return False

async def main():
    \"\"\"Главная функция\"\"\"
    print(\"\"\"
?? NeuroPartner - Упрощенный запуск
?? Проверка системы...
\"\"\")
    
    settings = setup_environment()
    
    if not settings.telegram_bot_token:
        print(\"??  TELEGRAM_BOT_TOKEN не установлен\")
    
    if not settings.gemini_api_key:
        print(\"??  GEMINI_API_KEY не установлен\")
    else:
        print(\"? GEMINI_API_KEY найден\")
    
    print(\"\\n?? Тестирование AI...\")
    ai_working = await test_gemini()
    
    if ai_working:
        print(\"\"\"
?? Базовая система работает!
        
?? Следующие шаги:
1. Установи TELEGRAM_BOT_TOKEN в .env
2. Запусти: python run_bot_simple.py
\"\"\")
    else:
        print(\"\"\"
? Есть проблемы с AI
?? Проверь GEMINI_API_KEY в .env
\"\"\")

if __name__ == \"__main__\":
    asyncio.run(main())
