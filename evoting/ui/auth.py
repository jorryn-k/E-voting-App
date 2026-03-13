from evoting.utils.display import header, error, success, warning, info, pause, clear_screen, menu_item
from evoting.utils.input import prompt, masked_input
from evoting.constants import THEME_LOGIN, THEME_ADMIN, THEME_VOTER
import hashlib

def login(store):
    clear_screen()
    header("E-VOTING SYSTEM", THEME_LOGIN)
    print()
    menu_item(1, "Login as Admin", THEME_LOGIN)
    menu_item(2, "Login as Voter", THEME_LOGIN)
    menu_item(3, "Register as Voter", THEME_LOGIN)
    menu_item(4, "Exit", THEME_LOGIN)
    print()
    choice = prompt("Enter choice: ")

    if choice == "1":
        return admin_login(store)
    elif choice == "2":
        return voter_login(store)
    elif choice == "3":
        store.voter_manager.create_voter()
        return False
    elif choice == "4":
        info("Goodbye!")
        store.save()
        exit()
    else:
        error("Invalid choice.")
        pause()
        return False

def admin_login(store):
    clear_screen()
    header("ADMIN LOGIN", THEME_ADMIN)
    username = prompt("Username: ")
    password = masked_input("Password: ").strip()
    hashed = hashlib.sha256(password.encode()).hexdigest()

    for admin in store.admins.values():
        if admin.username == username and admin.password == hashed and admin.is_active:
            store.current_user = admin
            store.current_role = "admin"
            store.log_action("LOGIN", username, "Admin login successful")
            success(f"Welcome, {admin.full_name}!")
            pause()
            return True
    error("Invalid credentials.")
    store.log_action("LOGIN_FAILED", username, "Invalid admin credentials")
    pause()
    return False

def voter_login(store):
    clear_screen()
    header("VOTER LOGIN", THEME_VOTER)
    card = prompt("Voter Card Number: ")
    password = masked_input("Password: ").strip()
    hashed = hashlib.sha256(password.encode()).hexdigest()

    for voter in store.voters.values():
        if voter.voter_card_number == card and voter.password == hashed:
            if not voter.is_active:
                error("Account deactivated.")
                pause()
                return False
            if not voter.is_verified:
                warning("Registration not verified yet.")
                info("Contact an admin.")
                pause()
                return False
            store.current_user = voter
            store.current_role = "voter"
            store.log_action("LOGIN", card, "Voter login successful")
            success(f"Welcome, {voter.full_name}!")
            pause()
            return True
    error("Invalid card or password.")
    pause()
    return False