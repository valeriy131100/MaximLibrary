from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from check_for_redirect import check_for_redirect


def parse_category_page(category_page):
    soup = BeautifulSoup(category_page, 'lxml')

    books = soup.find_all('table', {'class': 'd_book'})

    return [
        int(''.join(filter(str.isdigit, book.find('a').attrs['href'])))
        for book in books
    ]


def get_category_book_ids(category_id, start, end):
    ids = []
    base_url = f'https://tululu.org/l{category_id}/'

    for page in range(start, end):
        category_url = urljoin(base_url, f'{page}/')
        response = requests.get(category_url)
        response.raise_for_status()
        check_for_redirect(response)

        ids.extend(parse_category_page(response.text))

    return ids


if __name__ == '__main__':
    print(get_category_book_ids(55, 1, 11))