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
        'Call api to update server'
        from API import API
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
    
    def increaseFailedTries(self):        
        'Call api to update server'
        from API import API
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
        
    def resetFailedTries(self):
        'Call api to update server'
        from API import API
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