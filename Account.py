def formatFloatFromServer(numberToConvert):
        numberToConvert=str(numberToConvert).replace(',','.')
        return numberToConvert

class Account:

    def __init__(self, accountID, accountHolderID, accountBalance):
        self.accountID=accountID
        self.accountHolderID=accountHolderID
        self.accountBalance=formatFloatFromServer(accountBalance)

    def getAccountID(self):
        return self.accountID
    
    def getAccountHolderID(self):
        return self.accountHolderID
    
    def getAccountBalance(self):
        return self.accountBalance

    def increaseBalance(self, amountToAdd):
        'Call api to update server'
        from API import API
        a = API()
        if a.increaseBalance(self.accountID,amountToAdd):
            ' server updated, update the local instance'
            self.accountBalance = float(self.accountBalance) + amountToAdd
            return True
        else:
            return False