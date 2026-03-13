from evoting.utils.display import header, info, menu_item, pause, clear_screen, error
from evoting.constants import THEME_VOTER, DIM, RESET
from evoting.utils.input import prompt

def voter_dashboard(store):
    while True:
        clear_screen()
        header("VOTER DASHBOARD", THEME_VOTER)
        station_name = store.stations.get(store.current_user.station_id, {}).name if hasattr(store.current_user, 'station_id') else "Unknown"
        print(f"  {THEME_VOTER}  ● {store.current_user.full_name}{RESET}")
        print(f"  {DIM}    Card: {store.current_user.voter_card_number}  │  Station: {station_name}{RESET}")

        menu_item(1, "View Open Polls", THEME_VOTER)
        menu_item(2, "Cast Vote", THEME_VOTER)
        menu_item(3, "View My Voting History", THEME_VOTER)
        menu_item(4, "View Results (Closed Polls)", THEME_VOTER)
        menu_item(5, "View My Profile", THEME_VOTER)
        menu_item(6, "Change Password", THEME_VOTER)
        menu_item(7, "Logout", THEME_VOTER)

        choice = prompt("Enter choice: ")

        if choice == "1": store.vote_manager.view_open_polls()
        elif choice == "2": store.vote_manager.cast_vote()
        elif choice == "3": store.vote_manager.view_voting_history()
        elif choice == "4": store.vote_manager.view_closed_poll_results()
        elif choice == "5": view_profile(store)
        elif choice == "6": change_password(store)
        elif choice == "7":
            store.log_action("LOGOUT", store.current_user.voter_card_number, "Voter logged out")
            store.save()
            break
        else:
            error("Invalid choice.")
            pause()

def view_profile(store):
    # Simple profile view (you can expand if needed)
    v = store.current_user
    print(f"\n  Name: {v.full_name}\n  Card: {v.voter_card_number}\n  Station: {v.station_id}\n  Verified: {'Yes' if v.is_verified else 'No'}")
    pause()

def change_password(store):
    # You can add this later if you want – for now it’s optional
    info("Password change feature coming in next update.")
    pause()