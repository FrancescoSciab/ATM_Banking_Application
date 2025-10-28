import sys
import gspread

from cardHolder import cardHolder
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("client_database")

def display_banner():
    print(
        """
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
    )

def print_menu():
    print("1. Check Balance")
    print("2. Withdraw Funds")
    print("3. Deposit Funds")
    print("4. Exit")

def main():
    display_banner()
    #print_menu()
    

if __name__ == "__main__":
    main()