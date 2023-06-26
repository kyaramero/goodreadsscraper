import requests
from bs4 import BeautifulSoup
import re



url = 'https://www.goodreads.com/shelf/show/lesbian?page=2'

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
pages = []

# def num_pages(url):
#     num = 25 # After that, pages aren't working, loading
#     for i in range (1, num + 1):
#         page = url + str(i)
#         pages.append(page)
num = 25

def get_data(url):
    # for i in range (1, num + 1):
    r = requests.get(url)
    print(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for d in soup.find_all('div', attrs={'class': 'elementList'}):
        info = d.find('div', attrs={'class': 'left'})
        if (info is not None): 
            title = info.find('img', alt=True)
            print(title)
            titles.append(title.get('alt'))
            author = info.find('a', attrs={'class': 'authorName'})
            authors.append(author.find('span').text)
            smallText = info.find('span', attrs={'class': 'smallText'})
            rating = get_rating(smallText.text)
            year = get_year(smallText.text)
            ratings.append(rating)
            released.append(year)
        # print(titles)
    return

get_data(url)


# def main():
#     num_pages(url)
#     for page in pages:
#         get_data(page)
#     # return titles

# print(main())
# num_pages(url)
# print(pages)
