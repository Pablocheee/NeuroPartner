import asyncio
from typing import Dict, Any, Optional, List
from infrastructure.external.OpenAIClient import OpenAIClient
from infrastructure.external.GeminiClient import GeminiClient
from infrastructure.external.OllamaClient import OllamaClient
from infrastructure.external.YandexGPTClient import YandexGPTClient
from infrastructure.external.AISwitch import AISwitch

class AIClient:
    \"\"\"Универсальный клиент для работы с AI провайдерами\"\"\"
    
    def __init__(self):
        self.providers = {
            'openai': OpenAIClient(),
            'gemini': GeminiClient(), 
            'ollama': OllamaClient(),
            'yandexgpt': YandexGPTClient()
        }
        self.fallback_chain = ['gemini', 'openai', 'yandexgpt', 'ollama']
        self.switch = AISwitch()
    
    async def process_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Обработать сообщение с автоматическим выбором провайдера\"\"\"
        
        # Определяем оптимального провайдера
        optimal_provider = self.switch.get_optimal_provider(
            context.get('task_type', 'general'),
            context.get('budget', 0)
        )
        
        # Цепочка fallback
        providers_to_try = [optimal_provider] + [
            p for p in self.fallback_chain if p != optimal_provider
        ]
        
        for provider_name in providers_to_try:
            try:
                provider = self.providers[provider_name]
                if await provider.is_available():
                    print(f\"🤖 Используем провайдер: {provider_name}\")
                    result = await provider.process(message, context)
                    
                    # Обновляем статистику
                    self.switch.usage_stats[provider_name] = \
                        self.switch.usage_stats.get(provider_name, 0) + 1
                    
                    return result
            except Exception as e:
                print(f\"❌ Провайдер {provider_name} недоступен: {e}\")
                continue
        
        raise Exception(\"Все AI провайдеры недоступны\")
    
    async def is_any_available(self) -> bool:
        \"\"\"Проверка доступности любого провайдера\"\"\"
        for provider in self.providers.values():
            if await provider.is_available():
                return True
        return False
    
    def get_usage_report(self) -> Dict[str, Any]:
        \"\"\"Получить отчет об использовании\"\"\"
        return self.switch.get_usage_report()
