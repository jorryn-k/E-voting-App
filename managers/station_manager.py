from evoting.utils.display import (
    header, subheader, table_header, table_divider,
    error, success, warning, info, pause, status_badge
)
from evoting.utils.input import prompt
from evoting.models.voting_station import VotingStation
from evoting.constants import* 

class StationManager:
    def __init__(self, store):
        self.store = store

    # ──────────────────────────────────────────────────────────────
    # CREATE VOTING STATION
    # ──────────────────────────────────────────────────────────────
    def create_voting_station(self):
        header("CREATE VOTING STATION", THEME_ADMIN)
        print()

        name = prompt("Station Name: ")
        if not name:
            error("Name cannot be empty.")
            pause()
            return

        location = prompt("Location/Address: ")
        if not location:
            error("Location cannot be empty.")
            pause()
            return

        region = prompt("Region/District: ")

        try:
            capacity = int(prompt("Voter Capacity: "))
            if capacity <= 0:
                error("Capacity must be positive.")
                pause()
                return
        except ValueError:
            error("Invalid capacity.")
            pause()
            return

        supervisor = prompt("Station Supervisor Name: ")
        contact = prompt("Contact Phone: ")
        opening_time = prompt("Opening Time (e.g. 08:00): ")
        closing_time = prompt("Closing Time (e.g. 17:00): ")

        station = VotingStation(
            id=self.store.station_id_counter,
            name=name,
            location=location,
            region=region,
            capacity=capacity,
            supervisor=supervisor,
            contact=contact,
            opening_time=opening_time,
            closing_time=closing_time,
            is_active=True
        )

        self.store.stations[self.store.station_id_counter] = station
        self.store.station_id_counter += 1

        self.store.log_action("CREATE_STATION", self.store.current_user.username,
                              f"Created station: {name} (ID: {station.id})")
        success(f"Voting Station '{name}' created! ID: {station.id}")
        self.store.save()
        pause()

    # ──────────────────────────────────────────────────────────────
    # VIEW ALL STATIONS
    # ──────────────────────────────────────────────────────────────
    def view_all_stations(self):
        header("ALL VOTING STATIONS", THEME_ADMIN)
        if not self.store.stations:
            info("No voting stations found.")
            pause()
            return

        print()
        table_header(f"{'ID':<5} {'Name':<25} {'Location':<25} {'Region':<15} {'Cap.':<8} {'Reg.':<8} {'Status':<10}", THEME_ADMIN)
        table_divider(96, THEME_ADMIN)

        for sid, s in self.store.stations.items():
            reg_count = sum(1 for v in self.store.voters.values() if v.station_id == sid)
            status = status_badge("Active", True) if s.is_active else status_badge("Inactive", False)
            print(f"  {s.id:<5} {s.name:<25} {s.location:<25} {s.region:<15} {s.capacity:<8} {reg_count:<8} {status}")

        print(f"\n  {DIM}Total Stations: {len(self.store.stations)}{RESET}")
        pause()

    # ──────────────────────────────────────────────────────────────
    # UPDATE STATION
    # ──────────────────────────────────────────────────────────────
    def update_station(self):
        header("UPDATE VOTING STATION", THEME_ADMIN)
        if not self.store.stations:
            info("No stations found.")
            pause()
            return

        print()
        for sid, s in self.store.stations.items():
            print(f"  {THEME_ADMIN}{s.id}.{RESET} {s.name} {DIM}- {s.location}{RESET}")

        try:
            sid = int(prompt("\nEnter Station ID to update: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if sid not in self.store.stations:
            error("Station not found.")
            pause()
            return

        s = self.store.stations[sid]
        print(f"\n  {BOLD}Updating: {s.name}{RESET}")
        info("Press Enter to keep current value\n")

        new_name = prompt(f"Name [{s.name}]: ")
        if new_name:
            s.name = new_name
        new_location = prompt(f"Location [{s.location}]: ")
        if new_location:
            s.location = new_location
        new_region = prompt(f"Region [{s.region}]: ")
        if new_region:
            s.region = new_region
        new_capacity = prompt(f"Capacity [{s.capacity}]: ")
        if new_capacity:
            try:
                s.capacity = int(new_capacity)
            except ValueError:
                warning("Invalid number, keeping old value.")
        new_supervisor = prompt(f"Supervisor [{s.supervisor}]: ")
        if new_supervisor:
            s.supervisor = new_supervisor
        new_contact = prompt(f"Contact [{s.contact}]: ")
        if new_contact:
            s.contact = new_contact

        self.store.log_action("UPDATE_STATION", self.store.current_user.username,
                              f"Updated station: {s.name} (ID: {sid})")
        success(f"Station '{s.name}' updated successfully!")
        self.store.save()
        pause()

    # ──────────────────────────────────────────────────────────────
    # DELETE / DEACTIVATE STATION
    # ──────────────────────────────────────────────────────────────
    def delete_station(self):
        header("DELETE VOTING STATION", THEME_ADMIN)
        if not self.store.stations:
            info("No stations found.")
            pause()
            return

        print()
        for sid, s in self.store.stations.items():
            status = status_badge("Active", True) if s.is_active else status_badge("Inactive", False)
            print(f"  {THEME_ADMIN}{s.id}.{RESET} {s.name} {DIM}({s.location}){RESET} {status}")

        try:
            sid = int(prompt("\nEnter Station ID to delete: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if sid not in self.store.stations:
            error("Station not found.")
            pause()
            return

        voter_count = sum(1 for v in self.store.voters.values() if v.station_id == sid)
        if voter_count > 0:
            warning(f"{voter_count} voters are registered at this station.")
            if prompt("Proceed with deactivation? (yes/no): ").lower() != "yes":
                info("Cancelled.")
                pause()
                return

        if prompt(f"Confirm deactivation of '{self.store.stations[sid].name}'? (yes/no): ").lower() == "yes":
            self.store.stations[sid].is_active = False
            self.store.log_action("DELETE_STATION", self.store.current_user.username,
                                  f"Deactivated station: {self.store.stations[sid].name}")
            success(f"Station '{self.store.stations[sid].name}' deactivated.")
            self.store.save()
        else:
            info("Cancelled.")
        pause()
        