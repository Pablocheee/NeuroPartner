import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from interfaces.telegram.FiniteStateMachine import *
from interfaces.telegram.states.WelcomeState import WelcomeState
from interfaces.telegram.states.GoalDiscoveryState import GoalDiscoveryState
from interfaces.telegram.states.ValueDemoState import ValueDemoState
from interfaces.telegram.states.ProjectCreationState import ProjectCreationState
from interfaces.telegram.states.ProjectExecutionState import ProjectExecutionState
from interfaces.telegram.states.SuccessValidationState import SuccessValidationState
from interfaces.telegram.KeyboardFactory import KeyboardFactory
from interfaces.telegram.MessageRenderer import MessageRenderer
from infrastructure.config import settings
from core.goals.GoalExtractor import GoalExtractor

class BotOrchestrator:
    \"\"\"Оркестратор Telegram бота\"\"\"

    def __init__(self):
        self.application = None
        self.state_manager = self
        self.goal_extractor = GoalExtractor()
        self.keyboard_factory = KeyboardFactory()
        self.message_renderer = MessageRenderer()

        # Инициализация репозиториев
        from infrastructure.persistence import UserRepository, GoalRepository, ProjectRepository
        self.user_repository = UserRepository()
        self.goal_repository = GoalRepository()
        self.project_repository = ProjectRepository()

    async def initialize(self):
        \"\"\"Инициализация бота\"\"\"
        self.application = Application.builder().token(settings.telegram_bot_token).build()

        # Настройка обработчиков состояний
        conversation_handler = ConversationHandler(
            entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)],
            states={
                WELCOME: [MessageHandler(filters.TEXT, self._handle_message)],
                GOAL_DISCOVERY: [MessageHandler(filters.TEXT, self._handle_message)],
                VALUE_DEMO: [MessageHandler(filters.TEXT, self._handle_message)],
                PROJECT_CREATION: [MessageHandler(filters.TEXT, self._handle_message)],
                PROJECT_EXECUTION: [MessageHandler(filters.TEXT, self._handle_message)],
                SUCCESS_VALIDATION: [MessageHandler(filters.TEXT, self._handle_message)],
                SUBSCRIPTION_OFFER: [MessageHandler(filters.TEXT, self._handle_message)],
                LEARNING: [MessageHandler(filters.TEXT, self._handle_message)],
                PORTFOLIO: [MessageHandler(filters.TEXT, self._handle_message)],
                REFERRAL: [MessageHandler(filters.TEXT, self._handle_message)],
            },
            fallbacks=[CommandHandler(\"cancel\", self._cancel)],
            initial_state_key=WELCOME
        )

        self.application.add_handler(conversation_handler)
        self.application.add_handler(CommandHandler(\"start\", self._start))

        logging.info(\"🤖 NeuroPartner Bot инициализирован\")

    async def _start(self, update: Update, context: CallbackContext):
        \"\"\"Обработчик команды /start\"\"\"
        # Сбрасываем состояние к приветствию
        context.user_data.clear()
        await update.message.reply_text(\"🌌 Добро пожаловать в NeuroPartner!\"\")
        return WELCOME

    async def _handle_message(self, update: Update, context: CallbackContext):
        \"\"\"Обработчик всех сообщений\"\"\"
        try:
            current_state = context.user_data.get('current_state', WELCOME)

            # Получаем обработчик состояния
            state_handler = self._get_state_handler(current_state)

            # Обрабатываем сообщение
            next_state = await state_handler.handle_message(update, context)

            # Обновляем состояние
            context.user_data['current_state'] = next_state

            return next_state

        except Exception as e:
            logging.error(f\"Ошибка обработки сообщения: {e}\")
            await update.message.reply_text(\"❌ Произошла ошибка. Попробуйте еще раз.\")
            return WELCOME

    async def _cancel(self, update: Update, context: CallbackContext):
        \"\"\"Отмена диалога\"\"\"
        await update.message.reply_text(\"Диалог прерван. Используйте /start чтобы начать заново.\")
        return ConversationHandler.END

    def _get_state_handler(self, state_name: str):
        \"\"\"Получить обработчик состояния\"\"\"
        handlers = {
            WELCOME: WelcomeState(self),
            GOAL_DISCOVERY: GoalDiscoveryState(self),
            VALUE_DEMO: ValueDemoState(self),
            PROJECT_CREATION: ProjectCreationState(self),
            PROJECT_EXECUTION: ProjectExecutionState(self),
            SUCCESS_VALIDATION: SuccessValidationState(self),
            # SUBSCRIPTION_OFFER: SubscriptionOfferState(self),
            # LEARNING: LearningState(self),
            # PORTFOLIO: PortfolioState(self),
            # REFERRAL: ReferralState(self),
        }
        return handlers.get(state_name, WelcomeState(self))

    async def run(self):
        \"\"\"Запуск бота\"\"\"
        await self.application.run_polling()
