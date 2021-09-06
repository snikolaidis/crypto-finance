import urllib
import requests

from lib import globals

class Network:
    def callGet(self, url):
        return requests.get(url)
