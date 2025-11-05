from interfaces.telegram.FiniteStateMachine import State, LEARNING, PROJECT_EXECUTION
from telegram import Update
from telegram.ext import ContextTypes
from application.ProjectCoordinatorService import ProjectCoordinatorService

class LearningState(State):
    \"\"\"Состояние обучения после выявления цели\"\"\"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        goal = context.user_data.get('current_goal')
        project = context.user_data.get('current_project')

        if user_message.lower() in ['да', 'yes', 'хочу', 'начать']:
            # Показываем учебный план
            learning_text = f\"\"\"
🎓 **Обучение для цели:** {goal.true_goal}

📚 **План обучения:**
1. **Определение задачи** - конкретизируем что нужно сделать
2. **Практическое выполнение** - создаем реальный результат  
3. **Анализ и улучшение** - учимся на практике

🚀 **Готов перейти к первому шагу проекта?**
            \"\"\"

            await update.message.reply_text(
                learning_text,
                reply_markup=self.keyboard_factory.get_yes_no_keyboard()
            )

            return PROJECT_EXECUTION

        else:
            # Возвращаем к обучению
            await update.message.reply_text(
                \"Обучение поможет тебе достичь цели быстрее. Хочешь начать?\",
                reply_markup=self.keyboard_factory.get_yes_no_keyboard()
            )
            return LEARNING
