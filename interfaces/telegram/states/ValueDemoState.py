from interfaces.telegram.FiniteStateMachine import State, VALUE_DEMO, PROJECT_CREATION
from telegram import Update
from telegram.ext import ContextTypes
from infrastructure.external import AIClient

class ValueDemoState(State):
    \"\"\"Состояние демонстрации практической ценности AI\"\"\"
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        goal = context.user_data.get('current_goal')
        
        if user_message.lower() in ['да', 'yes', 'хочу', 'покажи']:
            # Показываем демонстрацию AI
            await update.message.reply_text(\"🚀 Создаю практическую демонстрацию...\")
            
            # Используем AI для создания демо
            ai_client = AIClient()
            demo_result = await ai_client.process_message(
                f\"Создай практическую демонстрацию для цели: {goal.true_goal}\",
                {'task_type': 'project_creation'}
            )
            
            # Показываем результат
            demo_text = f\"\"\"
💫 **Вот что AI может сделать для твоей цели:**

{demo_result['content']}

🎯 **Готов создать полноценный проект вместе?**
            \"\"\"
            
            await update.message.reply_text(
                demo_text,
                reply_markup=self.keyboard_factory.get_project_creation_keyboard()
            )
            
            return PROJECT_CREATION
        
        else:
            # Пользователь отказался от демо
            await update.message.reply_text(
                \"Хорошо! Можешь вернуться, когда будешь готов создать проект. 🪐\",
                reply_markup=self.keyboard_factory.get_main_menu({})
            )
            return PROJECT_CREATION
