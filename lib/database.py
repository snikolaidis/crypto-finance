import sqlite3
from lib import globals
from simple_chalk import chalk

class Database:
    
    def getOptionsValue(self, key):
        rec, = globals.db_schema.execSelectOne("SELECT option_value FROM options WHERE option_name = ?", [key.lower()])
        return rec
    
    def setOptionsValue(self, key, value):
        curVal = self.getOptionsValue(key)
        if curVal != None:
            globals.db_schema.execSQL("UPDATE options SET option_value = ? WHERE option_name = ?", [value, key.lower()])
        else:
            globals.db_schema.execSQL("INSERT INTO options (option_name, option_value) values (?, ?)", [key.lower(), value])

    def showSettings(self):
        rows = globals.db_schema.execSelect("SELECT option_name, option_value FROM options ORDER BY option_name")
        for row in rows:
            print("[" + row[0] + "] : ", chalk.green(row[1]))

    def setSettings(self):
        key = input("Give me the key: ")
        key = key.lower()
        value = self.getOptionsValue(key)
        if value != None:
            print("Updating existing key")
            print("Current value:", chalk.green(value))
        else:
            print("Adding new key")

        value = input("Enter the new value: ")
        self.setOptionsValue(key, value)

        if value != None:
            print("Value is updated.")
        else:
            print("Key is added.")

    def getSettings(self, key):
        key = print("Give me the key: ")
        return self.getOptionsValue(key)

    # ToDo: Refactor the following calls by moving them to finance and using execCommand, execSelect and execSelectOne methods
    def getSupportedCoins(self, coin = "_all"):
        if coin == "_all":
            return globals.db_schema.execSelect("SELECT id, coin_name, coin_code, price_value, price_date, rank FROM list_of_coins ORDER BY rank")
        else:
            rec, = globals.db_schema.execSelectOne("SELECT id, coin_name, coin_code, price_value, price_date, rank FROM list_of_coins WHERE coin_code=?", [coin])
            return rec

    def setCoinInformation(self, coinCode, price, date, rank, coinName = ''):
        rowsCnt, = globals.db_schema.execSelectOne("SELECT COUNT(*) FROM list_of_coins 'database' WHERE coin_code = ?", [coinCode])
        if int(rowsCnt) == 0:
            globals.db_schema.execSQL("INSERT INTO list_of_coins (coin_name, coin_code, price_value, price_date, rank) VALUES (?, ?, ?, ?, ?)", [coinName, coinCode.upper(), price, date, rank])
        else:
            globals.db_schema.execSQL("UPDATE list_of_coins SET price_value=?, price_date=?, rank=? WHERE coin_code=?", [price, date, rank, coinCode.upper()])

    def unsetCoinInformation(self, coinCode):
        globals.db_schema.execSQL("DELETE FROM list_of_coins WHERE coin_code = ?", [coinCode])
