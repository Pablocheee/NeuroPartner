from interfaces.telegram.FiniteStateMachine import State, GOAL_DISCOVERY, VALUE_DEMO
from telegram import Update
from telegram.ext import ContextTypes
from core.user import User, UserId
from core.goals import Goal

class GoalDiscoveryState(State):
    \"\"\"Состояние выявления истинных целей пользователя\"\"\"
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        
        # Создаем или получаем пользователя
        user = await self._get_or_create_user(update, context)
        
        # Извлекаем цель с помощью AI
        goal = await self.goal_extractor.extract_true_goal(user_message, user)
        
        # Сохраняем цель
        context.user_data['current_goal'] = goal
        user.add_goal(goal)
        
        # Сохраняем пользователя
        await self.state_manager.user_repository.save(user)
        
        # Показываем подтверждение и предлагаем демонстрацию
        confirmation_text = f\"\"\"
🎯 Понял твою цель!

**Истинная цель:** {goal.true_goal}
**Профессия:** {user.profile.profession or 'определяется автоматически'}
**Целевой результат:** {goal.success_criteria.measurable_target}

💫 Хочешь, чтобы я прямо сейчас показал, как AI может помочь с этой целью?
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
