from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
from . import ProjectStatus

@dataclass
class ProjectResult:
    \"\"\"Результаты выполнения проекта\"\"\"
    time_saved: float = 0.0  # часов
    efficiency_gain: float = 1.0  # множитель
    achievement: str = \"\"
    metrics: Dict[str, Any] = field(default_factory=dict)
    user_feedback: Optional[str] = None

@dataclass
class Project:
    \"\"\"Доменная модель проекта\"\"\"
    id: str
    user_id: str
    goal_id: str
    name: str
    description: str
    status: ProjectStatus = ProjectStatus.DRAFT
    template_type: str = \"custom\"
    steps: List[Dict] = field(default_factory=list)
    current_step: int = 0
    result: Optional[ProjectResult] = None
    ai_amplified: bool = False
    goal_contribution: float = 0.0  # 0.0 - 1.0
    time_estimate: timedelta = field(default_factory=lambda: timedelta(hours=2))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def is_completed(self) -> bool:
        \"\"\"Проверка завершения проекта\"\"\"
        return self.status == ProjectStatus.COMPLETED
    
    def get_current_step(self) -> Optional[Dict]:
        \"\"\"Получить текущий шаг\"\"\"
        if self.steps and 0 <= self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def complete_step(self) -> bool:
        \"\"\"Завершить текущий шаг\"\"\"
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.updated_at = datetime.now()
            return True
        else:
            self.status = ProjectStatus.COMPLETED
            return False
    
    def calculate_roi(self) -> float:
        \"\"\"Рассчитать ROI проекта\"\"\"
        if not self.result:
            return 0.0
        return self.result.efficiency_gain * self.result.time_saved
