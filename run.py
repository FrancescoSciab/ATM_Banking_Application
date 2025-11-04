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
    print("4. Change PIN")
    print("5. Exit")

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

        if choice in ("5", "quit", "exit"):
            print("Goodbye!")
            break
        elif choice in {"1", "2", "3", "4"}:
            # For all these options we first ask for card number and pin
            try:
                card_num = input("Card number: ").strip()
                pin = input("PIN: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nOperation cancelled")
                continue

            try:
                cards = api.getATMCards(card_num)
            except Exception as e:
                print(f"Error looking up card: {e}")
                continue

            if not cards:
                print("Card not found.")
                continue

            card = cards[0]

            # Authenticate
            if not card.verify_pin(pin):
                print("Incorrect PIN.")
                # Optionally show failed tries
                try:
                    print(f"Failed tries: {card.getFailedTries()}")
                except:
                    pass
                continue

            # Authenticated: handle actions
            if choice == "1":
                bal = card.check_balance()
                if bal is None:
                    print("Could not retrieve balance.")
                else:
                    print(f"Current balance: {bal:.2f}")

            elif choice == "2":
                try:
                    amt = float(input("Amount to withdraw: ").strip())
                except Exception:
                    print("Invalid amount")
                    continue
                if amt <= 0:
                    print("Amount must be positive")
                    continue
                success = card.withdraw(amt)
                if success:
                    print(f"Withdrawn {amt:.2f}. New balance: {card.check_balance():.2f}")
                else:
                    print("Withdrawal failed (insufficient funds or server error).")

            elif choice == "3":
                try:
                    amt = float(input("Amount to deposit: ").strip())
                except Exception:
                    print("Invalid amount")
                    continue
                if amt <= 0:
                    print("Amount must be positive")
                    continue
                success = card.deposit(amt)
                if success:
                    print(f"Deposited {amt:.2f}. New balance: {card.check_balance():.2f}")
                else:
                    print("Deposit failed (server error).")

            elif choice == "4":
                try:
                    new_pin = input("Enter new PIN: ").strip()
                    confirm = input("Confirm new PIN: ").strip()
                except Exception:
                    print("Input cancelled")
                    continue
                if new_pin != confirm:
                    print("PIN mismatch. Try again.")
                    continue
                if not new_pin.isdigit():
                    print("PIN must be numeric")
                    continue
                success = card.change_pin(new_pin)
                if success:
                    print("PIN changed successfully.")
                else:
                    print("Failed to change PIN.")
            else:
                print("Unhandled option")
        else:
            print("Invalid option. Please choose 1-5.")
    return

if api != None:
    main()