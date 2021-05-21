import requests
import json
from datetime import datetime
from pprint import pprint

#ticker is a string containing the symbol of the stock we're interested in
#period1 and period2 and integers containing the unix timestamps of the oldest 
#   and most recent stock prices we're interested in, respectively
def getStockPrices(ticker, period1, period2):
    '''we want the daily stock prices for a given stock over a certain period of time'''

    #creates empty list of seven lists that will contain the stock info we're scraping
    #each list corresponds to a different column in the table
    stockInfoList = [[],[],[],[],[],[],[]]

    #fills in the url to get the stock prices of the stock indicated by 'ticker' over the span of time
    #   stretching from the arguments 'period1' to 'period2'
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?formatted=true&includeAdjustedClose=true&interval=1d&period1={period1}&period2={period2}&useYfid=true&corsDomain=finance.yahoo.com"

    #this gets the html of the page at the above url. We're not using the standard boilerplate code here
    #because the page is in JSON format, so there's no need to use BeautifulSoup here. 
    page = requests.get(url)

    stockInfoDict = json.loads(page.content)["chart"]["result"][0] #turns JSON to dict

    #this turns the unix timestamps to dates which look like Apr 02, 2020
    stockInfoList[0] = [datetime.utcfromtimestamp(timeStamp).strftime('%b %d, %Y') for timeStamp in stockInfoDict["timestamp"]]
    
    #everythingButAdjustedClose is a dictionary containing all of the information we're looking for except for the adjusted close
    everythingButAdjustedClose = stockInfoDict["indicators"]["quote"][0]

    #stores all of the stock info we're looking for inside the everythingButAdjustedClose dictionary
    stockInfoList[1] = everythingButAdjustedClose["open"]
    stockInfoList[2] = everythingButAdjustedClose["high"]
    stockInfoList[3] = everythingButAdjustedClose["low"]
    stockInfoList[4] = everythingButAdjustedClose["close"]
    stockInfoList[6] = everythingButAdjustedClose["volume"]

    #stores the adjusted close info
    stockInfoList[5] = stockInfoDict["indicators"]["adjclose"][0]["adjclose"]

    #this reverses all of the lists so that the most recent stock information comes first 
    # (this isn't strictly necessary, but I want the format of this info to be the same as that in the other files)
    stockInfoList = [stockList[::-1] for stockList in stockInfoList]

    #packages everything in a dictionary
    stockInfoDict = dict(zip(["date", "open", "high", "low", "close", "adjusted close", "volume"], stockInfoList))
    return stockInfoDict

#example of how to call the function. This gets the daily stock prices of Apple, Inc from April 14th, 2020 to January 11th, 2021
stockInfoDict = getStockPrices('AAPL', 1586822400, 1610358400)
pprint(stockInfoDict)