from .base import BaseModel
from datetime import datetime

class VotingStation(BaseModel):
    def __init__(self, id, name, location, region, capacity, supervisor, contact,
                 opening_time, closing_time, is_active=True):
        self.id = id
        self.name = name
        self.location = location
        self.region = region
        self.capacity = capacity
        self.registered_voters = 0
        self.supervisor = supervisor
        self.contact = contact
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.is_active = is_active
        self.created_at = datetime.now().isoformat()