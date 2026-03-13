import json
import os
from datetime import datetime

DATA_FILE = "evoting_data.json"

def save_data(store):
    data = {
        "candidates": {k: v.to_dict() for k, v in store.candidates.items()},
        "candidate_id_counter": store.candidate_id_counter,
        "voting_stations": {k: v.to_dict() for k, v in store.stations.items()},
        "station_id_counter": store.station_id_counter,
        "polls": {k: v.to_dict() for k, v in store.polls.items()},
        "poll_id_counter": store.poll_id_counter,
        "positions": {k: v.to_dict() for k, v in store.positions.items()},
        "position_id_counter": store.position_id_counter,
        "voters": {k: v.to_dict() for k, v in store.voters.items()},
        "voter_id_counter": store.voter_id_counter,
        "admins": {k: v.to_dict() for k, v in store.admins.items()},
        "admin_id_counter": store.admin_id_counter,
        "votes": [v.to_dict() for v in store.votes],
        "audit_log": store.audit_log
    }
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print("  Data saved successfully")
    except Exception as e:
        print(f"  Error saving: {e}")

def load_data(store):
    if not os.path.exists(DATA_FILE):
        store.init_default_admin()
        return
    try:
        with open(DATA_FILE) as f:
            raw = json.load(f)
        store.load_from_dict(raw)
        print("  Data loaded successfully")
    except Exception as e:
        print(f"  Error loading: {e}")