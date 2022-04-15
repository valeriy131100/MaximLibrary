from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from check_for_redirect import check_for_redirect


def parse_category_page(category_page):
    soup = BeautifulSoup(category_page, 'lxml')

    books = soup.find_all('table', {'class': 'd_book'})

    return [
        urljoin('https://tululu.org', book.find('a').attrs['href'])
        for book in books
    ]


def get_category_book_links(category_id, start, end):
    links = []
    base_url = f'https://tululu.org/l{category_id}/'

    for page in range(start, end):
        category_url = urljoin(base_url, f'{page}/')
        response = requests.get(category_url)
        response.raise_for_status()
        check_for_redirect(response)

        links.extend(parse_category_page(response.text))

    return links


if __name__ == '__main__':
    print(get_category_book_links(55, 1, 11))
