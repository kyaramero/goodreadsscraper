import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.goodreads.com/shelf/show/lesbian?page='

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
    page_num = 1
    while True:
        page_url = url + str(page_num)
        cookies_dict = {"my_cookie": "cookie_value"}
        response = requests.get(page_url, cookies=cookies_dict)
        soup = BeautifulSoup(response.text, 'html.parser')

        data_found = False
        
        for d in soup.find_all('div', attrs={'class': 'elementList'}):
            info = d.find('div', attrs={'class': 'left'})
            if info is not None: 
                title = info.find('img', alt=True)
                titles.append(title.get('alt'))
                author = info.find('a', attrs={'class': 'authorName'})
                authors.append(author.find('span').text)
                smallText = info.find('span', attrs={'class': 'smallText'})
                rating = get_rating(smallText.text)
                year = get_year(smallText.text)
                ratings.append(rating)
                released.append(year)
                data_found = True
        
        if not data_found:
            break
        
        page_num += 1

get_data(url)
print(titles)
