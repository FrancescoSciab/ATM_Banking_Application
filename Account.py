class Account:

    def __init__(self, accountID, accountHolderID, accountBalance):
        self.accountID=accountID
        self.accountHolderID=accountHolderID
        self.accountBalance=accountBalance

    def getAccountID(self):
        return self.accountID
    
    def getAccountHolderID(self):
        return self.accountHolderID
    
    def getAccountBalance(self):
        return self.accountBalance

    def increaseBalance(self, amountToAdd):
        self.accountBalance+=amountToAdd
        'Call api to update server'