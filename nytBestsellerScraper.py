#first example

import requests
from bs4 import BeautifulSoup

#year is a number with 4 digits, month is any number from 1-12,
#   and day is any number from 1 to the number of days in the month indicated by the argument 'month'
def getBestsellerList(year, month, day):

    #fills in the url to get the nyt bestseller list for the date indicated by the arguments year, month, and day
    #we use zfill to get the month and day arguments to be two digits long (4 gets turned into 04, for example),
    #   since that's what the nyt link wants us to do
    url = f"https://www.nytimes.com/books/best-sellers/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}/"

    #standard boilerplate code we will use every time we do web scraping
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #bookTitles is a list of the html tags containing the book titles in each of the 11 lists on the website
    bookTitlesHtml = soup.find_all(class_ = 'css-i1z3c1')

    #categories is a list of the html tags containing the names of the 11 lists on the website
    categoriesHtml = soup.find_all(class_ = 'css-nzgijy')

    #here we use list comprehension to get the actual text of the book titles and names of categories
    #.title() capitalizes the first letter of every word. This makes the book titles look like titles
    bookTitles = [title.text.title() for title in bookTitlesHtml]
    categories = [category.text for category in categoriesHtml]

    #packages everything in a list of dictionaries. this is fairly arbitrary, but it's a nice structured form for the data
    bestsellers = [{"Category": category, "Top Five Books": bookTitles[5*index: 5*index+5]} for index, category in enumerate(categories)]

    return bestsellers

#example of how to call the function. This gets the categories and titles of the March 1, 2020 list
bestsellers = getBestsellerList(2020,3,1)
print(bestsellers)