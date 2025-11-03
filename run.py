import sys
import os
import json

# Google Sheets is optional
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GOOGLE_OK = True
except Exception as e:
    print(f"[WARN] Google APIs unavailable: {e}")
    gspread = Credentials = None
    GOOGLE_OK = False

try:
    from cardHolder import cardHolder
except Exception as e:
    print(f"[WARN] Failed to import cardHolder: {e}")
    class cardHolder:  # noqa: N801
        pass

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

SHEET = None
if GOOGLE_OK:
    try:
        # Prefer CREDS env var in Render/local; fallback to creds.json if present
        if os.environ.get("CREDS"):
            info = json.loads(os.environ["CREDS"])
            creds = Credentials.from_service_account_info(info)
        elif os.path.exists("creds.json"):
            creds = Credentials.from_service_account_file("creds.json")
        else:
            raise FileNotFoundError("No Google credentials provided (CREDS env or creds.json)")

        scoped = creds.with_scopes(SCOPE)
        client = gspread.authorize(scoped)
        SHEET = client.open("client_database")
    except Exception as e:
        print(f"[WARN] Google Sheets disabled: {e}")
else:
    print("[WARN] Google libraries not available; running without Sheets.")

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

if __name__ == "__main__":
    main()