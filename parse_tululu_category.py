from itertools import count
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from check_for_redirect import check_for_redirect


def parse_category_page(category_page):
    soup = BeautifulSoup(category_page, 'lxml')

    books = soup.select('.d_book')

    return [
        int(''.join(filter(
            str.isdigit,
            book.select_one('a').attrs['href']
        )))
        for book in books
    ]


def get_range(start, end):
    if start and end:
        return range(start, end)
    elif end:
        return range(1, end)
    elif start:
        return count(start)
    else:
        raise ValueError


def get_category_book_ids(category_id, start, end):
    ids = []
    base_url = f'https://tululu.org/l{category_id}/'

    for page in get_range(start, end):
        try:
            page_url = urljoin(base_url, f'{page}/')
            response = requests.get(page_url)
            response.raise_for_status()
            check_for_redirect(response)

            ids.extend(parse_category_page(response.text))
        except requests.HTTPError:
            break

    return ids
