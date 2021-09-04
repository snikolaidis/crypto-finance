from requests import NullHandler
from lib import globals
from simple_chalk import chalk

class Finance:

    def calculateMonthlyRepeatedInvestment(coin, monthly_invest = 500, yearly_perc_increase = 20, method = "avg", initial_amount = 0):
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
            print(coin[1] + ' (' + chalk.green(coin[2]) + ')')
            if coin[3] is not None:
                print("  Price: " + chalk.green('{:,}'.format(coin[3])))
            if coin[4] is not None:
                print("  Date: " + chalk.green(coin[4]))

    def updateCoinsSupported(self):
        if globals.tools.updatePricesFromNomics() == False:
            print("There was an error while updating the system, please check and make sure you have the key " + chalk.green("nomics") + " configured in the settings.")
        else:
            print("All coins are updated.")

    def generateRandomPricesFor(self, coin):
        print('ToDo: generateRandomPricesFor', coin)


    # ToDo
    def predictionsAndInvestments(self, coin):
        print('ToDo: predictionsAndInvestments', coin)

    def predictionsAndInvestmentsManyCoins(self):
        print('ToDo: predictionsAndInvestmentsManyCoins')

    def predictionsAndInvestmentsFictionalCoin(self):
        print('ToDo: predictionsAndInvestmentsFictionalCoin')

    def generateCustomRandomPrices(self):
        print('ToDo: generateCustomRandomPrices')