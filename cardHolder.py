import sys
import gspread
from google.oauth2.service_account import Credentials

# General functions will be used repeatedly

# Function to ensure that the number in the database is converted to a float type for easier processing
def formatFloatFromServer(numberToConvert):
        numberToConvert=str(numberToConvert).replace(',','.')
        return numberToConvert

class API:
    # Initialise the API class
    # The connection can be verified by checking that the instance is not None    
    def __init__(self):
        self.SCOPE=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        try:
            self.CREDS = Credentials.from_service_account_file("creds.json")
            self.SCOPED_CREDS = self.CREDS.with_scopes(self.SCOPE)
            self.GSPREAD_CLIENT = gspread.authorize(self.SCOPED_CREDS)
            self.SHEET = self.GSPREAD_CLIENT.open("client_database")
        except Exception as e:
            self=None


    # Get a list of all Account Holders, or just 1
    # @id - set as 0 to retrieve all account holders, or any other number to retrieve just 1
    # Returns an array of type AccountHolder
    # The length of the return will be 0 if no account holder is found
    def getAccountHolders(self, id):
        return_list_of_accountHolders = []
        list_of_accountHolders = self.SHEET.worksheet("accountHolder").get_all_values()[1:]
        for holder in list_of_accountHolders:
            if (int(id) == 0):
                return_list_of_accountHolders.append(AccountHolder(holder[0],holder[1],holder[2],holder[3]))
            elif int(id) == int(holder[0]):
                return_list_of_accountHolders.append(AccountHolder(holder[0],holder[1],holder[2],holder[3]))
        return return_list_of_accountHolders
    
    # Get a list of all accounts, or just 1 by searching by "Account ID"
    # @id - set as 0 to retrieve all accounts, or any other number to retrieve 1
    # Returns an array of type "Account"
    # The length of the returned array will be 0 if no Accounts are found
    def getAccountByID(self,id):
        return_list_of_accounts = []
        list_of_accounts = self.SHEET.worksheet("account").get_all_values()[1:]
        for account in list_of_accounts:
            if int(id) == 0:
                return_list_of_accounts.append(Account(account[0],account[1],account[2]))
            elif int(id) == int(account[0]):
                return_list_of_accounts.append(Account(account[0],account[1],account[2]))
        return return_list_of_accounts
    
    # Get a list of all accounts, or just 1 by searching by "Account Holder ID"
    # @id - set as 0 to retrieve all accounts, or any other number to retrieve 1
    # Returns an array of type "Account"
    # The length of the returned array will be 0 if no Accounts are found
    def getAccountByHolderID(self,id):
        return_list_of_accounts = []
        list_of_accounts = self.SHEET.worksheet("account").get_all_values()[1:]
        for account in list_of_accounts:
            if int(id) == 0:
                return_list_of_accounts.append(Account(account[0],account[1],account[2]))
            elif int(id) == int(account[1]):
                return_list_of_accounts.append(Account(account[0],account[1],account[2]))
        return return_list_of_accounts
    
    # Get a list of all atm cards, or just 1 by searching by "ATM Card ID"
    # @id - set as 0 to retrieve all cards, or any other number to retrieve 1
    # Returns an array of type "ATMCard"
    # The length of the returned array will be 0 if no ATMCards are found
    def getATMCards(self,id):
        return_list_of_atm_cards = []
        list_of_accounts = []
        if int(id)==0:
            # You will need all accounts to pair
            # Search once here to avoid repeated searches later
            list_of_accounts=self.getAccountByID(0)
        list_of_cards = self.SHEET.worksheet("atmCards").get_all_values()[1:]
        for atm in list_of_cards:
            if int(id)==0:
                # Find the row that corresponds to the accountID
                for account in list_of_accounts:
                    if int(account.getAccountID())==int(atm[0]):
                        return_list_of_atm_cards.append(ATMCard(atm[0],account.getAccountID(),account.getAccountBalance(),atm[1],atm[2],atm[3]))
            elif int(id)==int(atm[1]):
                for account in self.getAccountByID(atm[0]):
                    if int(account.getAccountID())==int(atm[0]):
                        return_list_of_atm_cards.append(ATMCard(atm[0],account.getAccountID(),account.getAccountBalance(),atm[1],atm[2],atm[3]))
        return return_list_of_atm_cards

class AccountHolder:
    # Initialise the AccountHolder class
    def __init__(self, id, firstname, lastname, phone):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone

    # Getters and Setters
    def getID(self):
        return self.id
    
    def getFirstname(self):
        return self.firstname
    
    def getLastname(self):
        return self.lastname
    
    def getPhone(self):
        return self.phone
    
    # Update the account details on the server
    # @firstname - a string
    # @lastname - a string
    # @phone - a string
    # Returns true if database successfully updated, false if it did not
    def updateAccount(self, firstname, lastname, phone):
        'Call api to update server'
        a = API()
        try:
            accountHolder_cell = a.SHEET.worksheet("accountHolder").findall(self.id)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in accountHolder_cell:
                if int(idColCheck.col)==1:
                    a.SHEET.worksheet("accountHolder").update_cell(idColCheck.row,2,firstname)
                    a.SHEET.worksheet("accountHolder").update_cell(idColCheck.row,3,lastname)
                    a.SHEET.worksheet("accountHolder").update_cell(idColCheck.row,4,phone)
                    self.firstname = firstname
                    self.lastname = lastname
                    self.phone = phone
                    return True
        except:
            return False
        return False

