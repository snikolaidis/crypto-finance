def getThePrice(arrayOfPrices, method = "avg"):
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
