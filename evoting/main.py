from evoting.utils.display import clear_screen
from evoting.persistence import load_data
from evoting.ui.authentication import login
from evoting.models.data_store import DataStore
from evoting.constants import*

def main():
    store = DataStore()
    print(f"\n  {THEME_LOGIN}Loading E-Voting System...{RESET}")
    load_data(store)                    # This calls store.load_from_dict

    while True:
        clear_screen()
        logged_in = login(store)
        if logged_in:
            if store.current_role == "admin":
                from evoting.ui.admin_dashboard import admin_dashboard
                admin_dashboard(store)
            elif store.current_role == "voter":
                from evoting.ui.voter_dashboard import voter_dashboard
                voter_dashboard(store)
            # Reset session
            store.current_user = None
            store.current_role = None
        store.save()                        # Auto-save after every action

if __name__ == "__main__":
    main()