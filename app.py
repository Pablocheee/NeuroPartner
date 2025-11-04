#!/usr/bin/env python3
"""
🚀 NeuroPartner - Главный запуск системы
"""

import asyncio
import logging
import sys
import os

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from infrastructure.config import settings
    print("✅ Конфигурация загружена")
except ImportError as e:
    print(f"❌ Ошибка импорта конфигурации: {e}")
    sys.exit(1)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def test_gemini():
    """Тест работы Gemini"""
    try:
        from infrastructure.external.GeminiClient import GeminiClient
        client = GeminiClient()
        
        if await client.is_available():
            print("✅ Gemini доступен!")
            result = await client.process("Привет! Ответь коротко.", {"task_type": "general"})
            print(f"🤖 Ответ: {result['content'][:100]}...")
            return True
        else:
            print("❌ Gemini недоступен")
            return False
    except Exception as e:
        print(f"❌ Ошибка Gemini: {e}")
        return False

async def main():
    """Запуск системы NeuroPartner"""
    try:
        print("""
🌌 🚀 🤖 🛸 💫 🌠 🪐 🔭
      
NeuroPartner System Startup...
Версия: 1.0.0
Режим: Testing
        """)
        
        # Проверяем конфигурацию
        if not settings.telegram_bot_token:
            print("⚠️  TELEGRAM_BOT_TOKEN не установлен")
        else:
            print("✅ TELEGRAM_BOT_TOKEN найден")
        
        if not settings.gemini_api_key:
            print("⚠️  GEMINI_API_KEY не установлен")
        else:
            print("✅ GEMINI_API_KEY найден")
        
        # Тест AI
        print("\n🧪 Тестирование AI...")
        ai_working = await test_gemini()
        
        if ai_working:
            print("""
🎉 NeuroPartner готов к работе!

📝 Следующие шаги:
1. Запусти бота: python run_bot_simple.py
2. Или протестируй полную систему
            """)
        else:
            print("""
❌ Есть проблемы с AI системой

🔧 Проверь:
1. GEMINI_API_KEY в .env файле
2. Интернет соединение
3. Файлы проекта
            """)
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        
    finally:
        print("\n🛑 NeuroPartner завершил работу")

if __name__ == "__main__":
    asyncio.run(main())
