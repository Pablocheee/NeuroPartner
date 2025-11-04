from interfaces.telegram.FiniteStateMachine import State, PROJECT_CREATION, PROJECT_EXECUTION
from telegram import Update
from telegram.ext import ContextTypes
from infrastructure.external import AIClient

class ProjectCreationState(State):
    """Состояние создания проекта по цели пользователя"""

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        goal = context.user_data.get('current_goal')

        if user_message.lower() in ['создать', 'начать', 'да', 'поехали']:
            # Создаем проект с помощью AI
            await update.message.reply_text("🛠️ Создаю пошаговый проект...")

            ai_client = AIClient()
            project_plan = await ai_client.process_message(
                f"Создай пошаговый план проекта для цели: {goal.true_goal}. " 
                "Верни 3-5 конкретных шагов.",
                {'task_type': 'project_planning'}
            )

            # Сохраняем план проекта
            context.user_data['project_plan'] = project_plan

            # Показываем первый шаг
            first_step_text = f"""
🎯 **План проекта для: {goal.true_goal}**

{project_plan['content']}

**📝 Шаг 1: Начни с первого пункта**
Расскажи как продвигаешься или задай вопрос!
            """

            await update.message.reply_text(first_step_text)
            return PROJECT_EXECUTION

        else:
            # Возвращаем к выбору
            await update.message.reply_text(
                "Хочешь создать проект для своей цели?",
                reply_markup=self.keyboard_factory.get_yes_no_keyboard()
            )
            return PROJECT_CREATION