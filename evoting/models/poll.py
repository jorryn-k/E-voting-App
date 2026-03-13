from .base import BaseModel
from datetime import datetime

class Poll(BaseModel):
    def __init__(self, id, title, description, election_type, start_date, end_date,
                 positions=None, station_ids=None, status="draft", total_votes_cast=0):
        self.id = id
        self.title = title
        self.description = description
        self.election_type = election_type
        self.start_date = start_date
        self.end_date = end_date
        self.positions = positions or []
        self.station_ids = station_ids or []
        self.status = status
        self.total_votes_cast = total_votes_cast
        self.created_at = datetime.now().isoformat()