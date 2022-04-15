import argparse
import json
import os
import urllib.parse

import requests
from bs4 import BeautifulSoup

import file_workers
from check_for_redirect import check_for_redirect
from parse_tululu_category import get_category_book_ids


def parse_book_page(book_page):
    soup = BeautifulSoup(book_page, 'lxml')

    book_header = soup.select_one('h1')
    title, author = book_header.text.split('::')

    image = soup.select_one('.bookimage img')

    comments = [
        comment.select_one('span').text
        for comment in soup.select('.texts')
    ]

    genres = [
        genre.text
        for genre in soup.select('.d_book a')
    ]

    return {
        'title': title.strip(),
        'author': author.strip(),
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

    book_path = file_workers.download_file(
        url=f'https://tululu.org/txt.php',
        filename=f'{book_id}. {title}.txt',
        folder=books_folder,
        as_text=True,
        request_params={'id': book_id}
    )

    image_url = parsed_book['image_url']
    full_image_url = urllib.parse.urljoin(
        'https://tululu.org', image_url
    )
    image_extension = file_workers.get_url_file_extension(image_url)

    image_path = file_workers.download_file(
        url=full_image_url,
        filename=f'{book_id}. {title}.{image_extension}',
        folder=images_folder
    )

    parsed_book.pop('image_url')

    return {
        'book_path': book_path,
        'image_path': image_path,
        **parsed_book
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--start_page', default=1, type=int)
    parser.add_argument('-e', '--end_page', default=None, type=int)
    parser.add_argument('-c', '--category', default=55, type=int)
    parser.add_argument('-i', '--images_folder', default='images/')
    parser.add_argument('-b', '--books_folder', default='books/')

    args = parser.parse_args()

    os.makedirs(args.images_folder, exist_ok=True)
    os.makedirs(args.books_folder, exist_ok=True)

    books = []

    category_book_ids = get_category_book_ids(
        args.category,
        args.start_page,
        args.end_page
    )

    for book_id in category_book_ids:
        try:
            book = download_book(
                book_id=book_id,
                images_folder=args.images_folder,
                books_folder=args.books_folder
            )
            books.append(book)
        except requests.HTTPError:
            continue

    with open('books.json', 'w', encoding='utf-8') as out:
        json.dump(books, out, ensure_ascii=False, indent=4)
