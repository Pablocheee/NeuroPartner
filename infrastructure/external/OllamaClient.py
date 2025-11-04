import requests
import json
from typing import Dict, Any

class OllamaClient:
    \"\"\"Клиент для локальных моделей Ollama\"\"\"
    
    def __init__(self):
        self.base_url = \"http://localhost:11434/api\"
        self.model_name = \"llama2\"  # Можно изменить на доступную модель
    
    async def is_available(self) -> bool:
        \"\"\"Проверка доступности Ollama\"\"\"
        try:
            response = requests.get(f\"{self.base_url}/tags\", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    async def process(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Обработать сообщение через Ollama\"\"\"
        try:
            payload = {
                \"model\": self.model_name,
                \"prompt\": message,
                \"stream\": False
            }
            
            response = requests.post(
                f\"{self.base_url}/generate\",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'provider': 'ollama',
                    'content': result['response'],
                    'model': self.model_name,
                    'cost': 0.0
                }
            else:
                raise Exception(f\"Ollama API error: {response.status_code}\")
        except Exception as e:
            raise Exception(f\"Ollama error: {str(e)}\")
