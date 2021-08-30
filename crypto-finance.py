import importlib.util
spec = importlib.util.spec_from_file_location("coins", "./lib/database.py")
database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database)
db = database.Database()