import random, math, json, time
from lib import globals
from datetime import datetime
from dateutil.relativedelta import relativedelta
from simple_chalk import chalk
import time
import pandas_ta as ta
import yfinance as yf

class FinTools:

    def updatePricesFromNomics(self):
        nomicsKey = globals.tools.getNomicsKey()
        if nomicsKey == None:
            return False

        # Get list of coins
        coinList = ''
        rows = globals.db_schema.execSelect("SELECT coin_code FROM list_of_coins")
        for row in rows:
            if coinList == '':
                coinList = row[0]
            else:
                coinList = coinList + "," + row[0]

        res = globals.network.callGet("https://api.nomics.com/v1/currencies/ticker?ids=" + coinList + "&interval=1d,30d&convert=USD&per-page=100&page=1&key=" + nomicsKey)
        if res:
            data = json.loads(res.text)
            for coin in data:
                rank = 999
                try:
                    rank = coin['rank']
                except:
                    pass
                globals.database.setCoinInformation(coin['currency'], coin['price'], coin['price_date'], rank)

        return True

    def updateFiatFromExchangeRatesAPI(self):
        exchangeRatesAPIKey = globals.tools.getExchangeRatesAPIKey()
        if exchangeRatesAPIKey == None:
            return False

        res = globals.network.callGet("http://api.exchangeratesapi.io/v1/latest?format=1&access_key=" + exchangeRatesAPIKey)
        if res:
            data = json.loads(res.text)
            globals.database.setOptionsValue('usd_eur', 1 / data['rates']['USD'])
            return 1 / data['rates']['USD']

        return False

    def updateHistoryOfCoin(self, coin_code, replace = False, echo = False):
        if echo:
            print("Updating " + chalk.greenBright(coin_code))
        
        coinHistoryPeriod = globals.database.getOptionsValue('coinHistoryPeriod', '1y')

        df = yf.Ticker(coin_code.upper() + '-USD').history(period='3y')[map(str.title, ['open', 'close', 'low', 'high', 'volume'])]

        # Add MACD
        df.ta.macd(close='close', fast=9, slow=13, append=True)

        # Add Pethagorean bottom
        pethagorean_bottom = []
        for index, row in df.iterrows():
            clearNumber = int(str(row["Close"]).replace(".", ""))

            # We call the procedure twice
            pb = sum(map(int, str(clearNumber)))
            while len(str(pb)) > 1:
                pb = sum(map(int, str(pb)))
            pethagorean_bottom.append(pb)

        df['pethagorean_bottom'] = pethagorean_bottom

        df.to_sql('fin_analysis_' + coin_code, globals.db_schema.getConnection(), if_exists = 'replace' if replace else 'append' )
        time.sleep(3)
        return True
        
    def updateHistoryOfCoin_old(self, coin_code, echo = False):
        nomicsKey = globals.tools.getNomicsKey()
        if nomicsKey == None:
            return False

        if echo:
            print("Updating " + chalk.greenBright(coin_code) + ":")

        # Get list of coins
        coin_code = coin_code.upper()
        coin_date, = globals.db_schema.execSelectOne("SELECT max(coin_date) FROM history_of_coins WHERE coin_code = ?", [coin_code])
        
        # If there's no record, we need to see when we will start from:
        if coin_date is None:
            print("   First candle date for " + chalk.greenBright(coin_code))
            ticker = globals.network.callGet("https://api.nomics.com/v1/currencies/ticker?ids=" + coin_code + "&key=" + nomicsKey)
            if ticker:
                data = json.loads(ticker.text)
                if len(data) > 0:
                    first_candle = globals.tools.getDateFromString(data[0]["first_candle"])
                    if first_candle.year < 2018:
                        coin_date = '2018-01-01T00:00:00'
                    else:
                        coin_date = first_candle.isoformat()
            else:
                if echo:
                    print("   " + chalk.redBright("Error while getting information about " + coin_code))
                return False

            print("   First date will be " + chalk.greenBright(coin_date))
            time.sleep(3)
            startDate = globals.tools.getDateFromString(coin_date)
        else:

            # We will start from the next day of the day we're working
            startDate = globals.tools.getDateFromString(coin_date) +  relativedelta(days=+1)

        endDate = globals.tools.lastDayOfTheMonth(startDate)
        today = datetime.now()

        if startDate > today:
            if echo:
                print("   " + chalk.greenBright("No updates necessary"))
                time.sleep(0.5)
            return True

        cont = True
        hasUpdates = False
        while cont:
            sparkline = globals.network.callGet("https://api.nomics.com/v1/currencies/sparkline?key=" + nomicsKey + "&ids=" + coin_code + "&start=" + startDate.isoformat() + "Z&end=" + endDate.isoformat() + "Z")
            if sparkline:
                data = json.loads(sparkline.text)
                if len(data) > 0 and len(data[0]['prices']) > 0:
                    if echo:
                        print("   " + chalk.greenBright(startDate.strftime('%B %Y')))
                    hasUpdates = True

                    for i in range(len(data[0]['prices'])):
                        globals.database.addCoinHistory(coin_code, data[0]['timestamps'][i], data[0]['prices'][i])

                if today > endDate:
                    startDate = globals.tools.getNextMonth(startDate)
                    endDate = globals.tools.lastDayOfTheMonth(startDate)
                else:
                    cont = False

            else:
                cont = False

            if (not hasUpdates) and echo:
                print("   " + chalk.greenBright("No updates necessary"))

            time.sleep(3)


        return True
