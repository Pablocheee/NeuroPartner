from application.commands import CreateProjectFromGoalCommand, CompleteProjectCommand
from application.queries import GetUserProjectsQuery, GetUserProgressQuery
from core.goals import GoalExtractor
from infrastructure.persistence import UserRepository, GoalRepository, ProjectRepository
from core.learning import ProgressIntegrator

class ProjectCoordinatorService:
    \"\"\"Главный сервис координации проектов и целей\"\"\"
    
    def __init__(self):
        # Репозитории
        self.user_repository = UserRepository()
        self.goal_repository = GoalRepository() 
        self.project_repository = ProjectRepository()
        
        # Команды
        self.create_project_cmd = CreateProjectFromGoalCommand(self.project_repository)
        self.complete_project_cmd = CompleteProjectCommand(self.project_repository, ProgressIntegrator())
        
        # Запросы
        self.get_projects_query = GetUserProjectsQuery(self.project_repository)
        self.get_progress_query = GetUserProgressQuery(self.user_repository)
        
        # Сервисы
        self.goal_extractor = GoalExtractor()
    
    async def process_user_goal(self, user_id: str, user_message: str) -> dict:
        \"\"\"Обработать цель пользователя и создать проект\"\"\"
        
        # Выявляем цель
        user = await self.user_repository.get_by_id(user_id)
        goal = await self.goal_extractor.extract_true_goal(user_message, user)
        
        # Сохраняем цель
        user.add_goal(goal)
        await self.user_repository.save(user)
        
        # Создаем проект
        project = await self.create_project_cmd.execute(user_id, goal)
        
        return {
            'goal': goal,
            'project': project,
            'user': user
        }
    
    async def complete_user_project(self, user_id: str, project_id: str, results: dict) -> dict:
        \"\"\"Завершить проект пользователя\"\"\"
        
        # Получаем проект и прогресс
        projects = await self.get_projects_query.execute(user_id)
        project = next((p for p in projects if p.id == project_id), None)
        progress = await self.get_progress_query.execute(user_id)
        
        if not project:
            raise ValueError(\"Project not found\")
        
        # Завершаем проект
        updated_progress = await self.complete_project_cmd.execute(project, progress, results)
        
        # Обновляем пользователя
        user = await self.user_repository.get_by_id(user_id)
        user.learning_progress = updated_progress
        await self.user_repository.save(user)
        
        return {
            'project': project,
            'progress': updated_progress,
            'level_up': updated_progress.current_level > progress.current_level
        }
    
    async def get_user_dashboard(self, user_id: str) -> dict:
        \"\"\"Получить дашборд пользователя с проектами и прогрессом\"\"\"
        
        projects = await self.get_projects_query.execute(user_id)
        progress = await self.get_progress_query.execute(user_id)
        
        return {
            'active_projects': [p for p in projects if p.status.value == 'active'],
            'completed_projects': [p for p in projects if p.status.value == 'completed'],
            'progress': progress,
            'current_level': progress.current_level,
            'total_projects': len(projects)
        }
