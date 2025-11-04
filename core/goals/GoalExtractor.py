from typing import Dict, Any, Optional
from core.goals import Goal, SuccessCriteria
from core.user import User
import re

class GoalExtractor:
    \"\"\"Извлечение истинных целей из диалога\"\"\"
    
    def __init__(self):
        self.profession_patterns = {
            'маркетолог': ['маркетинг', 'продвижение', 'конверсия', 'трафик'],
            'программист': ['код', 'разработка', 'приложение', 'сайт'],
            'дизайнер': ['дизайн', 'интерфейс', 'визуал', 'ux/ui'],
            'предприниматель': ['бизнес', 'стартап', 'продажи', 'клиенты'],
            'студент': ['учеба', 'обучение', 'проект', 'курс']
        }
    
    async def extract_true_goal(self, user_message: str, user: User) -> Goal:
        \"\"\"Извлечь истинную цель из сообщения пользователя\"\"\"
        
        # Анализ сообщения
        profession = self._detect_profession(user_message)
        true_goal = self._extract_core_goal(user_message)
        measurable_target = self._create_measurable_target(true_goal)
        
        # Создание критериев успеха
        success_criteria = SuccessCriteria(
            measurable_target=measurable_target,
            quality_standards=[\"работающий прототип\", \"измеримые результаты\"]
        )
        
        goal = Goal(
            id=str(hash(user_message + user.id.value)),
            user_id=user.id.value,
            true_goal=true_goal,
            stated_goal=user_message,
            description=f\"Автоматически выявленная цель для {profession}\",
            success_criteria=success_criteria,
            priority=self._calculate_priority(user_message)
        )
        
        return goal
    
    def _detect_profession(self, message: str) -> str:
        \"\"\"Определить профессию из сообщения\"\"\"
        message_lower = message.lower()
        
        for profession, keywords in self.profession_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return profession
        
        return \"создатель\"  # профессия по умолчанию
    
    def _extract_core_goal(self, message: str) -> str:
        \"\"\"Извлечь ядро цели\"\"\"
        # Убираем вводные слова
        cleaned = re.sub(r'(хочу|мне нужно|надо|желаю)\s+', '', message.lower())
        
        # Определяем тип цели
        if any(word in cleaned for word in ['научиться', 'освоить', 'изучить']):
            return f\"Освоить практический навык: {cleaned}\"
        elif any(word in cleaned for word in ['создать', 'разработать', 'сделать']):
            return f\"Создать работающий проект: {cleaned}\"
        elif any(word in cleaned for word in ['увеличить', 'улучшить', 'оптимизировать']):
            return f\"Улучшить показатели: {cleaned}\"
        else:
            return f\"Достичь практического результата: {cleaned}\"
    
    def _create_measurable_target(self, true_goal: str) -> str:
        \"\"\"Создать измеримую цель\"\"\"
        if 'навык' in true_goal:
            return \"Создать 1 работающий проект с применением навыка\"
        elif 'проект' in true_goal:
            return \"Завершенный проект с измеримыми результатами\"  
        elif 'показатели' in true_goal:
            return \"Улучшение ключевых метрик на 25%+\"
        else:
            return \"Конкретный измеримый результат за 24 часа\"
    
    def _calculate_priority(self, message: str) -> int:
        \"\"\"Рассчитать приоритет цели\"\"\"
        urgency_words = ['срочно', 'быстро', 'немедленно', 'сегодня']
        if any(word in message.lower() for word in urgency_words):
            return 8
        return 5