class Account:
    # Initialise the Account class
    def __init__(self, accountID, accountHolderID, accountBalance):
        self.accountID=accountID
        self.accountHolderID=accountHolderID
        self.accountBalance=formatFloatFromServer(accountBalance)

    # Getters and Setters
    def getAccountID(self):
        return self.accountID
    
    def getAccountHolderID(self):
        return self.accountHolderID
    
    def getAccountBalance(self):
        return self.accountBalance

    # Update the balance on the account
    # @amountToAdd - a float, can be negative to reduce the balance, or positive to increase it
    # Returns true if database successfully updated, false if it did not
    def increaseBalance(self, amountToAdd):
        'Call api to update server'
        a = API()
        try:
            account_cell = a.SHEET.worksheet("account").findall(self.accountID)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in account_cell:
                if int(idColCheck.col)==1:
                    curValue = formatFloatFromServer(a.SHEET.worksheet("account").row_values(idColCheck.row)[2])
                    print(curValue)                    
                    curValue = float(curValue)+amountToAdd
                    print(curValue)
                    a.SHEET.worksheet("account").update_cell(idColCheck.row,3,curValue)
                    return True
        except:
            return False
        return False

class ATMCard(Account):
    # Initialise the ATMCard class
    def __init__(self, accountID, accountHolderID, accountBalance, cardNumber, pin, failedTries):
        super().__init__(accountID, accountHolderID, accountBalance)
        self.cardNumber = cardNumber
        self.pin = pin
        self.failedTries = failedTries

    # Getters and Setters
    def getCardNumber(self):
        return self.cardNumber
    
    def getPin(self):
        return self.pin
    
    # Update the pin in the database relating to an instance of an ATMCard
    # @newPin - an int
    # Returns true if database successfully updated, false if it did not
    def setPin(self, newPin):
        'Call api to update server'
        a = API()
        try:
            card_cell = a.SHEET.worksheet("atmCards").findall(self.cardNumber)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in card_cell:
                if int(idColCheck.col)==2:
                    a.SHEET.worksheet("atmCards").update_cell(idColCheck.row,3,newPin)
                    self.pin = newPin
                    return True
        except:
            return False
        return False
    
    def getFailedTries(self):
        return self.failedTries
    
    # Update the number of failed tries in the database by 1
    # Returns true if database successfully updated, false if it did not
    def increaseFailedTries(self):        
        'Call api to update server'
        a = API()
        try:
            card_cell = a.SHEET.worksheet("atmCards").findall(self.cardNumber)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in card_cell:
                if int(idColCheck.col)==2:
                    a.SHEET.worksheet("atmCards").update_cell(idColCheck.row,4,int(self.failedTries)+1)
                    self.failedTries = int(self.failedTries)+ 1
                    return True
        except:
            return False
        return False
    
    # Update the number of failedTries in the database, resets the number to 0
    # Returns true if database successfully updated, false if it did not
    def resetFailedTries(self):
        'Call api to update server'
        a = API()
        try:
            card_cell = a.SHEET.worksheet("atmCards").findall(self.cardNumber)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in card_cell:
                if int(idColCheck.col)==2:
                    a.SHEET.worksheet("atmCards").update_cell(idColCheck.row,4,0)
                    self.failedTries = 0
                    return True
        except:
            return False
        return False






# # This class needs to be removed
# class cardHolder:
#     def __init__(self, cardNum, pin, firstname, lastname, balance):
#         self.cardNum = cardNum
#         self.pin = pin
#         self.firstname = firstname
#         self.lastname = lastname
#         self.balance = balance

#     def __str__(self):
#         return f"cardHolder({self.cardNum}, {self.pin}, {self.firstname}, {self.lastname}, {self.balance})"

#     # Getter methods
#     def get_cardNum(self):
#         return self.cardNum

#     def get_pin(self):
#         return self.pin

#     def get_firstName(self):
#         return self.firstname

#     def get_lastName(self):
#         return self.lastname

#     def get_balance(self):
#         return self.balance

#     # Setter mathods
#     def set_cardNum(self, newVal):
#         self.cardNum = newVal

#     def set_pin(self, newVal):
#         self.pin = newVal

#     def set_firstName(self, newVal):
#         self.firstname = newVal

#     def set_lastName(self, newVal):
#         self.lastname = newVal

#     def set_balance(self, newVal):
#         self.balance = newVal

#     def print_out(self):
#         print("Card #: ", self.cardNum)
#         print("Pin: ", self.pin)
#         print("First Name: ", self.firstname)
#         print("Last Name: ", self.lastname)
#         print("Balance: ", self.balance)
