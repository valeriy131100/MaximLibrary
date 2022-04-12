import argparse
import os
import urllib.parse

import requests
from bs4 import BeautifulSoup

import file_workers


def check_for_redirect(response: requests.Response):
    if not response.history:
        return

    raise requests.HTTPError


def parse_book_page(book_page):
    soup = BeautifulSoup(book_page, 'lxml')

    book_header = soup.find('h1')
    title, _ = book_header.text.split('::')

    image = soup.find('div', {'class': 'bookimage'}).find('img')

    comments = [
        comment.find('span').text
        for comment in soup.find_all('div', {'class': 'texts'})
    ]

    genres = [
        genre.text
        for genre in soup.find('span', {'class': 'd_book'}).find_all('a')
    ]

    return {
        'title': title.strip(),
        'image_url': image.attrs['src'],
        'comments': comments,
        'genres': genres
    }


def download_book(book_id, books_folder='books/', images_folder='images/'):
    response = requests.get(
        f'https://tululu.org/b{book_id}/'
    )
    response.raise_for_status()

    check_for_redirect(response)

    parsed_book = parse_book_page(response.text)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_id', default=1, type=int)
    parser.add_argument('-e', '--end_id', default=10, type=int)

    args = parser.parse_args()

    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            download_book(book_id=book_id)
        except requests.HTTPError:
            continue
