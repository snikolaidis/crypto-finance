#!/usr/bin/python3

# Import libraries
import sys
import importlib.util
from simple_chalk import chalk
from lib import globals

def callTheLibFiles():
    spec = importlib.util.spec_from_file_location("coins", "./lib/database.py")
    databaseClass = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(databaseClass)
    globals.database = databaseClass.Database()

    spec = importlib.util.spec_from_file_location("coins", "./lib/misc.py")
    miscClass = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(miscClass)
    globals.misc = miscClass.Misc()

def main():
    globals.misc.doTheMenuLoop()

# Starting the app
globals.init()
callTheLibFiles()
main()