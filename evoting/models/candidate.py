import datetime

from .base import BaseModel
from ..constants import MIN_CANDIDATE_AGE, MAX_CANDIDATE_AGE, REQUIRED_EDUCATION_LEVELS

class Candidate(BaseModel):
    def __init__(self, id, full_name, national_id, date_of_birth, age, gender,
                 education, party, manifesto, address, phone, email,
                 years_experience, is_active=True, is_approved=True, created_by="system"):
        self.id = id
        self.full_name = full_name
        self.national_id = national_id
        self.date_of_birth = date_of_birth
        self.age = age
        self.gender = gender
        self.education = education
        self.party = party
        self.manifesto = manifesto
        self.address = address
        self.phone = phone
        self.email = email
        self.years_experience = years_experience
        self.is_active = is_active
        self.is_approved = is_approved
        self.created_at = datetime.now().isoformat()
        self.created_by = created_by

    def validate(self):
        if not MIN_CANDIDATE_AGE <= self.age <= MAX_CANDIDATE_AGE:
            raise ValueError(f"Age must be between {MIN_CANDIDATE_AGE} and {MAX_CANDIDATE_AGE}")
        if self.education not in REQUIRED_EDUCATION_LEVELS:
            raise ValueError("Invalid education level")