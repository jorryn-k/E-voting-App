from .base import BaseModel
from datetime import datetime

class Position(BaseModel):
    def __init__(self, id, title, description, level, max_winners, min_candidate_age=25, is_active=True):
        self.id = id
        self.title = title
        self.description = description
        self.level = level
        self.max_winners = max_winners
        self.min_candidate_age = min_candidate_age
        self.is_active = is_active
        self.created_at = datetime.now().isoformat()
        