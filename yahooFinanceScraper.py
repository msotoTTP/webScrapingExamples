import requests
from bs4 import BeautifulSoup
from pprint import pprint

#ticker is a string containing the symbol of the stock we're interested in
#period1 and period2 and integers containing the unix timestamps of the oldest 
#   and most recent stock prices we're interested in, respectively
def getStockPrices(ticker, period1, period2):
    '''we want the daily stock prices for a given stock over a certain period of time'''

    #fills in the url to get the stock prices of the stock indicated by 'ticker' over the span of time
    #   stretching from the arguments 'period1' to 'period2'
    url = f"https://finance.yahoo.com/quote/{ticker}/history?period1={period1}&period2={period2}&interval=1d"

    #standard boilerplate code we will use every time we do web scraping
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #creates empty list of seven lists that will contain the stock info we're scraping
    #each list corresponds to a different column in the table
    stockInfoList = [[],[],[],[],[],[],[]]

    #the whole table is inside a 'tbody' tag, and each row is in a 'tr' tag
    rows = soup.tbody.find_all('tr')
    for row in rows:

        #each element in the row is in a 'td' tag
        cols = row.find_all('td')

        #this only stores the info contained in rows with 7 columns
        #rows that don't have 7 columns don't have the stock information we're looking for
        [stockInfoList[i].append(col.span.text) for i, col in enumerate(cols) if len(cols) == 7]

    #packages everything in a dictionary
    stockInfoDict = dict(zip(["date", "open", "high", "low", "close", "adjusted close", "volume"], stockInfoList))
    return stockInfoDict

#example of how to call the function. This gets the daily stock prices of Apple, Inc from April 14th, 2020 to January 11th, 2021
stockInfoDict = getStockPrices('AAPL', 1586822400, 1610358400)
pprint(stockInfoDict)
