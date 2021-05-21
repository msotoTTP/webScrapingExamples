import requests
from bs4 import BeautifulSoup
import ciso8601
import time
from pprint import pprint

#date is a string with a date that looks like Apr 02, 2020
#this function takes a date and turns it into a unix timestamp
def dateToUnixTime(date):

    #format the date so that it can be put into the parse_datetime method of ciso8601
    date = date.replace(',','') #get rid of commas
    month, day, year = date.split()
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    month = months[month] #this turns the three letter abbreviation for the month to a two digit number
    properlyFormattedDate = year + month + day

    #use the ciso8601 library to turn the date to a unix timestamp
    timeStamp = ciso8601.parse_datetime(properlyFormattedDate) 
    # to get time in seconds:
    return int( time.mktime( timeStamp.timetuple() ) )


#ticker is a string containing the symbol of the stock we're interested in
#period1 and period2 and integers containing the unix timestamps of the oldest 
#   and most recent stock prices we're interested in, respectively
def getStockPrices(ticker, period1, period2):
    '''we want the daily stock prices for a given stock over a certain period of time'''

    #creates empty list of seven lists that will contain the stock info we're scraping
    #each list corresponds to a different column in the table
    stockInfoList = [[],[],[],[],[],[],[]]

    #as long as we're looking for more than three days of stock prices, keep making requests (the number of seconds in a day is 86,400)
    while (period2 - period1 > 86400*3):

        #fills in the url to get the stock prices of the stock indicated by 'ticker' over the span of time
        #   stretching from the arguments 'period1' to 'period2'
        url = f"https://finance.yahoo.com/quote/{ticker}/history?period1={period1}&period2={period2}&interval=1d"

        #standard boilerplate code we will use every time we do web scraping
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        #the whole table is inside a 'tbody' tag, and each row is in a 'tr' tag
        rows = soup.find('tbody').find_all('tr')
        for row in rows:

            #each element in the row is in a 'td' tag
            cols = row.find_all('td')

            #this only stores the info contained in rows with 7 columns
            #rows that don't have 7 columns don't have the stock information we're looking for
            [stockInfoList[i].append(cols[i].span.text) for i in range(7) if len(cols) == 7]

        #this gets the date of the oldest stock prices obtained in the last request
        oldestDate = stockInfoList[0][-1]
        #converts the date above to a unix timestamp
        period2 = dateToUnixTime(oldestDate)

    #packages everything in a dictionary
    stockInfoDict = dict(zip(["date", "open", "high", "low", "close", "adjusted close", "volume"], stockInfoList))
    return stockInfoDict

#example of how to call the function. This gets the daily stock prices of Apple, Inc from April 14th, 2020 to January 11th, 2021
stockInfoDict = getStockPrices('AAPL', 1586822400, 1610358400)
pprint(stockInfoDict)