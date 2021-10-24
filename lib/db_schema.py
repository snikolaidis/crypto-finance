import sqlite3
from simple_chalk import chalk

class DB_Schema:

    conn = False
    version = -1

    def __init__(self):
        self.connect()
        self.getVersion()
        self.updateDatabase()

    def connect(self):
        print("Connecting to database")
        self.conn = sqlite3.connect('./database/database.db')

    def getConnection(self):
        return self.conn

    # Commit all pending changes
    # Close the connection
    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    def getVersion(self):
        print("Get current version")
        rowsCnt, = self.execSelectOne("SELECT COUNT(*) FROM sqlite_master 'database' WHERE type='table' AND name='options'")
        if int(rowsCnt) == 0:
            self.version = -1
        else:
            rowVer, = self.execSelectOne("SELECT option_value FROM options WHERE option_name = 'version'")
            self.version = int(rowVer)
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

        # Version 3:
        # List of coins - Adding BNB
        if self.version < 3:
            cur.execute("INSERT INTO list_of_coins (coin_name, coin_code) VALUES (?, ?)", ["Binance Coin", "BNB"])

            self.version = 3
            print("Upgrading database to version " + str(self.version))
            cur.execute("UPDATE options set option_value = ? where option_name = ?", [self.version, 'version'])
            self.conn.commit()

        # Version 4:
        # New module: NFTs
        if self.version < 4:
            cur.execute("""CREATE TABLE nft_all_conbinations (
                id INTEGER PRIMARY KEY,
                code TEXT NOT NULL,
                uuid TEXT NOT NULL,
                used INTEGER NOT NULL,
                uncommon_id INTEGER NOT NULL
            );""")
            cur.execute("CREATE INDEX nft_all_conbinations_IDX_code ON nft_all_conbinations(code)")
            cur.execute("CREATE INDEX nft_all_conbinations_IDX_uuid ON nft_all_conbinations(uuid)")
            cur.execute("CREATE INDEX nft_all_conbinations_IDX_used ON nft_all_conbinations(used)")
            cur.execute("CREATE INDEX nft_all_conbinations_IDX_uncommon_id ON nft_all_conbinations(uncommon_id)")

            # uncommon_level: how may uncommon features are there
            # uncommon_fields: per feature, uncommon level: 0-1-0-0-0: All features are common, 2nd feature is uncommon
            cur.execute("""CREATE TABLE nft_uncommon_conbinations (
                id INTEGER PRIMARY KEY,
                common_id INTEGER NOT NULL,
                uncommon_level INTEGER NOT NULL,
                uncommon_fields TEXT NOT NULL
            );""")
            cur.execute("CREATE INDEX nft_uncommon_conbinations_IDX_common_id ON nft_uncommon_conbinations(common_id)")
            cur.execute("CREATE INDEX nft_uncommon_conbinations_IDX_uncommon_level ON nft_uncommon_conbinations(uncommon_level)")
            cur.execute("CREATE INDEX nft_uncommon_conbinations_IDX_uncommon_fields ON nft_uncommon_conbinations(uncommon_fields)")

            self.version = 4
            print("Upgrading database to version " + str(self.version))
            cur.execute("UPDATE options set option_value = ? where option_name = ?", [self.version, 'version'])
            self.conn.commit()

        # Version 5:
        # New module: NFTs
        if self.version < 5:
            cur.execute("ALTER TABLE nft_all_conbinations ADD COLUMN used_date TEXT NULL")
            cur.execute("CREATE INDEX nft_all_conbinations_IDX_used_date ON nft_all_conbinations(used_date)")

            self.version = 5
            print("Upgrading database to version " + str(self.version))
            cur.execute("UPDATE options set option_value = ? where option_name = ?", [self.version, 'version'])
            self.conn.commit()

        # Version 6:
        # Add rank in coins
        if self.version < 6:
            cur.execute("ALTER TABLE list_of_coins ADD COLUMN rank INTEGER NULL")

            self.version = 6
            print("Upgrading database to version " + str(self.version))
            cur.execute("UPDATE options set option_value = ? where option_name = ?", [self.version, 'version'])
            self.conn.commit()

        # Version 7:
        # Add rank in coins
        if self.version < 7:
            cur.execute("""CREATE TABLE history_of_coins (
                id INTEGER PRIMARY KEY,
                coin_code TEXT NOT NULL,
                coin_date TEXT NULL,
                price REAL NULL
            );""")
            cur.execute("CREATE INDEX history_of_coins_IDX_code ON history_of_coins(coin_code)")
            cur.execute("CREATE INDEX history_of_coins_IDX_date ON history_of_coins(coin_date)")
            cur.execute("CREATE INDEX history_of_coins_IDX_code_date ON history_of_coins(coin_code, coin_date)")

            self.version = 7
            print("Upgrading database to version " + str(self.version))
            cur.execute("UPDATE options set option_value = ? where option_name = ?", [self.version, 'version'])
            self.conn.commit()

        # End of database migration
        if prev_version != self.version:
            print("Database upgrade completed")
        else:
            print("Database is in latest version")


    def execSQL(self, sql, params = None):
        cur = self.conn.cursor()
        if params is None:
            cur.execute(sql)
        else:
            cur.execute(sql, params)
        self.execCommit()
        
    def execCommit(self):
        self.conn.commit()
        
    def execSelect(self, sql, params = None):
        cur = self.conn.cursor()
        if params is None:
            cur.execute(sql)
        else:
            cur.execute(sql, params)
        return cur.fetchall()
        
    def execSelectOne(self, sql, params = None):
        cur = self.conn.cursor()
        if params is None:
            cur.execute(sql)
        else:
            cur.execute(sql, params)
        return cur.fetchone()
