from typing import List, Dict, Any
from core.learning import LearningProgress, Skill
from core.goals import Goal

class AdaptiveLearningPath:
    \"\"\"Адаптивный путь обучения на основе целей и прогресса\"\"\"
    
    def __init__(self, skill_gap_analyzer):
        self.skill_gap_analyzer = skill_gap_analyzer
    
    def generate_learning_plan(self, goal: Goal, user_progress: LearningProgress) -> Dict[str, Any]:
        \"\"\"Сгенерировать персональный план обучения\"\"\"
        
        # Анализируем пробелы
        skill_gaps = self.skill_gap_analyzer.analyze_gaps(goal, user_progress.skills_learned)
        learning_path = self.skill_gap_analyzer.recommend_learning_path(goal, user_progress)
        
        # Создаем план проектов
        projects_plan = self._create_projects_plan(learning_path, goal)
        
        return {
            'goal': goal.true_goal,
            'current_level': user_progress.current_level,
            'skill_gaps': len(skill_gaps),
            'learning_path': learning_path,
            'projects_plan': projects_plan,
            'estimated_completion_time': f\"{len(projects_plan) * 2} часов\",
            'confidence_score': self._calculate_confidence(user_progress, skill_gaps)
        }
    
    def _create_projects_plan(self, learning_path: List[Dict], goal: Goal) -> List[Dict[str, Any]]:
        \"\"\"Создать план проектов для обучения\"\"\"
        projects = []
        
        for i, item in enumerate(learning_path[:3]):  # Первые 3 навыка
            project = {
                'id': f\"project_{i+1}\",
                'name': f\"Практика: {item['skill'].name}\",
                'description': f\"Освоение навыка {item['skill'].description} через практический проект\",
                'skill': item['skill'],
                'duration': item['estimated_time'],
                'xp_reward': item['skill'].xp_value,
                'steps': self._generate_project_steps(item['skill'], goal)
            }
            projects.append(project)
        
        return projects
    
    def _generate_project_steps(self, skill: Skill, goal: Goal) -> List[Dict[str, str]]:
        \"\"\"Сгенерировать шаги проекта\"\"\"
        
        base_steps = [
            {\"step\": 1, \"title\": \"Постановка задачи\", \"description\": \"Определить конкретную задачу для решения\"},
            {\"step\": 2, \"title\": \"AI-анализ\", \"description\": \"Проанализировать задачу с помощью AI\"},
            {\"step\": 3, \"title\": \"Практическая реализация\", \"description\": \"Выполнить практическую часть\"},
            {\"step\": 4, \"title\": \"Проверка результатов\", \"description\": \"Протестировать и улучшить результат\"}
        ]
        
        # Адаптируем шаги под конкретный навык
        if 'маркетинг' in skill.name:
            base_steps[2]['description'] = \"Создать маркетинг-материалы с AI\"
        elif 'код' in skill.name:
            base_steps[2]['description'] = \"Написать код с AI-помощником\"
        elif 'дизайн' in skill.name:
            base_steps[2]['description'] = \"Создать дизайн-прототип с AI\"
        
        return base_steps
    
    def _calculate_confidence(self, progress: LearningProgress, skill_gaps: List[Skill]) -> float:
        \"\"\"Рассчитать уверенность в достижении цели\"\"\"
        base_confidence = progress.current_level / 10.0  # 0.1 to 1.0
        
        # Уменьшаем уверенность при большом количестве пробелов
        gap_penalty = len(skill_gaps) * 0.1
        confidence = max(0.1, base_confidence - gap_penalty)
        
        # Увеличиваем уверенность при наличии опыта
        if progress.completed_projects > 0:
            confidence += min(0.3, progress.completed_projects * 0.1)
        
        return min(1.0, confidence)
