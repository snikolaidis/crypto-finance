import importlib.util
spec = importlib.util.spec_from_file_location("coins", "./../data/coins.py")
data_coins = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_coins)

spec = importlib.util.spec_from_file_location("coins", "./../lib/tools.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)

myCoins = data_coins.myCoins()

finalInvest = 0
finalAmount = 0

coinInvest, coinAmount = tools.calculateMonthlyRepeatedInvestment(myCoins["btc"], 200, 25)
finalInvest += coinInvest
finalAmount += coinAmount

coinInvest, coinAmount = tools.calculateMonthlyRepeatedInvestment(myCoins["eth"], 150, 25)
finalInvest += coinInvest
finalAmount += coinAmount

coinInvest, coinAmount = tools.calculateMonthlyRepeatedInvestment(myCoins["ada"], 150, 25)
finalInvest += coinInvest
finalAmount += coinAmount


print("")
print("Total invest : " + "$ {:,.2f}".format(finalInvest))
print("Final amount : " + "$ {:,.2f}".format(finalAmount))
print("Percentage   : " + "{:,.5f}%".format(((finalAmount - finalInvest) / finalInvest) * 100))