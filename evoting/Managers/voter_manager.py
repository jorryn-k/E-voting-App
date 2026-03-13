from evoting.utils.display import (
    header, subheader, table_header, table_divider,
    error, success, warning, info, pause, status_badge, menu_item
)
from evoting.utils.input import masked_input, prompt
from evoting.models.voter import Voter
from evoting.constants import* 
import datetime
import random
import string
import hashlib

class VoterManager:
    def __init__(self, store):
        self.store = store

    # ──────────────────────────────────────────────────────────────
    # CREATE / REGISTER VOTER (used by auth.py and admin if needed)
    # ──────────────────────────────────────────────────────────────
    def create_voter(self):
        """Called from register_voter in auth.py or could be used by admin"""
        header("VOTER REGISTRATION", THEME_ADMIN if self.store.current_role == "admin" else THEME_ADMIN)  # reuse same UI
        print()

        full_name = prompt("Full Name: ")
        if not full_name:
            error("Name cannot be empty.")
            pause()
            return

        national_id = prompt("National ID Number: ")
        if not national_id:
            error("National ID cannot be empty.")
            pause()
            return

        for v in self.store.voters.values():
            if v.national_id == national_id:
                error("A voter with this National ID already exists.")
                pause()
                return

        dob_str = prompt("Date of Birth (YYYY-MM-DD): ")
        try:
            dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d")
            age = (datetime.datetime.now() - dob).days // 365
            if age < MIN_VOTER_AGE:
                error(f"You must be at least {MIN_VOTER_AGE} years old to register.")
                pause()
                return
        except ValueError:
            error("Invalid date format.")
            pause()
            return

        gender = prompt("Gender (M/F/Other): ").upper()
        if gender not in ["M", "F", "OTHER"]:
            error("Invalid gender selection.")
            pause()
            return

        address = prompt("Residential Address: ")
        phone = prompt("Phone Number: ")
        email = prompt("Email Address: ")
        password = masked_input("Create Password: ").strip()  # from utils.input (already imported in auth, but we can import again)
        if len(password) < 6:
            error("Password must be at least 6 characters.")
            pause()
            return

        confirm_password = masked_input("Confirm Password: ").strip()
        if password != confirm_password:
            error("Passwords do not match.")
            pause()
            return

        if not self.store.stations:
            error("No voting stations available. Contact admin.")
            pause()
            return

        subheader("Available Voting Stations", THEME_ADMIN_ACCENT)
        for sid, station in self.store.stations.items():
            if station.is_active:
                print(f"    {THEME_ADMIN}{sid}.{RESET} {station.name} {DIM}- {station.location}{RESET}")

        try:
            station_choice = int(prompt("\nSelect your voting station ID: "))
            if station_choice not in self.store.stations or not self.store.stations[station_choice].is_active:
                error("Invalid station selection.")
                pause()
                return
        except ValueError:
            error("Invalid input.")
            pause()
            return

        voter_card = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

        voter = Voter(
            id=self.store.voter_id_counter,
            full_name=full_name,
            national_id=national_id,
            date_of_birth=dob_str,
            age=age,
            gender=gender,
            address=address,
            phone=phone,
            email=email,
            password=hashlib.sha256(password.encode()).hexdigest(),
            voter_card_number=voter_card,
            station_id=station_choice,
            is_verified=False,
            is_active=True,
            has_voted_in=[],
            registered_at=str(datetime.datetime.now())
        )

        self.store.voters[self.store.voter_id_counter] = voter
        self.store.voter_id_counter += 1

        self.store.log_action("REGISTER", full_name, f"New voter registered with card: {voter_card}")
        success("Registration successful!")
        print(f"  {BOLD}Your Voter Card Number: {BRIGHT_YELLOW}{voter_card}{RESET}")
        warning("IMPORTANT: Save this number! You need it to login.")
        info("Your registration is pending admin verification.")
        self.store.save()
        pause()

    # ──────────────────────────────────────────────────────────────
    # VIEW ALL VOTERS
    # ──────────────────────────────────────────────────────────────
    def view_all_voters(self):
        header("ALL REGISTERED VOTERS", THEME_ADMIN)
        if not self.store.voters:
            info("No voters registered.")
            pause()
            return

        print()
        table_header(f"{'ID':<5} {'Name':<25} {'Card Number':<15} {'Stn':<6} {'Verified':<10} {'Active':<8}", THEME_ADMIN)
        table_divider(70, THEME_ADMIN)

        for vid, v in self.store.voters.items():
            verified = status_badge("Yes", True) if v.is_verified else status_badge("No", False)
            active = status_badge("Yes", True) if v.is_active else status_badge("No", False)
            print(f"  {v.id:<5} {v.full_name:<25} {v.voter_card_number:<15} {v.station_id:<6} {verified:<19} {active}")

        verified_count = sum(1 for v in self.store.voters.values() if v.is_verified)
        unverified_count = sum(1 for v in self.store.voters.values() if not v.is_verified)
        print(f"\n  {DIM}Total: {len(self.store.voters)}  │  Verified: {verified_count}  │  Unverified: {unverified_count}{RESET}")
        pause()

    # ──────────────────────────────────────────────────────────────
    # VERIFY VOTER
    # ──────────────────────────────────────────────────────────────
    def verify_voter(self):
        header("VERIFY VOTER", THEME_ADMIN)
        unverified = {vid: v for vid, v in self.store.voters.items() if not v.is_verified}
        if not unverified:
            info("No unverified voters.")
            pause()
            return

        subheader("Unverified Voters", THEME_ADMIN_ACCENT)
        for vid, v in unverified.items():
            print(f"  {THEME_ADMIN}{v.id}.{RESET} {v.full_name} {DIM}│ NID: {v.national_id} │ Card: {v.voter_card_number}{RESET}")

        print()
        menu_item(1, "Verify a single voter", THEME_ADMIN)
        menu_item(2, "Verify all pending voters", THEME_ADMIN)
        choice = prompt("\nChoice: ")

        if choice == "1":
            try:
                vid = int(prompt("Enter Voter ID: "))
            except ValueError:
                error("Invalid input.")
                pause()
                return
            if vid not in self.store.voters:
                error("Voter not found.")
                pause()
                return
            if self.store.voters[vid].is_verified:
                info("Already verified.")
                pause()
                return

            self.store.voters[vid].is_verified = True
            self.store.log_action("VERIFY_VOTER", self.store.current_user.username,
                                  f"Verified voter: {self.store.voters[vid].full_name}")
            success(f"Voter '{self.store.voters[vid].full_name}' verified!")
            self.store.save()

        elif choice == "2":
            count = 0
            for vid in unverified:
                self.store.voters[vid].is_verified = True
                count += 1
            self.store.log_action("VERIFY_ALL_VOTERS", self.store.current_user.username,
                                  f"Verified {count} voters")
            success(f"{count} voters verified!")
            self.store.save()

        pause()

    # ──────────────────────────────────────────────────────────────
    # DEACTIVATE VOTER
    # ──────────────────────────────────────────────────────────────
    def deactivate_voter(self):
        header("DEACTIVATE VOTER", THEME_ADMIN)
        if not self.store.voters:
            info("No voters found.")
            pause()
            return

        try:
            vid = int(prompt("Enter Voter ID to deactivate: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if vid not in self.store.voters:
            error("Voter not found.")
            pause()
            return

        if not self.store.voters[vid].is_active:
            info("Already deactivated.")
            pause()
            return

        if prompt(f"Deactivate '{self.store.voters[vid].full_name}'? (yes/no): ").lower() == "yes":
            self.store.voters[vid].is_active = False
            self.store.log_action("DEACTIVATE_VOTER", self.store.current_user.username,
                                  f"Deactivated voter: {self.store.voters[vid].full_name}")
            success("Voter deactivated.")
            self.store.save()
        pause()

    # ──────────────────────────────────────────────────────────────
    # SEARCH VOTERS
    # ──────────────────────────────────────────────────────────────
    def search_voters(self):
        header("SEARCH VOTERS", THEME_ADMIN)
        subheader("Search by", THEME_ADMIN_ACCENT)
        menu_item(1, "Name", THEME_ADMIN)
        menu_item(2, "Voter Card Number", THEME_ADMIN)
        menu_item(3, "National ID", THEME_ADMIN)
        menu_item(4, "Station", THEME_ADMIN)
        choice = prompt("\nChoice: ")

        results = []
        if choice == "1":
            term = prompt("Name: ").lower()
            results = [v for v in self.store.voters.values() if term in v.full_name.lower()]
        elif choice == "2":
            term = prompt("Card Number: ")
            results = [v for v in self.store.voters.values() if term == v.voter_card_number]
        elif choice == "3":
            term = prompt("National ID: ")
            results = [v for v in self.store.voters.values() if term == v.national_id]
        elif choice == "4":
            try:
                sid = int(prompt("Station ID: "))
                results = [v for v in self.store.voters.values() if v.station_id == sid]
            except ValueError:
                error("Invalid input.")
                pause()
                return
        else:
            error("Invalid choice.")
            pause()
            return

        if not results:
            info("No voters found.")
        else:
            print(f"\n  {BOLD}Found {len(results)} voter(s):{RESET}")
            for v in results:
                verified = status_badge("Verified", True) if v.is_verified else status_badge("Unverified", False)
                print(f"  {THEME_ADMIN}ID:{RESET} {v.id}  {DIM}│{RESET}  {v.full_name}  {DIM}│  Card:{RESET} {v.voter_card_number}  {DIM}│{RESET}  {verified}")

        pause()
        