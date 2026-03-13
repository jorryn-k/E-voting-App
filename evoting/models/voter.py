from .base import BaseModel
from datetime import datetime
from ..constants import MIN_VOTER_AGE

class Voter(BaseModel):
    def __init__(self, id, full_name, national_id, date_of_birth, age, gender, address,
                 phone, email, password, voter_card_number, station_id,
                 is_verified=False, is_active=True, has_voted_in=None, registered_at=None):
        self.id = id
        self.full_name = full_name
        self.national_id = national_id
        self.date_of_birth = date_of_birth
        self.age = age
        self.gender = gender
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.voter_card_number = voter_card_number
        self.station_id = station_id
        self.is_verified = is_verified
        self.is_active = is_active
        self.has_voted_in = has_voted_in or []
        self.registered_at = registered_at or datetime.now().isoformat()

    def validate(self):
        if self.age < MIN_VOTER_AGE:
            raise ValueError(f"Must be at least {MIN_VOTER_AGE} years old")