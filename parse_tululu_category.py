from itertools import count
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from check_for_redirect import check_for_redirect


def parse_category_page(category_page):
    soup = BeautifulSoup(category_page, 'lxml')

    books = soup.select('.d_book')

    ids = [
        ''.join(filter(
            str.isdigit,
            book.select_one('a').attrs['href']
        ))
        for book in books
    ]

    last_page = int(soup.select('.npage')[-1].text)
    selected_page = int(soup.select_one('.npage_select').text)

    return {
        'ids': ids,
        'last_page': max(last_page, selected_page)
    }


def get_category_book_ids(category_id, start, end):
    ids = []
    base_url = f'https://tululu.org/l{category_id}/'

    for page in count(start=start):
        try:
            page_url = urljoin(base_url, f'{page}/')
            response = requests.get(page_url)
            response.raise_for_status()
            check_for_redirect(response)

            parsed_page = parse_category_page(response.text)
            ids.extend(parsed_page['ids'])

            if (end and page == end) or (page == parsed_page['last_page']):
                break

        except requests.HTTPError:
            break

    return ids
