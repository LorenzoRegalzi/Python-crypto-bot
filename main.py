from Bot import Bot
import time
myBot = Bot();

while(1):
    cryptoData = myBot.fetchCurrencyData()

    myBot.maxVolumeLast24h(cryptoData)
    myBot.bestCryptoLast24h(cryptoData)
    myBot.howMuchForBest20Last24h(cryptoData)
    myBot.howMuchTotalForBestVolumeLast24h(cryptoData)
    myBot.percentageOfEarningsLast24h(cryptoData)

    myBot.printReport()

    # routine
    minutes = 60 * 24
    seconds = minutes * 60
    time.sleep(seconds)










