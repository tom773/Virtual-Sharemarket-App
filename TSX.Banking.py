import time
from googlefinance import getQuotes
import json



class Account:

    balance = 50000

    def __init__(self, filename):
        self.filename = filename
        try:
            openFile = open(self.filename, "r")
            self.balance = float(openFile.read())
        except FileNotFoundError:
            pass

    def save(self):
        openFile = open(self.filename, "w")
        openFile.write(str(self.balance))



class TSX:
    def __init__(self, account):
        self.account = account

    def start(self):
            chosenService = int(input("Select service: 1. Banking 2. ShareMarket: "))
            if chosenService is 1:
                banking = Banking(self.account)
                banking.getAge()
            elif chosenService is 2:
                shareMarket = ShareMarket(self.account)
                shareMarket.startMenu()


class Banking:
    def __init__(self, account):

        self.account = account

    def getAge(self):

        Age = int(input("Hello, Please enter your current legal age \n"))

        if Age < 18:
            print("You are too young to use our rektBanking service")
            self.quit()
        else:
            print("Welcome to rektBanking")
            self.menu()

    def menu(self):
        print("Please select an option from the menu: \n" "1. Balance 2. Make a Payment 3. Currency Converter 4. Deposit 5. Withdraw 6. Quit")
        number = int(input())

        if number is 1:
            self.printBalance()

        if number is 2:
            self.makePayment()

        if number is 3:
            self.currencyConverter()

        if number is 4:
            self.deposit()

        if number is 5:
            self.withdraw()

        if number is 6:
            print("Thanks for using our Banking Service!")
            time.sleep(2)
            self.quit()

        else:
            print("Not a valid selection, try again")
            time.sleep(1)

            self.menu()

    def printBalance(self):
        print("Your Balance is: $", self.account.balance)

        time.sleep(2)

        self.menu()



    def makePayment(self):

        print("To whom would you like to receive the payment?")

        person = input()

        print("You selected " + person + ", Please specify how much to send: ")

        amount = int(input())

        while amount > self.account.balance:

            print("Not enough funds, Try Again\n")

            amount = int(input())

        print("You have sent", amount, " dollars to " + person + "\n")

        self.account.balance = self.account.balance - amount

        self.printBalance()

    def deposit(self):

        print("How much would you like to deposit without Commas or Dollar Sign")

        amount = int(input())

        self.account.balance = self.account.balance + amount

        self.printBalance()

    def withdraw(self):

        print("How much would you like to withdraw without Commas or a Dollar sign")

        amount = int(input())

        while amount > self.account.balance:
            print("Not enough funds try again\n")
            time.sleep(2)

            amount = int(input())



        self.account.balance = self.account.balance - amount

        self.printBalance()

    def gbp(self, value):
        rate = 0.69

        finalGbp = value * rate
        print("£", finalGbp)

    def Euro(self,value):
        rate = 0.89

        finalEuro = value * rate
        print("€", finalEuro)

    def Aud(self, value):
        rate = 1.41

        finalAud = value * rate
        print("$", finalAud)



    def currencyConverter(self):
        currency = int(input("Please Select a currency 1. GBP 2. Euro or 3. Aud \n"))

        value = int(input("Enter amount in USD to convert from\n "))

        if currency is 1:
            self.gbp(value)
            time.sleep(2)
            self.menu()
        if currency is 2:
            self.Euro(value)
            time.sleep(2)
            self.menu()
        if currency is 3:
            self.Aud(value)
            time.sleep(2)
            self.menu()

    def quit(self):
        self.account.save()
        quit()

class ShareMarket:

    stocksBought = list()

    def __init__(self, account):
        self.account = account

    def startMenu(self):

        print("Welcome to the TSX Investor page\n\n")

        menuItem = int(input("Please select an option from the menu: 1. Buy 2. Sell 3. Check a Stock 4. My Portfolio 5. Quit\n"))

        if menuItem is 1:
            self.buyStock()

        elif menuItem is 2:
            self.sellStock()

        elif menuItem is 3:
            self.checkStock()

        elif menuItem is 4:
            self.myPortfolioMenu()

        elif menuItem is 5:
            self.quit()

        else:
            print("Invalid Selection, Try Again")
            time.sleep(2)
            self.startMenu()



    def getPrice(self, chosenStock):
        """
        Retrieves the last trade price of a stock.

        :param chosenStock: stock symbol
        :return: float value of last trade price
        """
        allInfo = getQuotes(chosenStock)

        theStock = allInfo[0]

        price = theStock["LastTradePrice"]

        return float(price)


    def buyStock(self):

        global stocksBought

        chosenStock = str(input("Please input the ID the stock you wish to purchase: "))

        print("The value of the stock is: \n", self.getPrice(chosenStock))

        amount = float(input("Please enter the amount of shares you wish to purchase: "))

        finalPrice = self.getPrice(chosenStock) * amount

        while finalPrice > self.account.balance:

            print("Not enough funds try again:\n")

            amount = float(input("Please enter the amount of shares you wish to purchase: "))

        print("Your final price is: ", finalPrice, "\n")

        self.stocksBought.append(chosenStock)

        print(self.stocksBought)

        time.sleep(2)

        self.account.balance = self.account.balance - finalPrice

        print("Your balance is now: ", self.account.balance)

        self.save(stocksBought)

        time.sleep(2)

        self.startMenu()

    def sellStock(self):
        pass

    def checkStock(self):
        chosenStock = str(input("Enter Stock Name: "))
        print(self.getPrice(chosenStock))
        time.sleep(2)
        self.startMenu()

    def myPortfolioMenu(self):

        try:
            pass
        except:

            pass

            print("No stocks bought")

            time.sleep(2)

            self.startMenu()

        chosenOption = int(input("Welcome to your Portfolio, choose an option: 1. Check Your Total Value 2. View Stocks Bought \n"))

        if chosenOption is 1:
            self.checkTotalValue()
        if chosenOption is 2:

            try:
                print("The stocks you have bought are: ", self.stocksBought)

                time.sleep(2)

                self.startMenu()
            except NameError:
                print(' '.join(map(str, self.stocksBought)))

                time.sleep(2)

                self.startMenu()

            finally:
                print("You Have Bought No Stocks")

                time.sleep(2)

                self.startMenu()

        else:
            print("Not a valid option, please select one: ")
            chosenOption = int(input())


    def save(self, stocksBought):

        with open('stocksBought.txt', 'w', encoding='utf-8') as outfile:
            json.dumps(stocksBought, outfile)



    def checkTotalValue(self):

        pass


    def quit(self):

        self.account.save()

        quit()

# start banking app

accountFileName = 'account.txt'
account = Account(accountFileName)

tsx = TSX(account)
tsx.start()
