from evoting.utils.display import (
    header, subheader, menu_item, pause, clear_screen, error, success
)
from evoting.utils.input import prompt          # ← IMPORTANT: This was missing
from evoting.constants import THEME_ADMIN, THEME_ADMIN_ACCENT, DIM, RESET

def admin_dashboard(store):
    while True:
        clear_screen()
        header("ADMIN DASHBOARD", THEME_ADMIN)
        print(f"  {THEME_ADMIN}  ● {store.current_user.full_name}{RESET}  {DIM}│  Role: {store.current_user.role}{RESET}")

        subheader("Candidate Management", THEME_ADMIN_ACCENT)
        menu_item(1, "Create Candidate", THEME_ADMIN)
        menu_item(2, "View All Candidates", THEME_ADMIN)
        menu_item(3, "Update Candidate", THEME_ADMIN)
        menu_item(4, "Delete Candidate", THEME_ADMIN)
        menu_item(5, "Search Candidates", THEME_ADMIN)

        subheader("Voting Station Management", THEME_ADMIN_ACCENT)
        menu_item(6, "Create Voting Station", THEME_ADMIN)
        menu_item(7, "View All Stations", THEME_ADMIN)
        menu_item(8, "Update Station", THEME_ADMIN)
        menu_item(9, "Delete Station", THEME_ADMIN)

        subheader("Polls & Positions", THEME_ADMIN_ACCENT)
        menu_item(10, "Create Position", THEME_ADMIN)
        menu_item(11, "View Positions", THEME_ADMIN)
        menu_item(12, "Update Position", THEME_ADMIN)
        menu_item(13, "Delete Position", THEME_ADMIN)
        menu_item(14, "Create Poll", THEME_ADMIN)
        menu_item(15, "View All Polls", THEME_ADMIN)
        menu_item(16, "Update Poll", THEME_ADMIN)
        menu_item(17, "Delete Poll", THEME_ADMIN)
        menu_item(18, "Open/Close Poll", THEME_ADMIN)
        menu_item(19, "Assign Candidates to Poll", THEME_ADMIN)

        subheader("Voter Management", THEME_ADMIN_ACCENT)
        menu_item(20, "View All Voters", THEME_ADMIN)
        menu_item(21, "Verify Voter", THEME_ADMIN)
        menu_item(22, "Deactivate Voter", THEME_ADMIN)
        menu_item(23, "Search Voters", THEME_ADMIN)

        subheader("Admin Management", THEME_ADMIN_ACCENT)
        menu_item(24, "Create Admin Account", THEME_ADMIN)
        menu_item(25, "View Admins", THEME_ADMIN)
        menu_item(26, "Deactivate Admin", THEME_ADMIN)

        subheader("Results & Reports", THEME_ADMIN_ACCENT)
        menu_item(27, "View Poll Results", THEME_ADMIN)
        menu_item(28, "View Detailed Statistics", THEME_ADMIN)
        menu_item(29, "View Audit Log", THEME_ADMIN)
        menu_item(30, "Station-wise Results", THEME_ADMIN)

        subheader("System", THEME_ADMIN_ACCENT)
        menu_item(31, "Save Data", THEME_ADMIN)
        menu_item(32, "Logout", THEME_ADMIN)
        print()

        choice = prompt("Enter choice: ")

        # ==================== MENU ROUTING ====================
        if choice == "1":
            store.candidate_manager.create_candidate()
        elif choice == "2":
            store.candidate_manager.view_all_candidates()
        elif choice == "3":
            store.candidate_manager.update_candidate()
        elif choice == "4":
            store.candidate_manager.delete_candidate()
        elif choice == "5":
            store.candidate_manager.search_candidates()

        elif choice == "6":
            store.station_manager.create_voting_station()
        elif choice == "7":
            store.station_manager.view_all_stations()
        elif choice == "8":
            store.station_manager.update_station()
        elif choice == "9":
            store.station_manager.delete_station()

        elif choice == "10":
            store.position_manager.create_position()
        elif choice == "11":
            store.position_manager.view_positions()
        elif choice == "12":
            store.position_manager.update_position()
        elif choice == "13":
            store.position_manager.delete_position()

        elif choice == "14":
            store.poll_manager.create_poll()
        elif choice == "15":
            store.poll_manager.view_all_polls()
        elif choice == "16":
            store.poll_manager.update_poll()
        elif choice == "17":
            store.poll_manager.delete_poll()
        elif choice == "18":
            store.poll_manager.open_close_poll()
        elif choice == "19":
            store.poll_manager.assign_candidates_to_poll()

        elif choice == "20":
            store.voter_manager.view_all_voters()
        elif choice == "21":
            store.voter_manager.verify_voter()
        elif choice == "22":
            store.voter_manager.deactivate_voter()
        elif choice == "23":
            store.voter_manager.search_voters()

        elif choice == "24":
            store.admin_manager.create_admin()
        elif choice == "25":
            store.admin_manager.view_admins()
        elif choice == "26":
            store.admin_manager.deactivate_admin()

        elif choice == "27":
            store.vote_manager.view_poll_results()
        elif choice == "28":
            store.vote_manager.view_detailed_statistics()
        elif choice == "29":
            store.vote_manager.view_audit_log()
        elif choice == "30":
            store.vote_manager.station_wise_results()

        elif choice == "31":
            store.save()
            pause()
        elif choice == "32":
            store.log_action("LOGOUT", store.current_user.username, "Admin logged out")
            store.save()
            break
        else:
            error("Invalid choice.")
            pause()