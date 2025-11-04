import sys
import os
import json
from cardHolder import API

# Import the API class and test the connection
api = None
try:
    from cardHolder import API
    api = API()
    if api == None:
        print(f"[WARN] Google APIs unavailable")
except Exception as e:
    print(f"[WARN] Failed to import API: {e}")

# Import necessary classes
# If any are unsuccessful assign api to "None" so the program wont continue
try:
    from cardHolder import Account
except Exception as e:
    print(f"[WARN] Failed to import Account: {e}")
    api = None

try:
    from cardHolder import AccountHolder
except Exception as e:
    print(f"[WARN] Failed to import AccountHolder: {e}")
    api = None

try:
    from cardHolder import ATMCard
except Exception as e:
    print(f"[WARN] Failed to import ATMCard: {e}")
    api = None



def print_banner():
    CYAN = "\033[1;36m"
    RESET = "\033[0m"
    if not sys.stdout.isatty() or os.environ.get("TERM") in (None, "dumb"):
        CYAN = RESET = ""
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║               █████╗ ████████╗███╗   ███╗                      ║
    ║              ██╔══██╗╚══██╔══╝████╗ ████║                      ║
    ║              ███████║   ██║   ██╔████╔██║                      ║
    ║              ██╔══██║   ██║   ██║╚██╔╝██║                      ║
    ║              ██║  ██║   ██║   ██║ ╚═╝ ██║                      ║
    ║              ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝                      ║
    ║                                                                ║
    ║                    Welcome to the ATM                          ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(CYAN + banner + RESET)

def print_menu():
    print("Please choose from one of the following options...")
    print("1. Check Balance")
    print("2. Withdraw Funds")
    print("3. Deposit Funds")
    print("4. Exit")

def main():
    print_banner()
    print_menu()
    # Minimal interactive loop so the terminal stays active
    while True:
        try:
            choice = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if choice in ("4", "quit", "exit"):
            print("Goodbye!")
            break
        elif choice in {"1", "2", "3"}:
            print(f"You selected {choice}. This feature is not implemented yet.")
        else:
            print("Invalid option. Please choose 1-4.")
    return

if api != None:
    main()