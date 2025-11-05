from typing import List
from core.projects import Project
from infrastructure.persistence import ProjectRepository

class GetUserProjectsQuery:
    \"\"\"Запрос получения проектов пользователя\"\"\"
    
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
    
    async def execute(self, user_id: str) -> List[Project]:
        \"\"\"Получить все проекты пользователя\"\"\"
        return await self.project_repository.get_by_user_id(user_id)
    
    async def get_active_project(self, user_id: str) -> Project:
        \"\"\"Получить активный проект пользователя\"\"\"
        return await self.project_repository.get_active_project(user_id)
