from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta
from . import SubscriptionTier

@dataclass
class Subscription:
    \"\"\"Доменная модель подписки\"\"\"
    user_id: str
    tier: SubscriptionTier = SubscriptionTier.FREE
    started_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    auto_renew: bool = False
    payment_method: str = \"ton_crypto\"
    
    def is_active(self) -> bool:
        \"\"\"Проверка активной подписки\"\"\"
        if self.tier == SubscriptionTier.FREE:
            return True
        return self.expires_at and self.expires_at > datetime.now()
    
    def upgrade(self, new_tier: SubscriptionTier, duration_days: int = 30) -> None:
        \"\"\"Обновление подписки\"\"\"
        self.tier = new_tier
        self.expires_at = datetime.now() + timedelta(days=duration_days)
    
    def days_remaining(self) -> int:
        \"\"\"Дней до окончания подписки\"\"\"
        if not self.expires_at:
            return 0
        return (self.expires_at - datetime.now()).days
