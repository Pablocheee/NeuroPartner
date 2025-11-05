from typing import Dict, Any
from core.goals import Goal
from core.projects import Project, ProjectStatus
from infrastructure.persistence import ProjectRepository

class CreateProjectFromGoalCommand:
    \"\"\"Команда создания проекта из выявленной цели\"\"\"
    
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
    
    async def execute(self, user_id: str, goal: Goal) -> Project:
        \"\"\"Создать проект на основе цели пользователя\"\"\"
        
        # Создаем проект из цели
        project = Project(
            id=f\"project_{user_id}_{int(datetime.now().timestamp())}\",
            user_id=user_id,
            goal_id=goal.id,
            name=f\"Проект: {goal.true_goal}\",
            description=f\"Практический проект для достижения: {goal.true_goal}\",
            status=ProjectStatus.ACTIVE,
            steps=self._generate_project_steps(goal)
        )
        
        # Сохраняем проект
        await self.project_repository.save(project)
        
        return project
    
    def _generate_project_steps(self, goal: Goal) -> List[Dict[str, str]]:
        \"\"\"Генерирует шаги проекта на основе цели\"\"\"
        return [
            {\"step\": 1, \"title\": \"Определение задачи\", \"description\": \"Конкретизируем что нужно сделать\"},
            {\"step\": 2, \"description\": \"Выполняем практическую часть\"},
            {\"step\": 3, \"description\": \"Анализируем результаты и улучшаем\"}
        ]
