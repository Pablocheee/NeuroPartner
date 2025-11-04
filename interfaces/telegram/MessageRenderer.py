from typing import List, Dict, Any
from core.goals import Goal
from core.projects import Project

class MessageRenderer:
    \"\"\"Рендерер сообщений для Telegram\"\"\"
    
    def render_goal_progress(self, goal: Goal, projects: List[Project]) -> str:
        \"\"\"Рендер прогресса цели\"\"\"
        progress = goal.calculate_progress(projects)
        progress_bar = self._create_progress_bar(progress)
        
        completed_projects = len([p for p in projects if p.is_completed()])
        total_projects = len(projects)
        
        return f\"\"\"
🌠 **Цель:** {goal.true_goal}
🪐 **Прогресс:** {progress_bar} {progress:.0%}

✅ **Завершено проектов:** {completed_projects}/{total_projects}
🚀 **Следующий шаг:** {self._get_next_steps(goal, projects)}

💫 **До цели осталось:** {self._format_remaining(goal, progress)}
        \"\"\"
    
    def render_project_success(self, project: Project, results) -> str:
        \"\"\"Рендер успешного завершения проекта\"\"\"
        return f\"\"\"
🛸 **Проект завершен!** 🌌

🤖 **Проект:** {project.name}
✅ **Результаты:**
   • 🌠 Сэкономлено времени: {results.time_saved} часов
   • 🚀 Увеличена эффективность: {results.efficiency_gain}x
   • 🪐 Достигнуто: {results.achievement}

🎯 **Вклад в цель:** +{project.goal_contribution:.0%}

💫 **Готов к следующему проекту?**
        \"\"\"
    
    def _create_progress_bar(self, progress: float, length: int = 10) -> str:
        \"\"\"Создать текстовый прогресс-бар\"\"\"
        filled = int(progress * length)
        empty = length - filled
        return \"█\" * filled + \"░\" * empty
    
    def _get_next_steps(self, goal: Goal, projects: List[Project]) -> str:
        \"\"\"Получить следующие шаги\"\"\"
        active_projects = [p for p in projects if not p.is_completed()]
        if active_projects:
            return f\"Продолжить проект '{active_projects[0].name}'\"
        else:
            return \"Создать новый проект для этой цели\"
    
    def _format_remaining(self, goal: Goal, progress: float) -> str:
        \"\"\"Форматировать оставшееся до цели\"\"\"
        if progress >= 1.0:
            return \"Цель достигнута! 🎉\"
        elif progress > 0.7:
            return \"Очень близко! 💫\"
        elif progress > 0.3:
            return \"Хороший прогресс! 🚀\"
        else:
            return \"Начинаем путь! 🌠\"
