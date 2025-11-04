from interfaces.telegram.FiniteStateMachine import State, WELCOME, GOAL_DISCOVERY
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

class WelcomeState(State):
    \"\"\"Состояние приветствия и первого знакомства\"\"\"
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_message = update.message.text
        
        # Сохраняем контекст первого сообщения
        context.user_data['first_message'] = user_message
        
        # Человеческое приветствие
        welcome_text = \"\"\"
👋 Привет! Я твой AI-партнер NeuroPartner.

Расскажи, над чем сейчас работаешь или о чем мечтаешь?

💫 Например:
• \"Хочу запустить онлайн-курс\"
• \"Нужно увеличить продажи\"  
• \"Мечтаю создать свое приложение\"
• \"Хочу научиться маркетингу\"
        \"\"\"
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Переход к выявлению целей
        return GOAL_DISCOVERY
