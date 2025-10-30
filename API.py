import sys
import gspread
from google.oauth2.service_account import Credentials

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
        from AccountHolder import AccountHolder
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
        from Account import Account
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
        from Account import Account
        return_list_of_accounts = []
        list_of_accounts = self.SHEET.worksheet("account").get_all_values()[1:]
        for account in list_of_accounts:
            if int(id) == 0:
                return_list_of_accounts.append(Account(account[0],account[1],account[2]))
            elif int(id) == int(account[1]):
                return_list_of_accounts.append(Account(account[0],account[1],account[2]))
        return return_list_of_accounts
    
    def GetATMCards(self,id):
        from ATMCard import ATMCard
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
    
    def setPin(self,cardNumber,newPin):
        try:
            card_cell = self.SHEET.worksheet("atmCards").findall(cardNumber)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in card_cell:
                if int(idColCheck.col)==2:
                    self.SHEET.worksheet("atmCards").update_cell(idColCheck.row,3,newPin)
                    return True
        except:
            return False

    def increaseFailedTries(self,cardNumber,failedTries):
        try:
            card_cell = self.SHEET.worksheet("atmCards").findall(cardNumber)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in card_cell:
                if int(idColCheck.col)==2:
                    self.SHEET.worksheet("atmCards").update_cell(idColCheck.row,4,failedTries)
                    return True
        except:
            return False
        
    def resetFailedTries(self,cardNumber):
        try:
            card_cell = self.SHEET.worksheet("atmCards").findall(cardNumber)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in card_cell:
                if int(idColCheck.col)==2:
                    self.SHEET.worksheet("atmCards").update_cell(idColCheck.row,4,0)
                    return True
        except:
            return False
        
    def increaseBalance(self,accountID,amountToAdd):
        try:
            card_cell = self.SHEET.worksheet("account").findall(accountID)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in card_cell:
                if int(idColCheck.col)==1:
                    from Account import formatFloatFromServer
                    curValue = formatFloatFromServer(self.SHEET.worksheet("account").row_values(idColCheck.row)[2])
                    print(curValue)                    
                    curValue = float(curValue)+amountToAdd
                    print(curValue)
                    self.SHEET.worksheet("account").update_cell(idColCheck.row,3,curValue)
                    return True
        except:
            return False