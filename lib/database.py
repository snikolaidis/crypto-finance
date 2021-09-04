import sqlite3
from simple_chalk import chalk

class Database:

    conn = False
    version = -1

    def __init__(self):
        self.connect()
        self.getVersion()
        self.updateDatabase()

    def connect(self):
        print("Connecting to database")
        self.conn = sqlite3.connect('./database/database.db')

    # Commit all pending changes
    # Close the connection
    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    def getVersion(self):
        print("Get current version")
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master 'database' WHERE type='table' AND name='options'")
        rows = cur.fetchall()
        if len(rows) == 0:
            self.version = -1
        else:
            self.version = 0
            cur.execute("SELECT option_value FROM options WHERE option_name = 'version'")
            self.version = int(cur.fetchone()[0])
        print("Database version: " + str(self.version))
    
    def updateDatabase(self):
        cur = self.conn.cursor()
        prev_version = self.version

        # Version 0:
        # Initial tables
        if self.version < 0:
            print("Upgrading database to version " + str(self.version))
            cur.execute("""CREATE TABLE options (
                id INTEGER PRIMARY KEY,
                option_name TEXT NOT NULL,
                option_value TEXT NOT NULL
            )""")

            self.version = 0
            print("Upgrading database to version " + str(self.version))
            cur.execute("INSERT INTO options (option_name, option_value) values (?, ?)", ('version', self.version))
            self.conn.commit()
        
        # Version 1:
        # List of coins - initial coins (BTC, ETH, ADA)
        if self.version < 1:
            cur.execute("""CREATE TABLE list_of_coins (
                id INTEGER PRIMARY KEY,
                coin_name TEXT NOT NULL,
                coin_code TEXT NOT NULL
            );""")
            coin_list = [
                ('Bitcoin', 'BTC'),
                ('Ethereum', 'ETH'),
                ('Cardano', 'ADA'),
            ]
            cur.executemany("INSERT INTO list_of_coins (coin_name, coin_code) VALUES (?, ?)", coin_list)

            self.version = 1
            print("Upgrading database to version " + str(self.version))
            cur.execute("UPDATE options set option_value = ? where option_name = ?", [self.version, 'version'])
            self.conn.commit()
        
        # Version 2:
        # List of coins - indeces
        if self.version < 2:
            cur.execute("ALTER TABLE list_of_coins ADD COLUMN price_value REAL NULL")
            cur.execute("ALTER TABLE list_of_coins ADD COLUMN price_date TEXT NULL")
            cur.execute("CREATE INDEX list_of_coins_IDX_coin_code ON list_of_coins(coin_code)")

            self.version = 2
            print("Upgrading database to version " + str(self.version))
            cur.execute("UPDATE options set option_value = ? where option_name = ?", [self.version, 'version'])
            self.conn.commit()

        # Version 2:
        # List of coins - Adding BNB
        if self.version < 3:
            cur.execute("INSERT INTO list_of_coins (coin_name, coin_code) VALUES (?, ?)", ["Binance Coin", "BNB"])

            self.version = 3
            print("Upgrading database to version " + str(self.version))
            cur.execute("UPDATE options set option_value = ? where option_name = ?", [self.version, 'version'])
            self.conn.commit()

        # End of database migration
        if prev_version != self.version:
            print("Database upgrade completed")
        else:
            print("Database is in latest version")
    
    def getOptionsValue(self, key):
        cur = self.conn.cursor()
        cur.execute("SELECT option_value FROM options WHERE option_name = ?", [key.lower()])
        rec = cur.fetchone()
        if rec != None:
            return  rec[0]
        else:
            return None
    
    def setOptionsValue(self, key, value):
        cur = self.conn.cursor()
        curVal = self.getOptionsValue(key)
        if curVal != None:
            cur.execute("UPDATE options SET option_value = ? WHERE option_name = ?", [value, key.lower()])
        else:
            cur.execute("INSERT INTO options (option_name, option_value) values (?, ?)", [key.lower(), value])
        self.conn.commit()

    def showSettings(self):
        cur = self.conn.cursor()
        cur.execute("SELECT option_name, option_value FROM options ORDER BY option_name")
        rows = cur.fetchall()
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
        
    def getSupportedCoins(self, coin = "_all"):
        cur = self.conn.cursor()
        if coin == "_all":
            cur.execute("SELECT id, coin_name, coin_code, price_value, price_date FROM list_of_coins ORDER BY coin_code")
            return cur.fetchall()
        else:
            cur.execute("SELECT id, coin_name, coin_code, price_value, price_date FROM list_of_coins WHERE coin_code=?", [coin])
            return cur.fetchone()

    def setCoinInformation(self, coin, price, date):
        cur = self.conn.cursor()
        cur.execute("UPDATE list_of_coins SET price_value=?, price_date=? WHERE coin_code=?", [price, date, coin.upper()])
        self.conn.commit()

