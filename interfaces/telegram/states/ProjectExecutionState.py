from interfaces.telegram.FiniteStateMachine import State, PROJECT_EXECUTION, SUCCESS_VALIDATION
from telegram import Update
from telegram.ext import ContextTypes
from application.ProjectCoordinatorService import ProjectCoordinatorService

class ProjectExecutionState(State):
    \"\"\"Состояние выполнения шагов проекта\"\"\"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        
        # Получаем текущий шаг и проект
        current_step = context.user_data.get('current_step', 1)
        project = context.user_data.get('current_project')
        goal = context.user_data.get('current_goal')
        
        # Если пользователь завершил шаг
        if \"завершил\" in user_message.lower() or \"готово\" in user_message.lower() or \"сделал\" in user_message.lower():
            current_step += 1
            context.user_data['current_step'] = current_step
            
            if current_step > 3:  # Все шаги завершены
                # Завершаем проект через координатор
                coordinator = ProjectCoordinatorService()
                user_id = str(update.effective_user.id)
                
                results = {
                    'time_saved': 5.0,  # Пример: сэкономил 5 часов
                    'efficiency_gain': 2.0,  # Пример: в 2 раза эффективнее
                    'achievement': f'Достигнута цель: {goal.true_goal}',
                    'metrics': {'quality_score': 8, 'completion_rate': 100}
                }
                
                await coordinator.complete_user_project(user_id, project.id, results)
                
                await update.message.reply_text(\"🎉 Все шаги проекта завершены!\"\")
                return SUCCESS_VALIDATION
            else:
                # Переход к следующему шагу
                await self._show_current_step(update, context, current_step)
                return PROJECT_EXECUTION
        
        else:
            # Показываем текущий шаг
            await self._show_current_step(update, context, current_step)
            return PROJECT_EXECUTION
    
    async def _show_current_step(self, update: Update, context: ContextTypes.DEFAULT_TYPE, step_number: int):
        \"\"\"Показать текущий шаг проекта\"\"\"
        goal = context.user_data.get('current_goal')
        
        step_texts = {
            1: f\"\"\"
🛠️ **Шаг 1: Определение задачи**

Для цели \"{goal.true_goal}\" определи конкретную задачу на сегодня.

💡 **Что будешь делать?** (опиши одним предложением)\"\"\",
            
            2: f\"\"\"
🚀 **Шаг 2: Выполнение**

Отлично! Теперь выполни эту задачу.

💫 **Расскажи как продвигаешься или попроси помощь!**\"\"\",
            
            3: f\"\"\"
🎯 **Шаг 3: Анализ результатов**

Проанализируй что получилось и что можно улучшить.

🤔 **Поделись результатами и выводами!**\"\"\"
        }
        
        text = step_texts.get(step_number, \"🎯 Продолжаем работу над проектом!\")
        
        await update.message.reply_text(
            text,
            reply_markup=self.keyboard_factory.get_step_completion_keyboard()
        )
