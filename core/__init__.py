from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
import uuid

class UserId:
    \"\"\"Value Object для ID пользователя\"\"\"
    def __init__(self, value: str):
        self.value = str(value)
    
    def __eq__(self, other):
        return isinstance(other, UserId) and self.value == other.value
    
    def __str__(self):
        return self.value

class GoalStatus(Enum):
    DISCOVERED = \"discovered\"
    ACTIVE = \"active\" 
    COMPLETED = \"completed\"
    ARCHIVED = \"archived\"

class ProjectStatus(Enum):
    DRAFT = \"draft\"
    ACTIVE = \"active\"
    COMPLETED = \"completed\"
    CANCELLED = \"cancelled\"

class SubscriptionTier(Enum):
    FREE = \"free\"
    PREMIUM = \"premium\"
    EXPERT = \"expert\"
