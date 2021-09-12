import re
from bs4 import BeautifulSoup
from datetime import date
from lib import globals

class Scrapers:
    def analyzeLongforecastCom(self, url):
        prices = {}

        res = globals.network.callGet(url)
        if res.status_code != 200:
            return False

        soup = BeautifulSoup(res.content, "html.parser")
        tables = soup.find_all("table")

        if len(tables) != 4:
            return prices

        # Parse and scrap the 3rd and 4th table
        for table_no in [2, 3]:
            current_year = '0'
            rows = tables[table_no].find_all("tr")
            for row in rows:
                # We're on a year selection:
                cells = row.find_all("td")
                if len(cells) == 1:
                    yearTitle = cells[0].get_text().strip().split(" ")
                    if len(yearTitle) == 1:
                        prices[yearTitle[0]] = {}
                    current_year = yearTitle[0]
                        
                elif current_year != '0':
                    monthNo = str(globals.tools.getTheMonthFromShort(cells[0].get_text().strip()))
                    prices[str(current_year)][monthNo] = float(cells[3].get_text().strip())

        return prices

    def analyzeCoinpriceforecastCom(self, url):
        prices = {}
        temp_prices = {}

        res = globals.network.callGet(url)
        if res.status_code != 200:
            return False

        soup = BeautifulSoup(res.content, "html.parser")

        # Get the current price of the coin
        h2 = soup.find("h2")
        h2_s = h2.get_text().strip().split("$")
        todayPrice = float(h2_s[1].replace(",", ""))

        todays_date = date.today()
        currentMonth = todays_date.month
        currentYear = todays_date.year

        table = soup.find("table")

        if table is None:
            return prices

        rows = table.find_all("tr")
        for row in rows[1:]:
            # We're on a year selection:
            cells = row.find_all("td")
            yearTitle = cells[0].get_text().strip()

            # Mid price
            mid_price = cells[1].get_text().strip()
            mid_price = float(mid_price.replace("$", "").replace(",", ""))
            # End of year price
            end_price = cells[2].get_text().strip()
            end_price = float(end_price.replace("$", "").replace(",", ""))

            temp_prices[yearTitle] = {
                "mid": mid_price,
                "end": end_price,
            }

        # Now is the part where things are getting a bit more complicated. For the future years,
        # we have two prices, mid and end of year. And also we have the today's price. What we
        # will do is to generate the in-between prices using the doGenerateCustomRandomPrices function,
        # calling if for the intermediate 5 months. Let's see where it will lead us.
        
        priceFromLastPeriod = todayPrice
        # We will start by taking the date and price of the beginning of the month, to start building the logic.
        for row in enumerate(temp_prices):
            current_year = row[1]
            prices[str(current_year)] = {}

            # If we are in the first (current) year, we need to be a bit more careful, because we have to take
            # just a part of it.
            if str(current_year) == str(currentYear):
                # Are we in the first half of the year?
                print('ToDo')

            else:
                # First half
                randomPrices = globals.finance.doGenerateCustomRandomPrices(priceFromLastPeriod, temp_prices[current_year]["mid"], 6, 5)
                monthNo = 0
                for price in randomPrices["prices"]:
                    monthNo += 1
                    prices[str(current_year)][str(monthNo)] = price["lineRandom"]

                monthNo += 1
                prices[str(current_year)][str(monthNo)] = temp_prices[current_year]["mid"]

                # Second half
                randomPrices = globals.finance.doGenerateCustomRandomPrices(temp_prices[current_year]["mid"], temp_prices[current_year]["end"], 6, 5)
                for price in randomPrices["prices"]:
                    monthNo += 1
                    prices[str(current_year)][str(monthNo)] = price["lineRandom"]

                monthNo += 1
                prices[str(current_year)][str(monthNo)] = temp_prices[current_year]["end"]

            priceFromLastPeriod = temp_prices[str(current_year)]["end"]

        # currentMonth
        # dateBeginningOfTheMonth

        # And afterwards, the price in the beginning of the month; we call it priceBeginningOfPeriod because we
        # will make the loop for the whole array
        # priceBeginningOfPeriod

        # Finally, since we know that the first row of the temp_prices is the current year, let's start building 

        return prices

