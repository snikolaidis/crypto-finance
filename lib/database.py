import sqlite3

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

    def disconnect(self):
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
            rows = cur.fetchall()
            for row in rows:
                self.version = int(row[0])
        print("Database version: " + str(self.version))

    def updateDatabase(self):
        cur = self.conn.cursor()
        prev_version = self.version

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
            cur.execute("UPDATE options set option_value = ? where option_name = ?", (self.version, 'version'))
            self.conn.commit()
        
        if self.version < 2:
            cur.execute("ALTER TABLE list_of_coins ADD COLUMN price_value REAL NULL")
            cur.execute("ALTER TABLE list_of_coins ADD COLUMN price_date TEXT NULL")
            cur.execute("CREATE INDEX list_of_coins_IDX_coin_code ON list_of_coins(coin_code)")

            self.version = 2
            print("Upgrading database to version " + str(self.version))
            cur.execute("UPDATE options set option_value = ? where option_name = ?", (self.version, 'version'))
            self.conn.commit()

        if prev_version != self.version:
            print("Database upgrade completed")
        else:
            print("Database is in latest version")