from interfaces.telegram.FiniteStateMachine import State, LEARNING, PROJECT_CREATION
from telegram import Update
from telegram.ext import ContextTypes
from infrastructure.external import AIClient

class LearningState(State):
    \"\"\"Состояние обучения после выявления цели\"\"\"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        goal = context.user_data.get('current_goal')
        
        # AI создает учебный план для цели
        ai_client = AIClient()
        learning_plan = await ai_client.process_message(
            f\"Создай краткий учебный план для цели: {goal.true_goal}. \" 
            \"3-5 практических шагов обучения.\",
            {'task_type': 'learning_plan'}
        )

        learning_text = f\"\"\"
🎓 **бучение для твоей цели:** {goal.true_goal}

{learning_plan['content']}

💡 **отов начать практический проект?**
        \"\"\"

        await update.message.reply_text(
            learning_text,
            reply_markup=self.keyboard_factory.get_yes_no_keyboard()
        )

        return PROJECT_CREATION
