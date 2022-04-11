import os
import urllib.parse

import requests
from bs4 import BeautifulSoup

import file_workers


def check_for_redirect(response: requests.Response):
    if not response.history:
        return

    raise requests.HTTPError


def parse_book(book_id):
    response = requests.get(
        f'https://tululu.org/b{book_id}/'
    )
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    book_header = soup.find('h1')
    title, _ = book_header.text.split('::')

    image = soup.find('div', {'class': 'bookimage'}).find('img')

    comments_divs = soup.find_all('div', {'class': 'texts'})

    comments = [comment_div.find('span').text for comment_div in comments_divs]

    return {
        'title': title.strip(),
        'image_url': image.attrs['src'],
        'comments': comments
    }


def download_books(count, books_folder='books/', images_folder='images/'):
    for book_id in range(1, count + 1):
        try:
            parsed_book = parse_book(book_id)

            title = parsed_book['title']

            file_workers.download_file(
                url=f'https://tululu.org/txt.php?id={book_id}',
                filename=f'{book_id}. {title}.txt',
                folder=books_folder,
            )

            image_url = parsed_book['image_url']
            full_image_url = urllib.parse.urljoin(
                'https://tululu.org', image_url
            )
            image_extension = file_workers.get_url_file_extension(image_url)

            file_workers.download_file(
                url=full_image_url,
                filename=f'{book_id}. {title}.{image_extension}',
                folder=images_folder
            )

        except requests.HTTPError:
            continue


if __name__ == '__main__':
    print(parse_book(9))
