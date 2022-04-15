from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_category_page(category_page):
    soup = BeautifulSoup(category_page, 'lxml')

    books = soup.find_all('table', {'class': 'd_book'})

    return [
        urljoin('https://tululu.org', book.find('a').attrs['href'])
        for book in books
    ]


if __name__ == '__main__':
    print(parse_category_page(
        requests.get(
            'https://tululu.org/l55/'
        ).text
    ))
