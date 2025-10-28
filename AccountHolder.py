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
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        'Call api to update server'