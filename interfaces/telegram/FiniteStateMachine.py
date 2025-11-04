from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from telegram import Update
from telegram.ext import ContextTypes

# Состояния FSM
WELCOME = \"welcome\"
GOAL_DISCOVERY = \"goal_discovery\" 
VALUE_DEMO = \"value_demo\"
PROJECT_CREATION = \"project_creation\"
PROJECT_EXECUTION = \"project_execution\"
SUCCESS_VALIDATION = \"success_validation\"
SUBSCRIPTION_OFFER = \"subscription_offer\"
LEARNING = \"learning\"
PORTFOLIO = \"portfolio\"
REFERRAL = \"referral\"

class State(ABC):
    \"\"\"Абстрактный класс состояния FSM\"\"\"
    
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.goal_extractor = state_manager.goal_extractor
        self.keyboard_factory = state_manager.keyboard_factory
        self.message_renderer = state_manager.message_renderer
    
    @abstractmethod
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        \"\"\"Обработка сообщения в состоянии\"\"\"
        pass
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        \"\"\"Обработка callback (кнопок)\"\"\"
        query = update.callback_query
        await query.answer()
        return await self.handle_message(update, context)
