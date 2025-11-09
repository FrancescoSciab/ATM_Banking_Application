import sys
import os
import json
import msvcrt
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

def get_pin(prompt="PIN: "):
    print(prompt, end='', flush=True)
    pin = ''
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}: 
            print()
            break
        elif ch == b'\x08': 
            if len(pin) > 0:
                pin = pin[:-1]
                print('\b \b', end='', flush=True)
        elif ch in {b'\x03', b'\x1b'}: 
            raise KeyboardInterrupt
        elif ch.isdigit():
            pin += ch.decode()
            print('*', end='', flush=True)
    return pin

def authenticate(api):
    """Prompt for card and PIN first, return a tuple (source, obj) or None.
    source: 'api' for ATMCard via API, 'repo' for ClientRecord via SimpleClientRepo
    """
    while True:
        try:
            card_num = input("Insert Your Card: ").strip()
            if not card_num:
                print("Please insert your card.")
                continue
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled")
            return None

        if api is not None:
            try:
                cards = api.getATMCards(card_num)
            except Exception as e:
                print(f"Error checking card with API: {e}")
                cards = []

            if cards: 
                card = cards[0]
                pin_attempts = 0
                while pin_attempts < 3:
                    pin = get_pin("PIN: ")
                    if not card.verify_pin(pin):
                        pin_attempts += 1
                        remaining_attempts = 3 - pin_attempts
                        print("Incorrect PIN.")
                        if remaining_attempts > 0:
                            print(f"You have {remaining_attempts} attempt(s) remaining for your PIN to enter")
                            try:
                                print(f"Failed tries: {card.getFailedTries()}")
                            except:
                                pass
                        if pin_attempts >= 3:
                            print("Too many failed PIN attempts. Your card has been locked for security.")
                            print("Please contact your bank administration to unlock your card.")
                            return None
                        continue
                    return ('api', card)

        if repo is not None:
            try:
                rec = repo.get_record(card_num)
                if not rec:
                    print("Card not found. Please try again.")
                    continue

                pin_attempts = 0
                while pin_attempts < 3:
                    pin = get_pin("PIN: ")
                    if str(rec.pin) == str(pin):
                        return ('repo', rec)
                    else:
                        pin_attempts += 1
                        remaining_attempts = 3 - pin_attempts
                        print("Incorrect PIN.")
                        if remaining_attempts > 0:
                            print(f"You have {remaining_attempts} attempt(s) remaining for your PIN to enter")
                        if pin_attempts >= 3:
                            print("Too many failed PIN attempts. Your card has been locked for security.")
                            print("Please contact your bank administration to unlock your card.")
                            return None
                        continue
            except Exception as e:
                print(f"[WARN] Sheet lookup failed: {e}")

        print("Card not found.")
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
                pin_attempts = 0
                pin_changed = False
                while pin_attempts < 3:
                    try:
                        current = get_pin("Enter current PIN: ")
                        if str(obj.pin) != str(current):
                            pin_attempts += 1
                            remaining_attempts = 3 - pin_attempts
                            print("Incorrect current PIN.")
                            if remaining_attempts > 0:
                                print(f"You have {remaining_attempts} attempt(s) remaining.")
                            if pin_attempts >= 3:
                                print("Too many incorrect attempts. Returning to main menu.")
                            continue
                        
                        try:
                            new_pin = get_pin("Enter new PIN: ")
                            confirm = get_pin("Confirm new PIN: ")
                            
                            if new_pin != confirm:
                                print("PIN mismatch. Try again.")
                                continue
                            if not new_pin.isdigit():
                                print("PIN must be numeric")
                                continue
                                
                            if repo.update_pin(obj.cardNum, new_pin):
                                obj.pin = new_pin
                                print("PIN changed successfully.")
                                pin_changed = True
                                break
                            else:
                                print("Failed to change PIN.")
                                break
                        except Exception:
                            print("Input cancelled")
                            break
                    except Exception:
                        print("Input cancelled")
                        break
                if not pin_changed:
                    continue
            elif choice == "5":
                transfer_money(obj, repo)
            else:
                print("Invalid option. Please choose 1-6.")
    return

if api != None or repo is not None:
    main()