import sys
import os
import platform
from cardHolder import API, show_welcome_message, transfer_money

# Cross-platform input handling
IS_WINDOWS = platform.system() == 'Windows'
if IS_WINDOWS:
    import msvcrt
else:
    import termios
    import tty

# Import the API class and test the connection
api = None
try:
    api = API()
    if api is None:
        print("[WARN] Google APIs unavailable")
except Exception as e:
    print(f"[WARN] Failed to initialize API: {e}")

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
    
    banner_lines = [
        "╔════════════════════════════════════════════════════════════════╗",
        "║                                                                ║",
        "║                    █████╗ ████████╗███╗   ███╗                 ║",
        "║                   ██╔══██╗╚══██╔══╝████╗ ████║                 ║",
        "║                   ███████║   ██║   ██╔████╔██║                 ║",
        "║                   ██╔══██║   ██║   ██║╚██╔╝██║                 ║",
        "║                   ██║  ██║   ██║   ██║ ╚═╝ ██║                 ║",
        "║                   ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝                 ║",
        "║                                                                ║",
        "║                         Welcome to the ATM                     ║",
        "║                                                                ║",
        "╚════════════════════════════════════════════════════════════════╝"
    ]
    
    # Get terminal width, default to 80 if unavailable
    try:
        terminal_width = os.get_terminal_size().columns
    except (AttributeError, OSError):
        terminal_width = 80
    
    # Banner width is 68 characters
    banner_width = len(banner_lines[0])
    
    # Calculate left padding to center the banner (add extra spaces to move right)
    if terminal_width > banner_width:
        padding = " " * (((terminal_width - banner_width) // 2) + 10)
    else:
        padding = ""
    
    # Print centered banner
    for line in banner_lines:
        print(CYAN + padding + line + RESET)
    
    # Center the tagline as well
    tagline = "Secure • Fast • 24/7 Access | Card-Only Banking"
    if terminal_width > len(tagline):
        tagline_padding = " " * ((terminal_width - len(tagline)) // 2)
    else:
        tagline_padding = ""
    
    print(tagline_padding + tagline)
    print()

def print_menu():
    print("Please choose from one of the following options...")
    print("1. Check Balance")
    print("2. Withdraw Funds")
    print("3. Deposit Funds")
    print("4. Change PIN")
    print("5. Transfer Money")
    print("6. Exit")

def get_pin(prompt="PIN: ", max_length=6):
    """
    Securely get PIN input with masked display (cross-platform).
    Falls back to standard input if terminal masking is unavailable.
    
    Args:
        prompt: The prompt to display
        max_length: Maximum PIN length (default: 6)
    
    Returns:
        The entered PIN as a string
    """
    print(prompt, end='', flush=True)
    pin = ''
    
    # Check if we can use terminal masking
    can_mask = False
    if IS_WINDOWS:
        can_mask = True
    else:
        # Check if stdin is a TTY that supports termios
        try:
            if sys.stdin.isatty():
                fd = sys.stdin.fileno()
                termios.tcgetattr(fd)
                can_mask = True
        except (AttributeError, OSError, termios.error):
            can_mask = False
    
    if not can_mask:
        # Fallback to standard input (no masking) for WebSocket/pseudo-terminals
        try:
            pin = input().strip()[:max_length]
            return pin
        except (EOFError, KeyboardInterrupt):
            print()
            raise KeyboardInterrupt
    
    if IS_WINDOWS:
        # Windows implementation using msvcrt
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
            elif ch.isdigit() and len(pin) < max_length:
                pin += ch.decode()
                print('*', end='', flush=True)
    else:
        # Linux/Unix implementation using termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                
                # Handle Enter key (newline or carriage return)
                if ch in {'\n', '\r'}:
                    print('\r\n', end='', flush=True)
                    break
                # Handle Backspace (127) or Delete (8)
                elif ord(ch) in {127, 8}:
                    if len(pin) > 0:
                        pin = pin[:-1]
                        print('\b \b', end='', flush=True)
                # Handle Ctrl+C
                elif ord(ch) == 3:
                    raise KeyboardInterrupt
                # Handle digits
                elif ch.isdigit() and len(pin) < max_length:
                    pin += ch
                    print('*', end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
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
                print("Unable to process your card. Please try again or contact support.")
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
    """
    Parse amount string to float, handling various formats.
    
    Args:
        s: Amount string (can contain spaces, commas, etc.)
    
    Returns:
        Float value of the amount
    
    Raises:
        ValueError: If the string cannot be converted to a valid amount
    """
    try:
        s = str(s).replace('\xa0', '').replace(' ', '').replace(',', '.')
        amount = float(s)
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        return amount
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid amount format: {s}") from e

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
                print("Could not retrieve balance." if bal is None else f"Current balance: €{bal:,.2f}")
            elif choice == "2":
                try:
                    amt = _parse_amount(input("Amount to withdraw: €").strip())
                except ValueError as e:
                    print(f"Invalid amount. {e}"); continue
                if amt <= 0: 
                    print("Amount must be positive"); continue
                if obj.withdraw(amt):
                    print(f"✓ Withdrawn €{amt:,.2f}. New balance: €{obj.check_balance():,.2f}")
                else:
                    print("Withdrawal failed (insufficient funds or server error).")
            elif choice == "3":
                try:
                    amt = _parse_amount(input("Amount to deposit: €").strip())
                except ValueError as e:
                    print(f"Invalid amount. {e}"); continue
                if amt <= 0: 
                    print("Amount must be positive"); continue
                if obj.deposit(amt):
                    print(f"✓ Deposited €{amt:,.2f}. New balance: €{obj.check_balance():,.2f}")
                else:
                    print("Deposit failed (server error).")
            elif choice == "4":
                try:
                    new_pin = get_pin("Enter new PIN: ")
                    confirm = get_pin("Confirm new PIN: ")
                except (EOFError, KeyboardInterrupt):
                    print("Input cancelled"); continue
                
                if not new_pin or not confirm:
                    print("PIN cannot be empty"); continue
                if new_pin != confirm: 
                    print("PIN mismatch. Try again."); continue
                if not new_pin.isdigit(): 
                    print("PIN must be numeric"); continue
                if len(new_pin) < 4:
                    print("PIN must be at least 4 digits"); continue
                    
                if obj.change_pin(new_pin):
                    print("✓ PIN changed successfully.")
                else:
                    print("Failed to change PIN.")
            elif choice == "5":
                transfer_money(obj, repo)
            else:
                print("Invalid option. Please choose 1-6.")
        else:
            if choice == "1":
                print(f"Current balance: €{obj.balance:,.2f}")
            elif choice == "2":
                try:
                    amt = _parse_amount(input("Amount to withdraw: €").strip())
                except ValueError as e:
                    print(f"Invalid amount. {e}"); continue
                if amt <= 0: 
                    print("Amount must be positive"); continue
                if amt > obj.balance:
                    print("Withdrawal failed (insufficient funds)."); continue
                new_balance = obj.balance - amt
                if repo.update_balance(obj.cardNum, new_balance):
                    obj.balance = new_balance
                    print(f"✓ Withdrawn €{amt:,.2f}. New balance: €{obj.balance:,.2f}")
                else:
                    print("Withdrawal failed (server error).")
            elif choice == "3":
                try:
                    amt = _parse_amount(input("Amount to deposit: €").strip())
                except ValueError as e:
                    print(f"Invalid amount. {e}"); continue
                if amt <= 0: 
                    print("Amount must be positive"); continue
                new_balance = obj.balance + amt
                if repo.update_balance(obj.cardNum, new_balance):
                    obj.balance = new_balance
                    print(f"✓ Deposited €{amt:,.2f}. New balance: €{obj.balance:,.2f}")
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
                            if len(new_pin) < 4:
                                print("PIN must be at least 4 digits")
                                continue
                                
                            if repo.update_pin(obj.cardNum, new_pin):
                                obj.pin = new_pin
                                print("✓ PIN changed successfully.")
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

if __name__ == "__main__":
    if api is not None or repo is not None:
        main()
    else:
        print("[ERROR] No backend available. Cannot start ATM application.")