from typing import List, Dict, Any
from core.learning import Skill, SkillLevel, LearningProgress
from core.goals import Goal
from core.projects import Project

class SkillGapAnalyzer:
    \"\"\"Анализатор пробелов в навыках для достижения целей\"\"\"
    
    def __init__(self):
        self.skill_library = self._initialize_skill_library()
    
    def analyze_gaps(self, goal: Goal, current_skills: List[Skill]) -> List[Skill]:
        \"\"\"Проанализировать пробелы в навыках для цели\"\"\"
        required_skills = self._get_required_skills(goal)
        current_skill_names = {skill.name for skill in current_skills}
        
        gaps = []
        for skill in required_skills:
            if skill.name not in current_skill_names:
                gaps.append(skill)
        
        return gaps
    
    def recommend_learning_path(self, goal: Goal, current_progress: LearningProgress) -> List[Dict[str, Any]]:
        \"\"\"Рекомендовать путь обучения\"\"\"
        skill_gaps = self.analyze_gaps(goal, current_progress.skills_learned)
        
        learning_path = []
        for skill in skill_gaps:
            learning_path.append({
                'skill': skill,
                'priority': self._calculate_priority(skill, goal),
                'estimated_time': '2-4 часа',
                'project_type': self._get_project_type_for_skill(skill)
            })
        
        # Сортируем по приоритету
        learning_path.sort(key=lambda x: x['priority'], reverse=True)
        
        return learning_path
    
    def _get_required_skills(self, goal: Goal) -> List[Skill]:
        \"\"\"Получить требуемые навыки для цели\"\"\"
        goal_text = goal.true_goal.lower()
        
        required_skills = []
        
        # Определяем навыки на основе типа цели
        if any(word in goal_text for word in ['маркетинг', 'продвижение', 'продажи']):
            required_skills.extend([
                Skill(\"ai_marketing\", \"AI-маркетинг\", \"marketing\", SkillLevel.BEGINNER, 50),
                Skill(\"content_creation\", \"Создание контента\", \"marketing\", SkillLevel.BEGINNER, 40),
                Skill(\"analytics\", \"Аналитика\", \"marketing\", SkillLevel.INTERMEDIATE, 60)
            ])
        
        elif any(word in goal_text for word in ['программирование', 'код', 'разработка']):
            required_skills.extend([
                Skill(\"ai_coding\", \"AI-программирование\", \"development\", SkillLevel.BEGINNER, 70),
                Skill(\"problem_solving\", \"Решение задач\", \"development\", SkillLevel.INTERMEDIATE, 80),
                Skill(\"debugging\", \"Отладка\", \"development\", SkillLevel.BEGINNER, 50)
            ])
        
        elif any(word in goal_text for word in ['дизайн', 'интерфейс', 'визуал']):
            required_skills.extend([
                Skill(\"ai_design\", \"AI-дизайн\", \"design\", SkillLevel.BEGINNER, 60),
                Skill(\"ux_principles\", \"Принципы UX\", \"design\", SkillLevel.BEGINNER, 40),
                Skill(\"prototyping\", \"Прототипирование\", \"design\", SkillLevel.INTERMEDIATE, 70)
            ])
        
        else:  # Общие навыки
            required_skills.extend([
                Skill(\"ai_assistance\", \"Работа с AI\", \"general\", SkillLevel.BEGINNER, 30),
                Skill(\"project_management\", \"Управление проектами\", \"general\", SkillLevel.BEGINNER, 40),
                Skill(\"problem_solving\", \"Решение проблем\", \"general\", SkillLevel.INTERMEDIATE, 60)
            ])
        
        return required_skills
    
    def _calculate_priority(self, skill: Skill, goal: Goal) -> int:
        \"\"\"Рассчитать приоритет навыка\"\"\"
        base_priority = 5
        
        # Увеличиваем приоритет для ключевых навыков
        if any(keyword in skill.name for keyword in ['ai', 'маркетинг', 'код']):
            base_priority += 2
        
        # Учитываем уровень сложности
        if skill.level == SkillLevel.BEGINNER:
            base_priority += 1
        elif skill.level == SkillLevel.ADVANCED:
            base_priority -= 1
        
        return base_priority
    
    def _get_project_type_for_skill(self, skill: Skill) -> str:
        \"\"\"Получить тип проекта для отработки навыка\"\"\"
        project_types = {
            'ai_marketing': 'Создание AI-маркетинг плана',
            'content_creation': 'Генерация контента с AI',
            'ai_coding': 'Разработка с AI-помощником',
            'ai_design': 'Создание дизайна с AI'
        }
        return project_types.get(skill.name, 'Практический проект с AI')
    
    def _initialize_skill_library(self) -> Dict[str, Skill]:
        \"\"\"Инициализировать библиотеку навыков\"\"\"
        skills = [
            Skill(\"ai_marketing\", \"AI-маркетинг\", \"marketing\", SkillLevel.BEGINNER, \"Использование AI для маркетинга\", 50),
            Skill(\"content_creation\", \"Создание контента\", \"marketing\", SkillLevel.BEGINNER, \"Создание контента с помощью AI\", 40),
            Skill(\"analytics\", \"Аналитика\", \"marketing\", SkillLevel.INTERMEDIATE, \"Анализ данных и метрик\", 60),
            Skill(\"ai_coding\", \"AI-программирование\", \"development\", SkillLevel.BEGINNER, \"Программирование с AI-помощником\", 70),
            Skill(\"problem_solving\", \"Решение задач\", \"development\", SkillLevel.INTERMEDIATE, \"Решение технических задач\", 80),
            Skill(\"ai_design\", \"AI-дизайн\", \"design\", SkillLevel.BEGINNER, \"Создание дизайна с AI\", 60),
            Skill(\"ux_principles\", \"Принципы UX\", \"design\", SkillLevel.BEGINNER, \"Основы пользовательского опыта\", 40),
        ]
        return {skill.id: skill for skill in skills}
