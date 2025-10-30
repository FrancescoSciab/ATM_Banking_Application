from Account import Account

class ATMCard(Account):
    def __init__(self, accountID, accountHolderID, accountBalance, cardNumber, pin, failedTries):
        super().__init__(accountID, accountHolderID, accountBalance)
        self.cardNumber = cardNumber
        self.pin = pin
        self.failedTries = failedTries

    def getCardNumber(self):
        return self.cardNumber
    
    def getPin(self):
        return self.pin
    
    def setPin(self, newPin):
        self.pin = newPin
        'Call api to update server'
        from API import API
        a = API()
        return a.setPin(self.cardNumber,newPin)
    
    def getFailedTries(self):
        return self.failedTries
    
    def increaseFailedTries(self):        
        'Call api to update server'
        from API import API
        a = API()
        if a.increaseFailedTries(self.cardNumber,int(self.failedTries)+1):
            ' server updated, update the local instance'
            self.failedTries = int(self.failedTries)+ 1
            return True
        else:
            return False

    def resetFailedTries(self):
        'Call api to update server'
        from API import API
        a = API()
        if a.resetFailedTries(self.cardNumber):
            ' server updated, update the local instance'
            self.failedTries = 0
            return True
        else:
            return False