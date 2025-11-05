from interfaces.telegram.FiniteStateMachine import State, SUCCESS_VALIDATION, WELCOME
from telegram import Update
from telegram.ext import ContextTypes

class SuccessValidationState(State):
    \"\"\"Состояние завершения проекта с переходом в меню\"\"\"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        goal = context.user_data.get('current_goal')
        
        if user_message.lower() in ['меню', 'главная', 'start', '/start', 'главное меню']:
            # Сброс и переход в главное меню
            context.user_data.clear()
            await update.message.reply_text(
                \"🏠 Возвращаемся в главное меню!\",
                reply_markup=self.keyboard_factory.get_main_menu({})
            )
            return WELCOME
        
        # Поздравляем с завершением и предлагаем меню
        success_text = f\"\"\"
🎉 **Проект успешно завершен!**

🏆 Ты достиг: {goal.true_goal}
🚀 Отличная работа! Теперь у тебя есть реальный результат.

💫 Выбери что делать дальше:
        \"\"\"

        await update.message.reply_text(
            success_text,
            reply_markup=self.keyboard_factory.get_main_menu({})
        )

        # Остаемся в этом состоянии пока пользователь не выберет меню
        return SUCCESS_VALIDATION
