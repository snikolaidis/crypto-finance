import random, math, json, time
from requests import NullHandler
from lib import globals
from simple_chalk import chalk

class Finance:

    def calculateMonthlyRepeatedInvestment(self, coin, monthly_invest = 500, yearly_perc_increase = 20, method = "avg", initial_amount = 0):
        print("")
        print("Coin: " + coin["code"].upper())
        print("Coin price at 12/2021: " + "$ {:,.2f}".format(getThePrice(coin["end_of_2021"], method)))

        totalProfit = initial_amount
        previous_value = getThePrice(coin["end_of_2021"], method)
        totalInvest = initial_amount
        monthyInvest = monthly_invest

        for year in range(2022, 2029):
            print("")
            print("Year: " + str(year))
            print("Monthly invest: " + "$ {:,.2f}".format(monthyInvest))

            for month in range(0, 12):
                key = str(year) + "-" + '{:02d}'.format(month + 1)
                new_value = getThePrice(coin["prices"][key], method)
                inc_perc = (new_value - previous_value) / previous_value
                totalProfit += monthyInvest + (totalProfit * inc_perc)
                totalInvest += monthyInvest

                print("Month: " + '{:02d}'.format(month + 1)
                    + "     " + "Price: $" + ("{:,.2f}".format(new_value)).rjust(11)
                    + "     " + "Diff: $" + ("{:,.2f}".format(new_value - previous_value)).rjust(11)
                    + "     " + "Perc:" + ("{:,.5f}%".format(inc_perc)).rjust(11)
                    + "     " + "Total: $" + ("{:,.2f}".format(totalProfit)).rjust(11)
                )
                previous_value = new_value
            
            monthyInvest = monthyInvest * (1 + (yearly_perc_increase / 100))
        
        print("")
        print("====================================================================================")

        return totalInvest, totalProfit


    def getCoinsSupported(self):
        coins = globals.database.getSupportedCoins()
        for coin in coins:
            self.printCoinInformation(coin[2], coin[1], coin[3], coin[4], coin[5])

    def updateCoinsSupported(self):
        if globals.tools.updatePricesFromNomics() == False:
            print("There was an error while updating the system, please check and make sure you have the key " + chalk.green("nomics") + " configured in the settings.")
        else:
            print("All coins are updated.")

        if globals.tools.updateFiatFromExchangeRatesAPI() == False:
            print("There was an error while updating the system, please check and make sure you have the key " + chalk.green("exchangeratesapi") + " configured in the settings.")
        else:
            print("All FIAT are updated.")

    def addCoinsSupported(self):
        newCoin = ""
        while True:
            newCoin = globals.tools.pickAString("Give me the coin code", 0, 5).upper()
            if newCoin == '':
                break

            try:
                # Let's check if it exists in the database
                coinCnt, = globals.db_schema.execSelectOne("SELECT COUNT(*) FROM list_of_coins WHERE coin_code = ?", [newCoin])
                if coinCnt > 0:
                    raise ValueError(newCoin + " already exists in the database.")

                nomicsKey = globals.tools.getNomicsKey()
                if nomicsKey == None:
                    return False

                res = globals.network.callGet("https://api.nomics.com/v1/currencies/ticker?ids=" + newCoin + "&interval=1d,30d&convert=USD&per-page=100&page=1&key=" + nomicsKey)
                if res:
                    data  = json.loads(res.text)
                    if len(data) == 0:
                        raise ValueError(newCoin + " is an unknown coin. Please try again")
                    coin = data[0]
                    rank = 999
                    try:
                        rank = coin['rank']
                    except:
                        print(newCoin + " has not ranking, I will apply ranking no 999.")
                        print()

                    globals.database.setCoinInformation(coin['currency'], coin['price'], coin['price_date'], rank, coin['name'])
                    print()
                    self.printCoinInformation(coin['name'], coin['currency'], float(coin['price']), coin['price_date'], rank)
                    print()
                    print(newCoin + " was added in the database.")

                break

            except ValueError as e:
                print(e)

    def removeCoinsSupported(self):
        newCoin = ""
        while True:
            newCoin = globals.tools.pickAString("Give me the coin code", 0, 5).upper()
            if newCoin == '':
                break

            try:
                # Let's check if it exists in the database
                coinCnt, = globals.db_schema.execSelectOne("SELECT COUNT(*) FROM list_of_coins WHERE coin_code = ?", [newCoin])
                if coinCnt == 0:
                    raise ValueError(newCoin + " does not exists in the database.")

                globals.database.unsetCoinInformation(newCoin)
                print(newCoin + " was removed from the database.")
                break

            except ValueError as e:
                print(e)

    def printCoinInformation(self, coin_code, name, price, price_date, rank):
        print(name + ' (' + chalk.green(coin_code) + ')')
        if price > 1:
            print("  Price: " + chalk.green('${:,.2f}'.format(price)))
        else:
            print("  Price: " + chalk.green('${:,}'.format(price)))
        print("  Date: " + chalk.green(price_date))
        print("  Rank: " + chalk.green(rank))

    def doGenerateCustomRandomPrices(self, startPrice, endPrice, totalMonths, fluctuation = 10):
        step = (endPrice - startPrice) / totalMonths
        calcPrice = startPrice

        # Basic return structure
        data = {
            "step": step,
            "startPrice": startPrice,
            "endPrice": endPrice,
            "months": totalMonths,
            "fluctuation": fluctuation,
            "prices": [],
        }

        # For every month, we calculate the monthly value, a ±10% variation and a random value between this variation
        # Also, we make a bit more natural char using logs (10 base) and a random variation, once again based on log,
        # with the logic that the random variation begins from ±10% and at the ends, falls down to ~0%.
        # The final result can be found here: https://i.imgur.com/0eF91zG.png
        # The sample has the following parameters:
        # startPrice: 50,200
        # endPrice: 157,746
        # totalMonths: 48

        oldRange = (math.log(totalMonths + 1, 10) - 0) # Starting from 1 to number of months (+1)
        newRange = (10 - 1) # Range 1 to 10 for log
        oldMin = math.log(1, 10) # 0
        newMin = 1


        for n in range(totalMonths - 1):
            calcPrice += step
            # Convert a number range to another range, maintaining ratio
            # OldRange = (OldMax - OldMin)  
            # NewRange = (NewMax - NewMin)  
            # NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
            # Source: https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio

            # What we do here actually is that we generate a 1-10 logarithmic chart based on the number of months
            logVar = (((math.log(n + 2, 10) - oldMin) * newRange) / oldRange) + newMin

            # And we apply it in the current loop, to generate a similar logic on the values here.
            logPrice = startPrice + (endPrice - startPrice) * math.log(logVar, 10)

            logPercent = 1 - math.log(10, 10) * (n + 1) / totalMonths
            data["prices"].append({
                # "month": n + 1,
                "linePrice": calcPrice,
                "lineRandom": random.uniform(calcPrice - (startPrice * fluctuation / 100), calcPrice + (startPrice * fluctuation / 100)),
                "logPrice": logPrice,
                "logRandom": random.uniform(logPrice * (1 - (logPercent / 10)), logPrice * (1 + (logPercent / 10)))
            })
        
        return data

    def generateCustomRandomPrices(self):

        startPrice = globals.tools.pickAFloat(message = "Give me the starting price", max = 100_000_000)
        endPrice = globals.tools.pickAFloat(message = "Give me the end price", min = startPrice, max = 100_000_000)
        totalMonths = globals.tools.pickAnInteger(message = "Give me the number of months to calculate", max = 120)

        data = self.doGenerateCustomRandomPrices(startPrice, endPrice, totalMonths)

        print()
        print("Starting price: ", data["startPrice"])
        print("Step          : ", data["step"])
        print("Total months  : ", data["months"])
        print("Target        : ", data["endPrice"])
        for idx, month in enumerate(data["prices"]):
            print()
            print("Month " + str(idx + 1) + ": ")
            print("  Price           : ", month["linePrice"])
            print("  Random price    : ", month["lineRandom"])
            print("  Log price       : ", month["logPrice"])
            print("  Log random price: ", month["logRandom"])

        print()
        print("Copy the data below to use it in a spreadsheet:")
        print(data)

    def generateTabbedList(self):
        excel_list = globals.database.getOptionsValue('excel_list')
        if (excel_list is None) or excel_list == "":
            print("Please update the " + chalk.greenBright("excel_list") + " parameter in settings.")
            return False

        usd_eur = globals.database.getOptionsValue('usd_eur')
        if usd_eur is None:
            usd_eur = globals.tools.updateFiatFromExchangeRatesAPI()

        listOfPrices = time.strftime('%m/%d/%Y %H:%M:%S') + "->" + usd_eur
        coinsNotListed = ""

        # And let's get the prices
        coins = excel_list.split(",")
        for coin in coins:
            res = globals.db_schema.execSelectOne("SELECT price_value FROM list_of_coins WHERE coin_code = ?", [coin])
            if res is not None:
                price, = res
                listOfPrices = listOfPrices + "->" + str(price)
            else:
                if coinsNotListed == "":
                    coinsNotListed = coin
                else:
                    coinsNotListed = coinsNotListed + ", " + coin

        # Adding data for CARPO
        listOfPrices = listOfPrices + "->1"

        print("Tabbed list of prices:")
        print(listOfPrices)
        print("")
        print("Don't forget to replace -> with tabs. :-)")

        if coinsNotListed != "":
            print("")
            print("Coins not found in the list: " + coinsNotListed)

    # ToDo
    def predictionsAndInvestments(self, coin):
        print('ToDo: predictionsAndInvestments', coin)

    def predictionsAndInvestmentsManyCoins(self):
        print('ToDo: predictionsAndInvestmentsManyCoins')

    def predictionsAndInvestmentsFictionalCoin(self):
        print('ToDo: predictionsAndInvestmentsFictionalCoin')

    def generateRandomPricesFor(self, coin):
        print('ToDo: generateRandomPricesFor', coin)
        # This function will access and crawl specific sites to get prices:
        # Nomics.co: Current price

        # BTC
        # https://longforecast.com/bitcoin-price-predictions-2017-2018-2019-btc-to-usd
        # https://coinpriceforecast.com/bitcoin-forecast-2020-2025-2030
        # https://digitalcoinprice.com/forecast/bitcoin/2021
        # https://coinmarketcap.com/currencies/bitcoin/price-estimates/ YOU NEED TO BE LOGGED IN!

        # ETH
        # https://longforecast.com/ethereum-price-prediction-2018-2019-2020-2021-eth-to-usd
        # https://coinpriceforecast.com/ethereum-forecast-2020-2025-2030
        # https://digitalcoinprice.com/forecast/ethereum/2021
        # https://coinmarketcap.com/currencies/ethereum/price-estimates/ YOU NEED TO BE LOGGED IN!

        # ADA
        # https://longforecast.com/cardano-price-prediction-2018-2019-2020-2021-ada-to-usd
        # https://coinpriceforecast.com/cardano-forecast-2020-2025-2030
        # https://digitalcoinprice.com/forecast/cardano/2021
        # https://coinmarketcap.com/currencies/cardano/price-estimates/ YOU NEED TO BE LOGGED IN!

        # BNB
        # https://longforecast.com/binance-coin
        # https://coinpriceforecast.com/binance-coin
        # https://digitalcoinprice.com/forecast/binance-coin
        # https://coinmarketcap.com/currencies/binance-coin/price-estimates/ YOU NEED TO BE LOGGED IN!

        # The plan is to get as best prediction as possible, in case of pages not providing monthly prices
        # but yearly or semi yearly prices

    def doGenerateChartFile(self, data, filename):
        print("ToDo: doGenerateChartFiles")
        # This function will get all the data generate an image file