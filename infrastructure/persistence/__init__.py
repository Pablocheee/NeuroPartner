from typing import List, Optional, Dict, Any
from core.user import User, UserId
from core.goals import Goal
from core.projects import Project
import json

class UserRepository:
    \"\"\"Репозиторий для работы с пользователями\"\"\"
    
    def __init__(self):
        # Временное хранилище в памяти
        self._users: Dict[str, User] = {}
    
    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        \"\"\"Получить пользователя по ID\"\"\"
        return self._users.get(user_id.value)
    
    async def save(self, user: User) -> None:
        \"\"\"Сохранить пользователя\"\"\"
        self._users[user.id.value] = user
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        \"\"\"Получить пользователя по Telegram ID\"\"\"
        for user in self._users.values():
            if hasattr(user, 'telegram_id') and user.telegram_id == telegram_id:
                return user
        return None

class GoalRepository:
    \"\"\"Репозиторий для работы с целями\"\"\"
    
    def __init__(self):
        self._goals: Dict[str, Goal] = {}
    
    async def get_by_user_id(self, user_id: str) -> List[Goal]:
        \"\"\"Получить цели пользователя\"\"\"
        return [goal for goal in self._goals.values() if goal.user_id == user_id]
    
    async def save(self, goal: Goal) -> None:
        \"\"\"Сохранить цель\"\"\"
        self._goals[goal.id] = goal
    
    async def get_active_goal(self, user_id: str) -> Optional[Goal]:
        \"\"\"Получить активную цель пользователя\"\"\"
        user_goals = await self.get_by_user_id(user_id)
        for goal in user_goals:
            if goal.status.value == 'active':
                return goal
        return None

class ProjectRepository:
    \"\"\"Репозиторий для работы с проектами\"\"\"
    
    def __init__(self):
        self._projects: Dict[str, Project] = {}
    
    async def get_by_user_id(self, user_id: str) -> List[Project]:
        \"\"\"Получить проекты пользователя\"\"\"
        return [project for project in self._projects.values() if project.user_id == user_id]
    
    async def save(self, project: Project) -> None:
        \"\"\"Сохранить проект\"\"\"
        self._projects[project.id] = project
    
    async def get_active_project(self, user_id: str) -> Optional[Project]:
        \"\"\"Получить активный проект пользователя\"\"\"
        user_projects = await self.get_by_user_id(user_id)
        for project in user_projects:
            if project.status.value == 'active':
                return project
        return None
