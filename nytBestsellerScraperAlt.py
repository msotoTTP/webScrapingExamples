#second example

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

    #creates empty list that will hold the book info we're scraping
    bestsellers = []

    #categories is a list of the ol tags on the page. The ol tags contain the list of five books in the category and
    #   are right next to the tags containing the category name
    categories = soup.find_all('ol')
    for category in categories:
        #categoryName contains the name of the current category
        categoryName = category.previous_sibling.a.text

        #all of the books are enclosed in li tags. We set recursive=False because we only want to consider the ol tag's
        #   direct children
        htmlEnclosingBooks = category.find_all('li', recursive=False)

        #creates empty list that will hold the list of book titles for the current category
        books = []
        for bookHtml in htmlEnclosingBooks:
            #this extracts the title of the current book and adds it to the list
            books.append( bookHtml.a.find('div', recursive=False).h3.text.title() )

        #packages everything in a list of dictionaries. this is fairly arbitrary, but it's a nice structured form for the data
        bestsellers.append({"Category": categoryName, "Top Five Books": books})

    #all of the code after the standard boilerplate can be replaced with the following line!
    #bestsellers = [{"Category": category.previous_sibling.a.text, "Top Five Books": [book.a.find('div', recursive=False).h3.text.title() for book in category.find_all('li', recursive=False)]} for category in soup.find_all('ol')]
    #comment out or delete the code on lines 19-40 and uncomment the above line to see it in action

    return bestsellers

#example of how to call the function. This gets the categories and titles of the March 1, 2020 list
bestsellers = getBestsellerList(2020,3,1)
print(bestsellers)