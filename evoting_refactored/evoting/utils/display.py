from evoting_refactored.constants import *

def colored(text, color):
    return f"{color}{text}{RESET}"

def header(title, theme_color):
    width = 58
    top = f"  {theme_color}{'═' * width}{RESET}"
    mid = f"  {theme_color}{BOLD} {title.center(width - 2)} {RESET}{theme_color} {RESET}"
    bot = f"  {theme_color}{'═' * width}{RESET}"
    print(top)
    print(mid)
    print(bot)

def subheader(title, theme_color):
    print(f"\n  {theme_color}{BOLD}▸ {title}{RESET}")

def table_header(format_str, theme_color):
    print(f"  {theme_color}{BOLD}{format_str}{RESET}")

def table_divider(width, theme_color):
    print(f"  {theme_color}{'─' * width}{RESET}")

def error(msg):
    print(f"  {RED}{BOLD} {msg}{RESET}")

def success(msg):
    print(f"  {GREEN}{BOLD} {msg}{RESET}")

def warning(msg):
    print(f"  {YELLOW}{BOLD} {msg}{RESET}")

def info(msg):
    print(f"  {GRAY}{msg}{RESET}")

def menu_item(number, text, color):
    print(f"  {color}{BOLD}{number:>3}.{RESET}  {text}")

def status_badge(text, is_good):
    return f"{GREEN}{text}{RESET}" if is_good else f"{RED}{text}{RESET}"

def pause():
    input(f"\n  {DIM}Press Enter to continue...{RESET}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')