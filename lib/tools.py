import requests
import json
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

    def updatePricesFromNomics(self):
        nomicsKey = globals.database.getOptionsValue('nomics')
        if nomicsKey == None:
            return False

        res = requests.get("https://api.nomics.com/v1/currencies/ticker?ids=BTC,ETH,ADA,BNB&interval=1d,30d&convert=USD&per-page=100&page=1&key=" + nomicsKey)
        if res.status_code == 200:
            data  = json.loads(res.text)
            for coin in data:
                globals.database.setCoinInformation(coin['currency'], coin['price'], coin['price_date'])

        return True
        