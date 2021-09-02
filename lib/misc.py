import sys, os
from simple_chalk import chalk
from lib import globals

class Misc:

    version = "0.1"

    # def __init__(self):

    def showTheTitle(self):
        print(chalk.redBright('CryptoFinance') + ' - A finanfial tool for cryptocurrencies, ver.' + self.version)
        print(chalk.greenBright('=============================================================='))
        print()

    def doTheMenuLoop(self):
        global database
        last_menu_option = 'main'
        while True:
            self.screen_clear()
            option = self.showTheMenu(last_menu_option)
            if option == '_exit':
                print()
                print(chalk.greenBright('Thank you for working with me! Have a lovely and profitable day!'))
                print()
                globals.database.disconnect()
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

                # print('MODULE: ' + module)
                # print('TASK  : ' + task)
                # print('PARAMS: ' + 'No param' if hasParams else params)
                # print('EXEC  : globals.' + module + '.' + task)

                if hasParams:
                    eval('globals.' + module + '.' + task)(eval(params))
                else:
                    eval('globals.' + module + '.' + task)()
                print()
                input("Press enter to return to previous menu.")

    # Menu options:
    # key: keyboard key
    # value:
    #   menu: menu:[menu name]
    #   task: task:[module name]:[method name]:params
    def showTheMenu(self, menu):
        accepted_options = []
        self.showTheTitle()

        if menu == 'settings':
            print('SETTINGS:')
            print(chalk.greenBright('1.') + ' Show settings')
            print(chalk.greenBright('2.') + ' Add/Modify entry')
            print()
            print(chalk.greenBright('X.') + ' Return to main menu')
            accepted_options = [
                {"key": "1", "value": "task:database:showSettings"},
                {"key": "2", "value": "task:database:modifySettings"},
                {"key": "x", "value": "menu:main"},
            ]
        elif menu == 'predictionsAndInvestments':
            print('PREDICTIONS AND INVESTMENTS:')
            print(chalk.greenBright('1.') + ' Invest in Bitcoin (BTC)')
            print(chalk.greenBright('2.') + ' Invest in Ethereum (ETH)')
            print(chalk.greenBright('3.') + ' Invest in Cardano (ADA)')
            print(chalk.greenBright('4.') + ' Invest in Binance Coin (BNB)')
            print(chalk.greenBright('5.') + ' Invest in many coins')
            print()
            print(chalk.greenBright('X.') + ' Return to main menu')
            accepted_options = [
                {"key": "1", "value": "task:finance:predictionsAndInvestments:'btc'"},
                {"key": "2", "value": "task:finance:predictionsAndInvestments:'eth'"},
                {"key": "3", "value": "task:finance:predictionsAndInvestments:'ada'"},
                {"key": "4", "value": "task:finance:predictionsAndInvestments:'bnb'"},
                {"key": "5", "value": "task:finance:predictionsAndInvestmentsManyCoins"},
                {"key": "x", "value": "menu:main"},
            ]
        else:
            print('MAIN MENU:')
            print(chalk.greenBright('1.') + ' Predictions and Investments')
            print(chalk.greenBright('S.') + ' Settings')
            print(chalk.greenBright('A.') + ' About')
            print()
            print(chalk.greenBright('X.') + ' Exit')
            accepted_options = [
                {"key": "1", "value": "menu:predictionsAndInvestments"},
                {"key": "s", "value": "menu:settings"},
                {"key": "a", "value": "task:misc:showAbout"},
                {"key": "x", "value": "_exit"},
            ]

        while True:
            print()
            value = input("Please give your choice:\n")
            value = value.lower()
            for option in accepted_options:
                if value == option['key']:
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
            "\n" +
            "\n"
        )

