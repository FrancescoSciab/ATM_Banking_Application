import sys
import gspread
from google.oauth2.service_account import Credentials
from API import API
import Account
import AccountHolder

# Create an instance of the API
x = API()

# Get all account holders
y = x.getAccountHolders(0)
print(len(y))

# Get just one account holder by searching by ID
y = x.getAccountHolders(1)
if len(y)>0:
    print(y[0].firstname)
else:
    print("No account holder found")

# Get just one account by searching by account ID
y=x.getAccountByID(12345678)
if len(y)>0:
    print(y[0].getAccountBalance())
else:
    print("No account found")

# Get just one account by searching by account holder ID
y=x.getAccountByHolderID(1)
if len(y)>0:
    print(y[0].getAccountBalance())
else:
    print("No account found")

# Get just one account by searching by account holder ID
# This account holder ID doesn't exist
y=x.getAccountByHolderID(10)
if len(y)>0:
    print(y[0].getAccountBalance())
else:
    print("No account found")

# Get all ATM cards
y = x.GetATMCards(0)
print(len(y))

# Get just one ATM card
y = x.GetATMCards(4402106811111111)
print(y[0].getAccountBalance())

# Change the pin on the previous card
print(y[0].setPin(2345))

# Increase the number of failed tries on the previous card
print(y[0].increaseFailedTries())
print(y[0].getFailedTries())

# Reset the number of failed tries
print(y[0].resetFailedTries())
print(y[0].getFailedTries())

print(y[0].increaseBalance(200))

print("End of BrianTest")