from core.projects import Project, ProjectResult, ProjectStatus
from core.learning import ProgressIntegrator, LearningProgress
from infrastructure.persistence import ProjectRepository

class CompleteProjectCommand:
    \"\"\"Команда завершения проекта с обновлением прогресса\"\"\"
    
    def __init__(self, project_repository: ProjectRepository, progress_integrator: ProgressIntegrator):
        self.project_repository = project_repository
        self.progress_integrator = progress_integrator
    
    async def execute(self, project: Project, user_progress: LearningProgress, results: Dict[str, Any]) -> LearningProgress:
        \"\"\"Завершить проект и обновить прогресс пользователя\"\"\"
        
        # Создаем результат проекта
        project_result = ProjectResult(
            time_saved=results.get('time_saved', 0),
            efficiency_gain=results.get('efficiency_gain', 1.0),
            achievement=results.get('achievement', ''),
            metrics=results.get('metrics', {})
        )
        
        # Завершаем проект
        project.complete(project_result)
        await self.project_repository.save(project)
        
        # Обновляем прогресс пользователя
        updated_progress = self.progress_integrator.update_progress_from_project(
            user_progress, project, project_result
        )
        
        return updated_progress
