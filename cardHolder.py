"""Data model representing a bank card holder used by the ATM application."""

class cardHolder:
    """Encapsulates card credentials, identity details, and account balance."""

    def __init__(self, cardNum, pin, firstname, lastname, balance):
        """Initialize a new card holder.
        
        Args:
            cardNum (str|int): The card number uniquely identifying the card.
            pin (str|int): Personal Identification Number (sensitive).
            firstname (str): Holder's first name.
            lastname (str): Holder's last name.
            balance (float): Current available balance.
        """
        self.cardNum = cardNum
        self.pin = pin
        self.firstname = firstname
        self.lastname = lastname
        self.balance = balance

    def __str__(self):
        """Internal/debug representation. Avoid exposing PIN in production logs."""
        return f"cardHolder({self.cardNum}, {self.pin}, {self.firstname}, {self.lastname}, {self.balance})"

    # Getter methods
    def get_cardNum(self):
        """Return the card number."""
        return self.cardNum

    def get_pin(self):
        """Return the PIN (sensitive). Avoid logging or displaying it."""
        return self.pin

    def get_firstName(self):
        """Return the holder's first name."""
        return self.firstname

    def get_lastName(self):
        """Return the holder's last name."""
        return self.lastname

    def get_balance(self):
        """Return the current account balance."""
        return self.balance

    # Setter methods
    def set_cardNum(self, newVal):
        """Set a new card number."""
        self.cardNum = newVal

    def set_pin(self, newVal):
        """Set a new PIN. Consider validation and secure storage."""
        self.pin = newVal

    def set_firstName(self, newVal):
        """Set the holder's first name."""
        self.firstname = newVal

    def set_lastName(self, newVal):
        """Set the holder's last name."""
        self.lastname = newVal

    def set_balance(self, newVal):
        """Set the account balance. Prefer domain operations (deposit/withdraw)."""
        self.balance = newVal

    def print_out(self):
        """Print all fields for debugging.
        
        Warning:
            This prints sensitive data (PIN). Do not use in production logs.
        """
        print("Card #: ", self.cardNum)
        print("Pin: ", self.pin)
        print("First Name: ", self.firstname)
        print("Last Name: ", self.lastname)
        print("Balance: ", self.balance)
