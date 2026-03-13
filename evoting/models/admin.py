from .base import BaseModel
from datetime import datetime

class Admin(BaseModel):
    def __init__(self, id, username, password, full_name, email, role, is_active=True):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.role = role
        self.is_active = is_active
        self.created_at = datetime.now().isoformat()