from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

session = HTMLSession()
session.cookies.set("COOKIE_NAME", "the cookie works", domain="https://www.goodreads.com/")

url = 'https://www.goodreads.com/shelf/show/'

genre = input('Type the genre you want to search (you can find the name on goodreads): ')

# Get Rating
def get_rating(input_text):
    match = re.search(r'avg rating (\d+\.\d+)', input_text)
    if match:
        avg_rating = float(match.group(1))
        return avg_rating
    
# Get Release Year
def get_year(input_text):
    match_published = re.search(r'published (\d{4})', input_text)
    if match_published:
        year_published = int(match_published.group(1))
        return year_published
    
# Variables    
titles = []
authors = []
ratings = []
released = []

def get_data(url):
    r = session.get(url + genre)
    r.cookies
    soup = BeautifulSoup(r.text, 'html.parser')
    for d in soup.find_all('div', attrs={'class': 'elementList'}):
        info = d.find('div', attrs={'class', 'left'})
        if (info is not None):
            title = info.find('img', alt=True)
            titles.append(title.get('alt'))
            author = info.find('a', attrs={'class', 'authorName'})
            authors.append(author.find('span').text)
            smallText = info.find('span', attrs={'class', 'smallText'})
            rating = get_rating(smallText.text)
            year = get_year(smallText.text)
            ratings.append(rating)
            released.append(year)

    return

get_data(url)

released = np.array(released)

df = pd.DataFrame({'Titulo': titles, 'Autor': authors, 'Nota': ratings, 'Ano de lancamento': released})

# By rating
df = df.sort_values(by=['Nota'], ascending=False)

df.to_csv('50LivrosGoodreads.csv')