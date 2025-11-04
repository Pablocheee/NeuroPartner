import openai
import os
from typing import Dict, Any
from infrastructure.config import settings

class OpenAIClient:
    \"\"\"Клиент для OpenAI API\"\"\"
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        self.model_name = \"gpt-3.5-turbo\"
        self.configured = bool(self.api_key)
    
    async def is_available(self) -> bool:
        \"\"\"Проверка доступности OpenAI\"\"\"
        return self.configured
    
    async def process(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Обработать сообщение через OpenAI\"\"\"
        if not self.configured:
            raise Exception(\"OpenAI не сконфигурирован\")
        
        try:
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {\"role\": \"system\", \"content\": \"Ты практичный AI-партнер NeuroPartner.\"},
                    {\"role\": \"user\", \"content\": message}
                ],
                max_tokens=1000
            )
            
            return {
                'provider': 'openai',
                'content': response.choices[0].message.content,
                'model': self.model_name,
                'cost': 0.002
            }
        except Exception as e:
            raise Exception(f\"OpenAI error: {str(e)}\")
