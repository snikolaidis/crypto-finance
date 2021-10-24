#!/usr/bin/python3

# System libraries
import sys
import importlib.util
from simple_chalk import chalk

# Custom libraries
from lib import globals
from lib import db_schema
from lib import database
from lib import finance
from lib import misc
from lib import tools
from lib import network
from lib import scrapers
from lib import nft
from lib import fintools

def initTheLibraries():
    globals.db_schema = db_schema.DB_Schema()
    globals.database = database.Database()
    globals.finance = finance.Finance()
    globals.misc = misc.Misc()
    globals.tools = tools.Tools()
    globals.network = network.Network()
    globals.scrapers = scrapers.Scrapers()
    globals.nft = nft.Nft()
    globals.fintools = fintools.FinTools()

def main():
    globals.misc.doTheMenuLoop()

# Starting the app
globals.init()
initTheLibraries()
main()
