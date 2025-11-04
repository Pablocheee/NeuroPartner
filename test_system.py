#!/usr/bin/env python3
\"\"\"
🧪 NeuroPartner - Тестирование системы
\"\"\"

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_ai_providers():
    \"\"\"Тестирование AI провайдеров\"\"\"
    print(\"🧪 Тестирование AI провайдеров...\\n\")
    
    try:
        from infrastructure.external import AIClient
        ai_client = AIClient()
        
        is_available = await ai_client.is_any_available()
        print(f\"🤖 Доступен ли любой AI провайдер: {'✅ Да' if is_available else '❌ Нет'}\")
        
        if is_available:
            test_message = \"Хочу научиться маркетингу для своего онлайн-курса\"
            print(f\"📨 Тестовое сообщение: {test_message}\")
            
            result = await ai_client.process_message(test_message, {
                'task_type': 'goal_extraction',
                'budget': 0
            })
            
            print(f\"✅ Получен ответ от {result['provider']}:\")
            print(f\"📝 {result['content']}\")
            
    except Exception as e:
        print(f\"❌ Ошибка AI обработки: {e}\")
    
    print()

async def main():
    \"\"\"Главная функция тестирования\"\"\"
    print(\"🧪 NeuroPartner System Test\")
    print(\"=\" * 50)
    
    await test_ai_providers()
    
    print(\"✅ Тестирование завершено!\")

if __name__ == \"__main__\":
    asyncio.run(main())
