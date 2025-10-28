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
    
    def getFailedTries(self):
        return self.failedTries
    
    def increaseFailedTries(self):
        self.failedTries+=1
        'Call api to update server'

    def resetFailedTries(self):
        self.failedTries=0
        'Call api to update server'
