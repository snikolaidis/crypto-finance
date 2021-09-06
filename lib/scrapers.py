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

        for table_no in [2, 3]:
            current_year = '0'
            rows = tables[table_no].find_all("tr")
            for row in rows:
                # We're on a year selection:
                cells = row.find_all("td")
                if len(cells) == 1:
                    yearTitle = cells[0].get_text().split(" ")
                    if len(yearTitle) == 1:
                        prices[yearTitle[0]] = {}
                    current_year = yearTitle[0]
                        
                elif current_year != '0':
                    monthNo = str(globals.tools.getTheMonthFromShort(cells[0].get_text()))
                    prices[str(current_year)][monthNo] = float(cells[3].get_text())

        return prices