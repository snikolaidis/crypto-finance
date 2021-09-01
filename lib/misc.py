import sys, os
from simple_chalk import chalk
from lib import globals

class Misc:

    # def __init__(self):

    def showTheTitle(sefl):
        print(chalk.redBright('CryptoFinance') + ' - A finanfial tool for cryptocurrencies, ver.0.1')
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
                sys.exit()

            # Analyze the option
            options = option.split(':')
            if options[0] == 'menu':
                last_menu_option = options[1]
            elif options[0] == 'task':
                self.screen_clear()
                self.showTheTitle()
                print('MODULE: ' + options[1])
                print('TASK  : ' + options[2])
                print('EXEC  : globals.' + options[1] + '.' + options[2])
                eval('globals.' + options[1] + '.' + options[2])()
                print()
                input("Press enter to return to previous menu.")

    # Menu options:
    # key: keyboard key
    # value:
    #   menu: menu:[menu name]
    #   task: task:[module name]:[method name]:[request parameters: true/false]
    def showTheMenu(self, menu):
        print('')
        accepted_options = []

        self.showTheTitle()

        if menu == 'settings':
            print('SETTINGS:')
            print(chalk.greenBright('1.') + ' Show settings')
            print(chalk.greenBright('2.') + ' Add/Modify entry')
            print()
            print(chalk.greenBright('X.') + ' Return to main menu')
            accepted_options = [
                {"key": "1", "value": "task:database:showSettings:false"},
                {"key": "2", "value": "task:database:modifySettings:true"},
                {"key": "x", "value": "menu:main"},
            ]
        elif menu == 'predictionsAndInvestments':
            print('PREDICTIONS AND INVESTMENTS:')
            print(chalk.greenBright('1.') + ' Invest in Bitcoin (BTC)')
            print(chalk.greenBright('2.') + ' Invest in Ethereum (ETH)')
            print(chalk.greenBright('3.') + ' Invest in Cardano (ADA)')
            print(chalk.greenBright('4.') + ' Invest in Binance Coin (BNB)')
            print(chalk.greenBright('4.') + ' Invest in Binance Coin (BNB)')
            print()
            print(chalk.greenBright('X.') + ' Return to main menu')
            accepted_options = [
                {"key": "1", "value": "task:predictionsAndInvestments:btc:true"},
                {"key": "2", "value": "task:predictionsAndInvestments:eth:true"},
                {"key": "3", "value": "task:predictionsAndInvestments:ada:true"},
                {"key": "4", "value": "task:predictionsAndInvestments:bnb:true"},
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
                {"key": "a", "value": "task:misc:showAbout:false"},
                {"key": "x", "value": "_exit"},
            ]

        while True:
            print()
            value = input("Please give your choice:\n")
            value = value.lower()
            for option in accepted_options:
                if value == option['key']:
                    return option['value']

    def hello(self):
        print('hello')

    # https://www.tutorialspoint.com/how-to-clear-screen-in-python
    def screen_clear(self):
        # for mac and linux(here, os.name is 'posix')
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            # for windows platfrom
            _ = os.system('cls')
        # print out some text
