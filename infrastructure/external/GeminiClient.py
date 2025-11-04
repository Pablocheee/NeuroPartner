import google.generativeai as genai
import os
import asyncio
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = 'gemini-1.5-flash'
        self.configured = bool(self.api_key)
        self.model = None
        
        if self.configured:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                logger.info('Gemini Client initialized')
            except Exception as e:
                logger.error(f'Gemini init error: {e}')
                self.configured = False
    
    async def is_available(self):
        if not self.configured:
            return False
        try:
            response = await self.process('Test', {})
            return True
        except Exception:
            return False
    
    async def process(self, message, context):
        if not self.configured:
            raise Exception('Gemini not configured')
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.model.generate_content(message)
            )
            return {
                'provider': 'gemini',
                'content': response.text,
                'model': self.model_name,
                'success': True
            }
        except Exception as e:
            raise Exception(f'Gemini error: {str(e)}')
