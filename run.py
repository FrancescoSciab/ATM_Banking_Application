import sys
import gspread
from google.oauth2.service_account import Credentials

try:
    from cardHolder import cardHolder
except Exception as e:
    print(f"[WARN] Failed to import cardHolder: {e}")
    # Minimal placeholder to keep the app running; replace after fixing cardHolder.py
    class cardHolder:  # noqa: N801
        pass

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Replace the direct initialization with a safe try/except:
try:
    CREDS = Credentials.from_service_account_file("creds.json")
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open("client_database")
except Exception as e:
    print(f"[WARN] Google Sheets disabled: {e}")
    CREDS = SCOPED_CREDS = None
    GSPREAD_CLIENT = SHEET = None


def print_banner():
    import os, sys
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
    return

if __name__ == "__main__":
    main()