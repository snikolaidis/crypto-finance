from datetime import datetime
from dateutil.relativedelta import relativedelta
from lib import globals

class Tools:

    def getThePrice(self, arrayOfPrices, method = "avg"):
        method = method.lower()
        if method == "avg":
            finalPrice = 0
            for coinKey in arrayOfPrices.keys():
                finalPrice += arrayOfPrices[coinKey]
            finalPrice = finalPrice / len(arrayOfPrices.keys())
        elif method == "max":
            finalPrice = 0
            for coinKey in arrayOfPrices.keys():
                finalPrice = max(finalPrice, arrayOfPrices[coinKey])
        elif method == "min":
            finalPrice = float('inf')
            for coinKey in arrayOfPrices.keys():
                finalPrice = min(finalPrice, arrayOfPrices[coinKey])

        return round(finalPrice, 6)

    def getNomicsKey(self):
        return globals.database.getOptionsValue('nomics')

    def getExchangeRatesAPIKey(self):
        return globals.database.getOptionsValue('exchangeratesapi')

    def getTheMonthFromShort(self, month):
        month = month.lower()
        months = {
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12,
        }
        try:
            return months[month]
        except:
            return -1
    
    def pickAnInteger(self, message = "Give me a number", min = 1, max = 100, default = 1):
        theNumber = default
        while True:
            theNumber = input(message + " (" + f"{min:,}" + " - " + f"{max:,}" + "): ")
            try:
                theNumber = int(theNumber)
                if theNumber < min or theNumber > max:
                    raise ValueError('')
            except ValueError as e:
                print("Please, enter a valid integer value.")
            else:
                break
        
        return theNumber
    
    def pickAString(self, message = "Give me a string", min = 1, max = 100, default = 1):
        theString = default
        while True:
            theString = input(message + " (length between " + f"{min:,}" + " - " + f"{max:,}" + "): ")
            try:
                if len(theString) < min or len(theString) > max:
                    raise ValueError('')
            except ValueError as e:
                print("Please, enter a valid string value.")
            else:
                break
        
        return theString
    
    def pickAFloat(self, message = "Give me a number", min = 1, max = 100, default = 1):
        theNumber = default
        while True:
            theNumber = input(message + " (" + f"{min:,}" + " - " + f"{max:,}" + "): ")
            try:
                theNumber = float(theNumber)
                if theNumber < min or theNumber > max:
                    raise ValueError('')
            except ValueError as e:
                print("Please, enter a valid real value.")
            else:
                break
        
        return theNumber

    def formatThePrice(self, price):
        if price > 1:
            return "{:,.2f}".format(price)
        else:
            return "{:,.f}".format(price)

    def getDateFromString(self, strDate):
        return datetime.fromisoformat(self.clearDateIsoFormat(strDate))

    def clearDateIsoFormat(self, strDate):
        return strDate.replace("Z", "")

    def firstDayOfTheMonth(self, date):
        return datetime(date.year, date.month, 1)

    def lastDayOfTheMonth(self, date):
        newDay = datetime(date.year, date.month, 1) + relativedelta(months=+1, days=-1)
        return newDay

    def getNextMonth(self, date):
        newDay = datetime(date.year, date.month, date.day) + relativedelta(months=+1)
        return newDay

    def getPreviousMonth(self, date):
        newDay = datetime(date.year, date.month, date.day) + relativedelta(months=-1)
        return newDay
