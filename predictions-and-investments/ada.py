import importlib.util
spec = importlib.util.spec_from_file_location("coins", "./../data/coins.py")
data_coins = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_coins)

spec = importlib.util.spec_from_file_location("coins", "./../lib/tools.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)

myCoins = data_coins.myCoins()

finalInvest, finalAmount = tools.calculateMonthlyRepeatedInvestment(myCoins["ada"], 500, 20)

print("")
print("Total invest : " + "$ {:,.2f}".format(finalInvest))
print("Final amount : " + "$ {:,.2f}".format(finalAmount))
print("Percentage   : " + "{:,.5f}%".format(((finalAmount - finalInvest) / finalInvest) * 100))