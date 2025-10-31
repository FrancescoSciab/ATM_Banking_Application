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
        try:
            account_cell = a.SHEET.worksheet("account").findall(self.accountID)
            ' There should be only one, but this search will ensure it is the card number column that was found'
            for idColCheck in account_cell:
                if int(idColCheck.col)==1:
                    from Account import formatFloatFromServer
                    curValue = formatFloatFromServer(a.SHEET.worksheet("account").row_values(idColCheck.row)[2])
                    print(curValue)                    
                    curValue = float(curValue)+amountToAdd
                    print(curValue)
                    a.SHEET.worksheet("account").update_cell(idColCheck.row,3,curValue)
                    return True
        except:
            return False
        return False