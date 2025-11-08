import sys
import os
import json
from cardHolder import API, show_welcome_message, transfer_money

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

# Import repo for the single-sheet format
try:
    from cardHolder import SimpleClientRepo
    repo = SimpleClientRepo()
except Exception as _:
    repo = None



def print_banner():
    CYAN = "\033[1;36m"
    RESET = "\033[0m"
    if not sys.stdout.isatty() or os.environ.get("TERM") in (None, "dumb"):
        CYAN = RESET = ""
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║                    █████╗ ████████╗███╗   ███╗                 ║
    ║                   ██╔══██╗╚══██╔══╝████╗ ████║                 ║
    ║                   ███████║   ██║   ██╔████╔██║                 ║
    ║                   ██╔══██║   ██║   ██║╚██╔╝██║                 ║
    ║                   ██║  ██║   ██║   ██║ ╚═╝ ██║                 ║
    ║                   ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝                 ║
    ║                                                                ║
    ║                         Welcome to the ATM                     ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(CYAN + banner + RESET)
    print(f"               Secure • Fast • 24/7 Access | Card-Only Banking{RESET}")
    print()

def print_menu():
    print("Please choose from one of the following options...")
    print("1. Check Balance")
    print("2. Withdraw Funds")
    print("3. Deposit Funds")
    print("4. Change PIN")
    print("5. Transfer Money")
    print("6. Exit")

def authenticate(api):
    """Prompt for card and PIN first, return a tuple (source, obj) or None.
    source: 'api' for ATMCard via API, 'repo' for ClientRecord via SimpleClientRepo
    """
    attempts = 0
    while attempts < 3:
        try:
            card_num = input("Insert Your Card: ").strip()
            if not card_num:
                print("Please insert your card.")
                attempts += 1
                continue
            pin = input("PIN: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled")
            return None

        # Try API backend first (ATMCard)
        if api is not None:
            try:
                cards = api.getATMCards(card_num)
            except Exception:
                cards = []
            if cards:
                card = cards[0]
                if not card.verify_pin(pin):
                    print("Incorrect PIN.")
                    try:
                        print(f"Failed tries: {card.getFailedTries()}")
                    except:
                        pass
                    attempts += 1
                    continue
                return ('api', card)

        # Fall back to SimpleClientRepo (single 'client' worksheet)
        if repo is not None:
            try:
                if repo.verify(card_num, pin):
                    rec = repo.get_record(card_num)
                    return ('repo', rec)
                else:
                    print("Incorrect PIN.")
                    attempts += 1
                    continue
            except Exception as e:
                print(f"[WARN] Sheet lookup failed: {e}")

        print("Card not found.")
        attempts += 1

    print("Too many failed attempts.")
    return None

def _parse_amount(s):
    s = str(s).replace('\xa0', '').replace(' ', '').replace(',', '.')
    return float(s)

def main():
    print_banner()
    if api is None and repo is None:
        print("[ERROR] Backend unavailable. Please check Google credentials or Sheets.")
        return

    auth = authenticate(api)
    if not auth:
        print("Goodbye!")
        return

    source, obj = auth

    # Show welcome message
    if source == 'repo':
        show_welcome_message(obj)
    elif source == 'api':
        print(f"\nWelcome back! Card ending in {obj.getCardNumber()[-4:]}")
        print(f"Balance: €{obj.check_balance():,.2f}\n")

    while True:
        print_menu()
        try:
            choice = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if choice in ("6", "quit", "exit"):
            print("Goodbye!")
            break

        if source == 'api':
            # Existing API + ATMCard flow
            if choice == "1":
                bal = obj.check_balance()
                print("Could not retrieve balance." if bal is None else f"Current balance: {bal:.2f}")
            elif choice == "2":
                try:
                    amt = _parse_amount(input("Amount to withdraw: ").strip())
                except Exception:
                    print("Invalid amount"); continue
                if amt <= 0: print("Amount must be positive"); continue
                print(f"Withdrawn {amt:.2f}. New balance: {obj.check_balance():.2f}" if obj.withdraw(amt)
                      else "Withdrawal failed (insufficient funds or server error).")
            elif choice == "3":
                try:
                    amt = _parse_amount(input("Amount to deposit: ").strip())
                except Exception:
                    print("Invalid amount"); continue
                if amt <= 0: print("Amount must be positive"); continue
                print(f"Deposited {amt:.2f}. New balance: {obj.check_balance():.2f}" if obj.deposit(amt)
                      else "Deposit failed (server error).")
            elif choice == "4":
                try:
                    new_pin = input("Enter new PIN: ").strip()
                    confirm = input("Confirm new PIN: ").strip()
                except Exception:
                    print("Input cancelled"); continue
                if new_pin != confirm: print("PIN mismatch. Try again."); continue
                if not new_pin.isdigit(): print("PIN must be numeric"); continue
                print("PIN changed successfully." if obj.change_pin(new_pin) else "Failed to change PIN.")
            elif choice == "5":
                transfer_money(obj, repo)
            else:
                print("Invalid option. Please choose 1-6.")
        else:
            # Single-sheet repo flow (ClientRecord)
            if choice == "1":
                print(f"Current balance: {obj.balance:.2f}")
            elif choice == "2":
                try:
                    amt = _parse_amount(input("Amount to withdraw: ").strip())
                except Exception:
                    print("Invalid amount"); continue
                if amt <= 0: print("Amount must be positive"); continue
                if amt > obj.balance:
                    print("Withdrawal failed (insufficient funds)."); continue
                new_balance = obj.balance - amt
                if repo.update_balance(obj.cardNum, new_balance):
                    obj.balance = new_balance
                    print(f"Withdrawn {amt:.2f}. New balance: {obj.balance:.2f}")
                else:
                    print("Withdrawal failed (server error).")
            elif choice == "3":
                try:
                    amt = _parse_amount(input("Amount to deposit: ").strip())
                except Exception:
                    print("Invalid amount"); continue
                if amt <= 0: print("Amount must be positive"); continue
                new_balance = obj.balance + amt
                if repo.update_balance(obj.cardNum, new_balance):
                    obj.balance = new_balance
                    print(f"Deposited {amt:.2f}. New balance: {obj.balance:.2f}")
                else:
                    print("Deposit failed (server error).")
            elif choice == "4":
                try:
                    new_pin = input("Enter new PIN: ").strip()
                    confirm = input("Confirm new PIN: ").strip()
                except Exception:
                    print("Input cancelled"); continue
                if new_pin != confirm: print("PIN mismatch. Try again."); continue
                if not new_pin.isdigit(): print("PIN must be numeric"); continue
                if repo.update_pin(obj.cardNum, new_pin):
                    obj.pin = new_pin
                    print("PIN changed successfully.")
                else:
                    print("Failed to change PIN.")
            elif choice == "5":
                transfer_money(obj, repo)
            else:
                print("Invalid option. Please choose 1-6.")
    return

if api != None or repo is not None:
    main()