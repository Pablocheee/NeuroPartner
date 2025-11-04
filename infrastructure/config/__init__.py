import os
from typing import Optional

class Settings:
    def __init__(self):
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///neuropartner.db')
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.ton_wallet_private_key = os.getenv('TON_WALLET_PRIVATE_KEY', '')

settings = Settings()
