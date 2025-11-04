from typing import List
from core.learning import LearningProgress, Skill
from core.projects import Project, ProjectResult

class ProgressIntegrator:
    \"\"\"Интегратор прогресса обучения и проектов\"\"\"
    
    def update_progress_from_project(self, progress: LearningProgress, project: Project, result: ProjectResult) -> LearningProgress:
        \"\"\"Обновить прогресс на основе завершенного проекта\"\"\"
        
        # Добавляем XP за проект
        base_xp = 50
        if project.ai_amplified:
            base_xp += 20
        if result.efficiency_gain > 2.0:
            base_xp += 30
        
        progress.add_xp(base_xp)
        progress.completed_projects += 1
        
        # Добавляем навыки на основе типа проекта
        skills_learned = self._extract_skills_from_project(project)
        for skill in skills_learned:
            progress.add_skill(skill)
        
        # Обновляем серию активности
        progress.learning_streak += 1
        
        return progress
    
    def _extract_skills_from_project(self, project: Project) -> List[Skill]:
        \"\"\"Извлечь навыки из проекта\"\"\"
        skills = []
        
        # Определяем навыки на основе типа проекта
        if any(keyword in project.name.lower() for keyword in ['маркетинг', 'продвижение']):
            skills.append(Skill(\"ai_marketing\", \"AI-маркетинг\", \"marketing\", \"beginner\", 50))
        
        elif any(keyword in project.name.lower() for keyword in ['код', 'разработка', 'программирование']):
            skills.append(Skill(\"ai_coding\", \"AI-программирование\", \"development\", \"beginner\", 70))
        
        elif any(keyword in project.name.lower() for keyword in ['дизайн', 'интерфейс']):
            skills.append(Skill(\"ai_design\", \"AI-дизайн\", \"design\", \"beginner\", 60))
        
        # Общие навыки
        skills.append(Skill(\"project_management\", \"Управление проектами\", \"general\", \"beginner\", 40))
        skills.append(Skill(\"ai_assistance\", \"Работа с AI\", \"general\", \"beginner\", 30))
        
        return skills
    
    def get_progress_summary(self, progress: LearningProgress) -> Dict:
        \"\"\"Получить сводку прогресса\"\"\"
        return {
            'level': progress.current_level,
            'total_xp': progress.total_xp,
            'level_progress': progress.get_level_progress(),
            'completed_projects': progress.completed_projects,
            'learning_streak': progress.learning_streak,
            'skills_learned': len(progress.skills_learned),
            'next_level_xp': progress._get_required_xp(progress.current_level) - progress.total_xp
        }
