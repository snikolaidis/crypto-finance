#!/usr/bin/python3

# System libraries
import sys
import importlib.util
from simple_chalk import chalk

# Custom libraries
from lib import globals
from lib import database
from lib import finance
from lib import misc
from lib import tools
from lib import network
from lib import scrapers
from lib import nft

def initTheLibraries():
    globals.database = database.Database()
    globals.finance = finance.Finance()
    globals.misc = misc.Misc()
    globals.tools = tools.Tools()
    globals.network = network.Network()
    globals.scrapers = scrapers.Scrapers()
    globals.nft = nft.Nft()

def main():
    globals.misc.doTheMenuLoop()

# Starting the app
globals.init()
initTheLibraries()
main()
