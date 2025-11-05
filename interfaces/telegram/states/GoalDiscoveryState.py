from interfaces.telegram.FiniteStateMachine import State, GOAL_DISCOVERY, LEARNING
from telegram import Update
from telegram.ext import ContextTypes
from core.user import User, UserId
from application.ProjectCoordinatorService import ProjectCoordinatorService

class GoalDiscoveryState(State):
    \"\"\"Состояние выявления истинных целей пользователя\"\"\"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text

        # Создаем или получаем пользователя
        user = await self._get_or_create_user(update, context)

        # Используем координатор вместо сырого AI
        coordinator = ProjectCoordinatorService()
        result = await coordinator.process_user_goal(user.id.value, user_message)

        # Сохраняем цель и проект в контекст
        context.user_data['current_goal'] = result['goal']
        context.user_data['current_project'] = result['project']

        # Показываем подтверждение и предлагаем обучение
        confirmation_text = f\"\"\"
🎯 Понял твою цель!

**Истинная цель:** {result['goal'].true_goal}
**Профессия:** {user.profile.profession or 'определяется автоматически'}
**Создан проект:** {result['project'].name}

💫 Давай начнем обучение для этой цели?
        \"\"\"

        await update.message.reply_text(
            confirmation_text,
            reply_markup=self.keyboard_factory.get_yes_no_keyboard()
        )

        return LEARNING

    async def _get_or_create_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> User:
        \"\"\"Создать или получить пользователя\"\"\"
        user_id = str(update.effective_user.id)

        # Пытаемся найти существующего пользователя
        user = await self.state_manager.user_repository.get_by_id(UserId(user_id))

        if not user:
            # Создаем нового пользователя
            from core.user import UserProfile
            profile = UserProfile(
                name=update.effective_user.first_name or \"Пользователь\"
            )

            user = User(
                id=UserId(user_id),
                profile=profile,
                telegram_id=update.effective_user.id
            )

            await self.state_manager.user_repository.save(user)

        return user
