from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class SkillLevel(Enum):
    BEGINNER = \"beginner\"
    INTERMEDIATE = \"intermediate\" 
    ADVANCED = \"advanced\"
    EXPERT = \"expert\"

@dataclass
class Skill:
    \"\"\"Модель навыка\"\"\"
    id: str
    name: str
    category: str
    level: SkillLevel
    description: str
    xp_value: int

@dataclass
class LearningProgress:
    \"\"\"Прогресс обучения пользователя\"\"\"
    user_id: str
    total_xp: int = 0
    current_level: int = 1
    skills_learned: List[Skill] = None
    completed_projects: int = 0
    learning_streak: int = 0
    last_activity: datetime = None
    
    def __post_init__(self):
        if self.skills_learned is None:
            self.skills_learned = []
    
    def add_xp(self, xp: int) -> None:
        \"\"\"Добавить опыт\"\"\"
        self.total_xp += xp
        self._check_level_up()
        self.last_activity = datetime.now()
    
    def _check_level_up(self) -> None:
        \"\"\"Проверить повышение уровня\"\"\"
        required_xp = self._get_required_xp(self.current_level)
        if self.total_xp >= required_xp:
            self.current_level += 1
    
    def _get_required_xp(self, level: int) -> int:
        \"\"\"Получить требуемый XP для уровня\"\"\"
        return level * 100  # Простая формула
    
    def add_skill(self, skill: Skill) -> None:
        \"\"\"Добавить освоенный навык\"\"\"
        self.skills_learned.append(skill)
        self.add_xp(skill.xp_value)
    
    def get_level_progress(self) -> float:
        \"\"\"Получить прогресс текущего уровня\"\"\"
        current_level_xp = self.total_xp - self._get_required_xp(self.current_level - 1)
        next_level_xp = self._get_required_xp(self.current_level) - self._get_required_xp(self.current_level - 1)
        return current_level_xp / next_level_xp
