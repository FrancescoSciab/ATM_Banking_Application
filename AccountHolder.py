class AccountHolder:
    def __init__(self, id, firstname, lastname, phone):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone

    def getID(self):
        return self.id
    
    def getFirstname(self):
        return self.firstname
    
    def getLastname(self):
        return self.lastname
    
    def getPhone(self):
        return self.phone
    
    def updateAccount(self, firstname, lastname, phone):
        'Call api to update server'
        from API import API
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