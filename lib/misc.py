import sys, os
import numpy as np
from getkey import getkey
from simple_chalk import chalk
from lib import globals

class Misc:

    version = "21.10.16.012"
    menuName = False
    menuTitles = False
    menuOptions = False

    def __init__(self):
        self.menuName = np.array([
            'main',
            'settings',
            'predictionsAndInvestments',
            'generateRandomPrices',
            'allAboutNFTs',
            'allAboutCoins',
        ])
        self.menuTitles = np.array([
            'MAIN MENU',
            'SETTINGS',
            'PREDICTIONS AND INVESTMENTS',
            'GENERATE RANDOM PRICES',
            'ALL ABOUT NFTs',
            'ALL ABOUT COINS',
        ])
        self.menuOptions = np.array([
            # main
            [
                {"key": "c", "title": "All about Coins", "value": "menu:allAboutCoins"},
                {"key": "p", "title": "Predictions and Investments", "value": "menu:predictionsAndInvestments"},
                {"key": "r", "title": "Generate random prices", "value": "menu:generateRandomPrices"},
                {"key": "n", "title": "All about NFTs", "value": "menu:allAboutNFTs"},
                {"key": "-"},
                {"key": "s", "title": "Settings", "value": "menu:settings"},
                {"key": "a", "title": "About", "value": "task:misc:showAbout"},
            ],
            # settings
            [
                {"key": "s", "title": "Show settings", "value": "task:database:showSettings"},
                {"key": "m", "title": "Add/Modify entry", "value": "task:database:setSettings"},
            ],
            # predictionsAndInvestments
            [
                {"key": "1", "title": "Predict investment in Bitcoin (BTC)", "value": "task:finance:predictionsAndInvestments:'btc'"},
                {"key": "2", "title": "Predict investment in Ethereum (ETH)", "value": "task:finance:predictionsAndInvestments:'eth'"},
                {"key": "3", "title": "Predict investment in Cardano (ADA)", "value": "task:finance:predictionsAndInvestments:'ada'"},
                {"key": "4", "title": "Predict investment in Binance Coin (BNB)", "value": "task:finance:predictionsAndInvestments:'bnb'"},
                {"key": "5", "title": "Predict investment in many coins", "value": "task:finance:predictionsAndInvestmentsManyCoins"},
                {"key": "6", "title": "Predict investment in fictional coin", "value": "task:finance:predictionsAndInvestmentsManyCoins"},
            ],
            # generateRandomPrices
            [
                {"key": "1", "title": "Generate random prices for Bitcoin (BTC)", "value": "task:finance:generateRandomPricesFor:'btc'"},
                {"key": "2", "title": "Generate random prices for Ethereum (ETH)", "value": "task:finance:generateRandomPricesFor:'eth'"},
                {"key": "3", "title": "Generate random prices for Cardano (ADA)", "value": "task:finance:generateRandomPricesFor:'ada'"},
                {"key": "4", "title": "Generate random prices for Binance Coin (BNB)", "value": "task:finance:generateRandomPricesFor:'bnb'"},
                {"key": "5", "title": "Generate custom random prices", "value": "task:finance:generateCustomRandomPrices"},
            ],
            # allAboutNFTs
            [
                {"key": "1", "title": "Generate all combinations", "value": "task:nft:generateAllCombinations"},
                {"key": "2", "title": "Select random image(s)", "value": "task:nft:selectRandomImages"},
            ],
            # allAboutCoins
            [
                {"key": "1", "title": "Coins supported", "value": "task:finance:getCoinsSupported"},
                {"key": "2", "title": "Add new coin", "value": "task:finance:addCoinsSupported"},
                {"key": "3", "title": "Remove existing coin", "value": "task:finance:removeCoinsSupported"},
                {"key": "4", "title": "Generate tabbed list", "value": "task:finance:generateTabbedList"},
                {"key": "-"},
                {"key": "u", "title": "Update coins", "value": "task:finance:updateCoinsSupported"},
                {"key": "a", "title": "Coin Analysis", "value": "task:finance:updateHistoryOfAllCoins"},
            ],
        ], dtype="object")

    def showTheTitle(self):
        print(chalk.redBright('CryptoFinance') + ' - A financial tool for cryptocurrencies, ' + chalk.greenBright('ver.' + self.version))
        print(chalk.greenBright('======================================================================='))
        print()


    def doTheMenuLoop(self):
        last_menu_option = 'main'
        while True:
            self.screen_clear()
            option = self.showTheMenu(last_menu_option)
            if option == '_exit':
                print()
                print(chalk.greenBright('Thank you for working with me! Have a lovely and profitable day!'))
                print()
                globals.db_schema.disconnect()
                self.screen_clear()
                sys.exit()

            # Analyze the option
            options = option.split(':')
            if options[0] == 'menu':
                last_menu_option = options[1]
            elif options[0] == 'task':
                self.screen_clear()
                self.showTheTitle()

                module = options[1]
                task = options[2]
                hasParams = True
                try:
                    params = options[3]
                except:
                    hasParams = False

                if hasParams:
                    eval('globals.' + module + '.' + task)(eval(params))
                else:
                    eval('globals.' + module + '.' + task)()
                print()
                print("---------------------------------------")
                print("Press any key to return to previous menu.")
                print()
                getkey()


    # Menu options:
    # key: keyboard key
    # value:
    #   menu: menu:[menu name]
    #   task: task:[module name]:[method name]:params
    def showTheMenu(self, menu):
        accepted_options = []
        self.showTheTitle()

        print(self.menuTitles[self.menuName == menu][0] + ':')
        accepted_options = self.menuOptions[self.menuName == menu][0][:]
        
        accepted_options.append({"key": "-"})

        if menu == 'main':
            accepted_options.append({"key": "x", "title": "Exit", "value": "_exit"})
        else:
            accepted_options.append({"key": "x", "title": "Return to main menu", "value": "menu:main"})

        for option in accepted_options:
            if option['key'] == "-":
                print()
            else:
                print(chalk.greenBright('[' + option['key'].upper() + '] ') + option['title'])

        print()

        while True:
            key = getkey()
            key = key.lower()
            for option in accepted_options:
                if key == option['key']:
                    return option['value']

    # https://www.tutorialspoint.com/how-to-clear-screen-in-python
    def screen_clear(self):
        # for mac and linux(here, os.name is 'posix')
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            # for windows platfrom
            _ = os.system('cls')
        # print out some text


    def showAbout(self):
        print(
            "Welcome to " + chalk.redBright('CryptoFinance') + ", ver." + self.version + "!\n"
            "\n" +
            "My name is " + chalk.green("Stratos Nikolaidis") + " and although being a professional Software Engineer since 2000, I'm rather new in python. So, please bear with me if there's a python expert who's reading this text and might think “what on earth he was thinking when he wrote this crap?”\n" +
            "\n" +
            "So, what's the story about " + chalk.redBright('CryptoFinance') + "?\n" +
            "\n" +
            "Obviously, I like crypto currencies. Yeap, that's true. I try to study them, try to under their logic, their technology, their trading logic etc.\n" +
            "\n" +
            "Disclaimer: I am not a financial advisor. If you want financial advice, find a financial advisor. What I do here, is for tutorial and educational purposes only.\n" +
            "\n" +
            "Now that we clarified that, let's go back to what I was saying: I like crypto currencies. In the same time, it was time to start learning python; I didn't have the luxury of using it earlier and now, as it looks like, it was time to do so.\n" +
            "\n" +
            "And while trying to figure out what projects to work on, I thought that writing something that has to do with crypto currencies would be awesome. Of course, everyrhing here is purely fictional. Just to make it clear. And it's actually playing with numbers. Not actual data. At least for now, I'm planning to add some real data, like taking the current price of crypto currencies etc.\n" +
            "\n" +
            "But that's all for now. Let's go back to work.\n" +
            "\n" +
            "Thank you,\n" +
            chalk.green("Stratos Nikolaidis")
        )

