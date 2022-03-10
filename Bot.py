import requests
from datetime import datetime
import json

class Bot:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': '1000',
            'convert': 'USD',
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '0e3c2234-a17e-4fb2-ad21-775bafaaef58',
        }
        self.currencies = {}
        self.orders = []
        self.report = {}

    def fetchCurrencyData(self):
        data = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return data['data']

    def maxVolumeLast24h(self, collection):
        cryptoBestVolume = None
        for item in collection:

            if not cryptoBestVolume or item['quote']['USD']['volume_24h'] > cryptoBestVolume['quote']['USD']['volume_24h']:
                cryptoBestVolume = item
        self.report['maxVolumeLast24h'] = {"symbol":cryptoBestVolume['symbol'], "maxVolume":cryptoBestVolume['quote']['USD']['volume_24h']}

    def bestCryptoLast24h(self, collection):
        orderBestCollection = []
        orderWorstCollection = []

        worstCollection = sorted(collection, key=lambda i: i['quote']['USD']['percent_change_24h'])
        bestCollection = sorted(collection, key=lambda i: i['quote']['USD']['percent_change_24h'],reverse=True)

        worst10 = worstCollection[0:10]
        best10 = bestCollection[0:10]

        for best in best10:
            orderBestCollection.append({"symbol":best['symbol'], "percent_change_24h": best['quote']['USD']['percent_change_24h']})

        for worst in worst10:
            orderWorstCollection.append({"symbol": worst['symbol'], "percent_change_24h": worst['quote']['USD']['percent_change_24h']})

        self.report['best_10_percent_change_24h'] = {"best10": orderBestCollection, "worst10": orderWorstCollection}

    def howMuchForBest20Last24h(self, collection):
        i = 0
        cryptoCollection = []
        for item in collection:
            i += 1
            if i < 21:
                cryptoCollection.append({"symbol":item['symbol'], "price":item['quote']['USD']['price']})

        self.report['howMuchForBest20'] = cryptoCollection

    def howMuchTotalForBestVolumeLast24h(self, collection):
        total = 0
        for item in collection:
            if item['quote']['USD']['volume_24h'] > 76000000:
                total += item['quote']['USD']['volume_24h']

        self.report['howMuchTotalForBestVolumeLast24h'] = {"total":total}

    def percentageOfEarningsLast24h(self, collection):
        i = 0
        cryptoCollection = []
        for item in collection:
            i += 1
            if i < 21:
                gain = item['quote']['USD']['percent_change_1h'] - item['quote']['USD']['percent_change_24h']
                cryptoCollection.append({"symbol": item["symbol"],"earn": gain})
        self.report['percentageOfEarningsLast24h'] = cryptoCollection



    def printReport(self):
        now = datetime.now()
        with open(f"report-{now}.json", "w") as outfile:
            json.dump(self.report, outfile,indent=4)

