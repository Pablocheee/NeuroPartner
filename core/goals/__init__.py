from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
from . import GoalStatus

@dataclass
class SuccessCriteria:
    \"\"\"Критерии успеха цели\"\"\"
    measurable_target: str
    deadline: Optional[datetime] = None
    quality_standards: List[str] = field(default_factory=list)
    validation_method: str = \"practical_result\"

@dataclass
class Goal:
    \"\"\"Доменная модель цели\"\"\"
    id: str
    user_id: str
    true_goal: str  # Истинная цель, извлеченная AI
    stated_goal: str  # То, что сказал пользователь
    description: str
    status: GoalStatus = GoalStatus.DISCOVERED
    success_criteria: SuccessCriteria = None
    priority: int = 5  # 1-10
    estimated_value: float = 0.0  # Расчетная ценность в условных единицах
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def calculate_progress(self, projects: List['Project']) -> float:
        \"\"\"Рассчитать прогресс цели на основе проектов\"\"\"
        if not projects:
            return 0.0
        
        relevant_projects = [p for p in projects if p.goal_id == self.id]
        if not relevant_projects:
            return 0.0
            
        completed = len([p for p in relevant_projects if p.status == ProjectStatus.COMPLETED])
        total = len(relevant_projects)
        
        return completed / total if total > 0 else 0.0
    
    def mark_completed(self) -> None:
        \"\"\"Пометить цель как завершенную\"\"\"
        self.status = GoalStatus.COMPLETED
        self.updated_at = datetime.now()
