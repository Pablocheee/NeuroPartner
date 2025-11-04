from typing import List, Dict, Any
from core.learning import LearningProgress
from core.projects import Project

class LessonOrchestrator:
    \"\"\"Оркестратор уроков и практических заданий\"\"\"
    
    def __init__(self):
        self.lesson_templates = self._initialize_lesson_templates()
    
    async def get_daily_lesson(self, user_progress: LearningProgress, active_project: Project = None) -> Dict[str, Any]:
        \"\"\"Получить ежедневный урок для пользователя\"\"\"
        
        # Определяем тип урока на основе прогресса и активного проекта
        lesson_type = self._determine_lesson_type(user_progress, active_project)
        
        # Выбираем шаблон урока
        lesson_template = self.lesson_templates.get(lesson_type, self.lesson_templates['default'])
        
        # Персонализируем урок
        personalized_lesson = self._personalize_lesson(lesson_template, user_progress, active_project)
        
        return personalized_lesson
    
    def _determine_lesson_type(self, progress: LearningProgress, project: Project) -> str:
        \"\"\"Определить тип урока\"\"\"
        
        if progress.current_level <= 2:
            return \"beginner\"
        elif not project:
            return \"project_selection\"
        elif project.current_step == 0:
            return \"project_start\"
        elif project.current_step >= len(project.steps) - 1:
            return \"project_completion\"
        else:
            return \"skill_development\"
    
    def _personalize_lesson(self, template: Dict, progress: LearningProgress, project: Project) -> Dict[str, Any]:
        \"\"\"Персонализировать урок\"\"\"
        lesson = template.copy()
        
        # Заменяем плейсхолдеры
        if project:
            lesson['title'] = lesson['title'].replace('{project_name}', project.name)
            lesson['content'] = lesson['content'].replace('{project_step}', str(project.current_step + 1))
        
        lesson['content'] = lesson['content'].replace('{user_level}', str(progress.current_level))
        lesson['xp_reward'] = progress.current_level * 10  # XP зависит от уровня
        
        return lesson
    
    def _initialize_lesson_templates(self) -> Dict[str, Dict]:
        \"\"\"Инициализировать шаблоны уроков\"\"\"
        return {
            \"beginner\": {
                \"title\": \"🚀 Введение в AI-партнерство\",
                \"content\": \"Привет! Сегодня мы освоим основы работы с AI. Твой уровень: {user_level}\",
                \"duration\": \"15 минут\",
                \"type\": \"theory\",
                \"practice_task\": \"Попробуй задать AI простой вопрос о своем проекте\"
            },
            \"project_start\": {
                \"title\": \"🎯 Начинаем проект: {project_name}\",
                \"content\": \"Отлично! Сегодня мы начинаем проект. Шаг {project_step} из {total_steps}\",
                \"duration\": \"20 минут\", 
                \"type\": \"practice\",
                \"practice_task\": \"Выполни первый шаг проекта с AI-помощником\"
            },
            \"skill_development\": {
                \"title\": \"💫 Развитие навыков\",
                \"content\": \"Продолжаем работать над проектом. Уровень {user_level}\",
                \"duration\": \"25 минут\",
                \"type\": \"practice\", 
                \"practice_task\": \"Примени новый навык в текущем проекте\"
            },
            \"project_completion\": {
                \"title\": \"🏆 Завершение проекта: {project_name}\",
                \"content\": \"Финальный рывок! Завершаем проект и фиксируем результаты\",
                \"duration\": \"30 минут\",
                \"type\": \"practice\",
                \"practice_task\": \"Заверши проект и проанализируй результаты\"
            },
            \"default\": {
                \"title\": \"💫 Ежедневное развитие\",
                \"content\": \"Продолжаем движение к цели! Уровень {user_level}\",
                \"duration\": \"20 минут\",
                \"type\": \"practice\",
                \"practice_task\": \"Выполни один шаг к своей цели с AI\"
            }
        }
    
    def validate_lesson_completion(self, user_input: str, lesson: Dict) -> bool:
        \"\"\"Валидировать завершение урока\"\"\"
        # Простая валидация - пользователь прислал любой текст
        return len(user_input.strip()) > 10  # Минимум 10 символов
