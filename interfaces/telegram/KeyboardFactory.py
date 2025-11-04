from telegram import ReplyKeyboardMarkup, KeyboardButton
from typing import Dict, Any

class KeyboardFactory:
    \"\"\"Фабрика клавиатур для Telegram бота\"\"\"
    
    def get_main_menu(self, user_context: Dict[str, Any]) -> ReplyKeyboardMarkup:
        \"\"\"Главное меню\"\"\"
        keyboard = [
            [\"🛸 Мои проекты\", \"🌌 Прогресс\"],
            [\"🎯 Текущая цель\", \"🚀 Новый проект\"],
            [\"👥 Пригласить друзей\", \"⚙️ Настройки\"]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    def get_yes_no_keyboard(self) -> ReplyKeyboardMarkup:
        \"\"\"Клавиатура Да/Нет\"\"\"
        keyboard = [[\"✅ Да\", \"❌ Нет\"]]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    def get_project_creation_keyboard(self) -> ReplyKeyboardMarkup:
        \"\"\"Клавиатура создания проекта\"\"\"
        keyboard = [
            [\"🚀 Создать проект\", \"🤖 Усилить AI\"],
            [\"🏠 В главное меню\"]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    def get_project_actions(self, project) -> ReplyKeyboardMarkup:
        \"\"\"Клавиатура управления проектом\"\"\"
        keyboard = [
            [\"▶️ Продолжить проект\", \"📊 Результаты\"],
            [\"🤖 AI Аналитика\", \"📋 Инструкции\"],
            [\"🏠 В главное меню\"]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    def get_subscription_offer(self) -> ReplyKeyboardMarkup:
        \"\"\"Клавиатура предложения подписки\"\"\"
        keyboard = [
            [\"💫 NeuroPartner Premium (10 TON)\", \"👥 Пригласить 3 друзей\"],
            [\"🚫 Пока не хочу\", \"🛰️ Узнать больше\"]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
