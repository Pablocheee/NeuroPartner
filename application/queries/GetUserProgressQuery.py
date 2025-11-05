from core.learning import LearningProgress
from infrastructure.persistence import UserRepository

class GetUserProgressQuery:
    \"\"\"Запрос получения прогресса пользователя\"\"\"
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: str) -> LearningProgress:
        \"\"\"Получить прогресс обучения пользователя\"\"\"
        user = await self.user_repository.get_by_id(user_id)
        return user.learning_progress if user else LearningProgress()
