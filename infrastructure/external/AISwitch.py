from typing import Dict, Any, List

class AISwitch:
    \"\"\"Интеллектуальное переключение между AI провайдерами\"\"\"
    
    def __init__(self):
        self.usage_stats = {}
        self.cost_tracker = {}
        self.provider_capabilities = {
            'openai': {
                'creative': 8, 
                'technical': 9, 
                'russian': 7, 
                'cost': 5,
                'speed': 8
            },
            'gemini': {
                'creative': 9, 
                'technical': 8, 
                'russian': 6, 
                'cost': 2,
                'speed': 7
            },
            'yandexgpt': {
                'creative': 7, 
                'technical': 7, 
                'russian': 10, 
                'cost': 4,
                'speed': 6
            },
            'ollama': {
                'creative': 6, 
                'technical': 6, 
                'russian': 5, 
                'cost': 0,
                'speed': 5
            }
        }
    
    def get_optimal_provider(self, task_type: str, budget: int) -> str:
        \"\"\"Выбор оптимального провайдера для задачи\"\"\"
        
        # Бесплатный вариант
        if budget == 0:
            return 'ollama'
        
        # Выбор на основе типа задачи и бюджета
        scored_providers = []
        for provider, capabilities in self.provider_capabilities.items():
            if capabilities['cost'] <= budget:
                score = capabilities.get(task_type, 5)
                # Учитываем скорость для срочных задач
                if task_type == 'urgent':
                    score += capabilities['speed'] * 0.5
                scored_providers.append((provider, score))
        
        if scored_providers:
            return max(scored_providers, key=lambda x: x[1])[0]
        
        # Fallback стратегия
        if task_type == 'creative':
            return 'gemini'
        elif task_type == 'technical':
            return 'openai' 
        elif task_type == 'russian':
            return 'yandexgpt'
        else:
            return 'gemini'  # По умолчанию Gemini как самый доступный
    
    def update_cost_stats(self, provider: str, cost: float) -> None:
        \"\"\"Обновить статистику затрат\"\"\"
        self.cost_tracker[provider] = self.cost_tracker.get(provider, 0) + cost
    
    def get_usage_report(self) -> Dict[str, Any]:
        \"\"\"Получить отчет об использовании\"\"\"
        return {
            'usage_stats': self.usage_stats,
            'cost_tracker': self.cost_tracker,
            'total_requests': sum(self.usage_stats.values()),
            'preferred_provider': max(self.usage_stats.items(), key=lambda x: x[1])[0] if self.usage_stats else 'none'
        }
