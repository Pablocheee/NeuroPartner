from interfaces.telegram.FiniteStateMachine import State, SUCCESS_VALIDATION, SUBSCRIPTION_OFFER
from telegram import Update
from telegram.ext import ContextTypes

class SuccessValidationState(State):
    \"\"\"Состояние валидации успеха проекта\"\"\"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        goal = context.user_data.get('current_goal')
        
        # Поздравляем с завершением проекта
        success_text = f\"\"\"
🎉 **Проект успешно завершен!**

🏆 Ты достиг: {goal.true_goal}
🚀 Отличная работа! Теперь у тебя есть реальный результат.

💫 Хочешь продолжить создавать проекты с полным доступом к AI?
        \"\"\"

        await update.message.reply_text(
            success_text,
            reply_markup=self.keyboard_factory.get_subscription_offer_keyboard()
        )

        return SUBSCRIPTION_OFFER
