from datetime import datetime
import hashlib
import json
import os

# Import all models
from .candidate import Candidate
from .voter import Voter
from .admin import Admin
from .voting_station import VotingStation
from .position import Position
from .poll import Poll
from .vote import Vote

# Import managers
from ..managers.candidate_manager import CandidateManager
from ..managers.voter_manager import VoterManager
from ..managers.station_manager import StationManager
from ..managers.admin_manager import AdminManager
from ..managers.position_manager import PositionManager
from ..managers.poll_manager import PollManager
from ..managers.vote_manager import VoteManager

from ..utils.display import info

class DataStore:
    def __init__(self):
        # ==================== DATA COLLECTIONS ====================
        self.candidates = {}
        self.candidate_id_counter = 1

        self.stations = {}
        self.station_id_counter = 1

        self.polls = {}
        self.poll_id_counter = 1

        self.positions = {}
        self.position_id_counter = 1

        self.voters = {}
        self.voter_id_counter = 1

        self.admins = {}
        self.admin_id_counter = 1

        self.votes = []
        self.audit_log = []

        # ==================== CURRENT SESSION ====================
        self.current_user = None
        self.current_role = None

        # ==================== MANAGERS (Dependency Injection) ====================
        self.candidate_manager = CandidateManager(self)
        self.voter_manager = VoterManager(self)
        self.station_manager = StationManager(self)
        self.admin_manager = AdminManager(self)
        self.position_manager = PositionManager(self)
        self.poll_manager = PollManager(self)
        self.vote_manager = VoteManager(self)

    # ==================== DEFAULT ADMIN ====================
    def init_default_admin(self):
        default_password = hashlib.sha256("admin123".encode()).hexdigest()
        self.admins[1] = Admin(
            id=1,
            username="admin",
            password=default_password,
            full_name="System Administrator",
            email="admin@evote.com",
            role="super_admin",
            is_active=True
        )
        self.admin_id_counter = 2
        info("Default admin account created (username: admin | password: admin123)")

    # ==================== PERSISTENCE ====================
    def load_from_dict(self, data):
        """Load everything from evoting_data.json"""
        # Candidates
        for k, v in data.get("candidates", {}).items():
            self.candidates[int(k)] = Candidate.from_dict(v)
        self.candidate_id_counter = data.get("candidate_id_counter", 1)

        # Stations
        for k, v in data.get("voting_stations", {}).items():
            self.stations[int(k)] = VotingStation.from_dict(v)
        self.station_id_counter = data.get("station_id_counter", 1)

        # Polls
        for k, v in data.get("polls", {}).items():
            self.polls[int(k)] = Poll.from_dict(v)
        self.poll_id_counter = data.get("poll_id_counter", 1)

        # Positions
        for k, v in data.get("positions", {}).items():
            self.positions[int(k)] = Position.from_dict(v)
        self.position_id_counter = data.get("position_id_counter", 1)

        # Voters
        for k, v in data.get("voters", {}).items():
            self.voters[int(k)] = Voter.from_dict(v)
        self.voter_id_counter = data.get("voter_id_counter", 1)

        # Admins
        for k, v in data.get("admins", {}).items():
            self.admins[int(k)] = Admin.from_dict(v)
        self.admin_id_counter = data.get("admin_id_counter", 1)

        # Votes
        self.votes = [Vote.from_dict(v) for v in data.get("votes", [])]

        # Audit Log
        self.audit_log = data.get("audit_log", [])

    def save(self):
        """Save to evoting_data.json"""
        from ..persistence import save_data
        save_data(self)

    # ==================== LOGGING ====================
    def log_action(self, action: str, user: str, details: str):
        self.audit_log.append({
            "timestamp": str(datetime.now()),
            "action": action,
            "user": user,
            "details": details
        })
        