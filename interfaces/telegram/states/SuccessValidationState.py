from interfaces.telegram.FiniteStateMachine import State, SUCCESS_VALIDATION, WELCOME
from telegram import Update
from telegram.ext import ContextTypes
from application.ProjectCoordinatorService import ProjectCoordinatorService

class SuccessValidationState(State):
    \"\"\"Состояние завершения проекта с переходом в меню\"\"\"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        goal = context.user_data.get('current_goal')
        project = context.user_data.get('current_project')
        
        # Получаем дашборд с прогрессом
        coordinator = ProjectCoordinatorService()
        user_id = str(update.effective_user.id)
        dashboard = await coordinator.get_user_dashboard(user_id)
        
        if user_message.lower() in ['меню', 'главная', 'start', '/start', 'главное меню']:
            # Сброс и переход в главное меню
            context.user_data.clear()
            await update.message.reply_text(
                \"🏠 Возвращаемся в главное меню!\",
                reply_markup=self.keyboard_factory.get_main_menu(dashboard)
            )
            return WELCOME
        
        # Показываем итог проекта с прогрессом
        success_text = f\"\"\"
🎉 **Проект успешно завершен!**

🏆 **Цель:** {goal.true_goal}
✅ **Проект:** {project.name}
📊 **Уровень:** {dashboard['progress'].current_level}
🛸 **Всего проектов:** {dashboard['total_projects']}

💫 Выбери что делать дальше:
        \"\"\"

        await update.message.reply_text(
            success_text,
            reply_markup=self.keyboard_factory.get_main_menu(dashboard)
        )

        # Остаемся в этом состоянии пока пользователь не выберет меню
        return SUCCESS_VALIDATION
