import urllib
import requests

from lib import globals

class Network:
    def callGet(self, url):
        res = requests.get(url)
        if res.status_code == 200:
            return res
        else:
            raise ConnectionError([
                "Error while calling: " + url,
                res
            ])
            return False
