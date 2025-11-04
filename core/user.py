from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from . import UserId, SubscriptionTier

@dataclass
class UserProfile:
    \"\"\"Профиль пользователя\"\"\"
    name: str
    profession: Optional[str] = None
    experience_level: str = \"beginner\"
    preferred_language: str = \"russian\"
    timezone: str = \"Europe/Moscow\"
    created_at: datetime = field(default_factory=datetime.now)

@dataclass  
class UIPreferences:
    \"\"\"Настройки интерфейса пользователя\"\"\"
    theme: str = \"cosmic_neon\"
    emoji_set: str = \"🌌🚀🤖🛸💫\"
    notification_level: str = \"normal\"
    learning_pace: str = \"moderate\"

@dataclass
class User:
    \"\"\"Агрегат пользователя\"\"\"
    id: UserId
    profile: UserProfile
    goals: List['Goal'] = field(default_factory=list)
    projects: List['Project'] = field(default_factory=list)
    subscription: 'Subscription' = None
    learning_progress: 'LearningProgress' = None
    ui_preferences: UIPreferences = field(default_factory=UIPreferences)
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    
    def add_goal(self, goal: 'Goal') -> None:
        \"\"\"Добавить цель пользователю\"\"\"
        self.goals.append(goal)
    
    def get_active_projects(self) -> List['Project']:
        \"\"\"Получить активные проекты\"\"\"
        return [p for p in self.projects if p.status == ProjectStatus.ACTIVE]
    
    def can_create_project(self) -> bool:
        \"\"\"Может ли пользователь создать новый проект\"\"\"
        if self.subscription.tier == SubscriptionTier.FREE:
            return len(self.projects) < 1
        return True
    
    def update_activity(self) -> None:
        \"\"\"Обновить время последней активности\"\"\"
        self.last_active = datetime.now()
