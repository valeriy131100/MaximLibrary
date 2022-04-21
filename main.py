import argparse
import json
import os
import urllib.parse
from pathlib import Path

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
        for genre in soup.select('span.d_book a')
    ]

    return {
        'title': title.strip(),
        'author': author.strip(),
        'image_url': image.attrs['src'],
        'comments': comments,
        'genres': genres
    }


def download_book(book_id,
                  txts_folder='books/',
                  skip_txts=False,
                  images_folder='images/',
                  skip_images=False):
    response = requests.get(
        f'https://tululu.org/b{book_id}/'
    )
    response.raise_for_status()

    check_for_redirect(response)

    parsed_book = parse_book_page(response.text)

    title = parsed_book['title']

    if not skip_txts:
        txt_path = file_workers.download_file(
            url=f'https://tululu.org/txt.php',
            filename=f'{book_id}. {title}.txt',
            folder=txts_folder,
            as_text=True,
            request_params={'id': book_id}
        )

        parsed_book['book_path'] = txt_path

    image_url = parsed_book.pop('image_url')

    if not skip_images:
        full_image_url = urllib.parse.urljoin(
            'https://tululu.org', image_url
        )
        image_extension = file_workers.get_url_file_extension(image_url)

        image_path = file_workers.download_file(
            url=full_image_url,
            filename=f'{book_id}. {title}.{image_extension}',
            folder=images_folder
        )

        parsed_book['image_path'] = image_path

    return parsed_book


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--start_page', default=1, type=int)
    parser.add_argument('-e', '--end_page', default=None, type=int)
    parser.add_argument('-c', '--category', default=55, type=int)
    parser.add_argument('-f', '--dest_folder', default='books/')
    parser.add_argument('-j', '--json_path', default='books.json')
    parser.add_argument('-i', '--skip_images', action='store_true')
    parser.add_argument('-t', '--skip_txts', action='store_true')

    args = parser.parse_args()

    base_folder = args.dest_folder

    os.makedirs(base_folder, exist_ok=True)

    images_folder = os.path.join(base_folder, 'images/')
    txts_folder = os.path.join(base_folder, 'txts/')
    json_path = Path(os.path.join(base_folder, args.json_path))

    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(txts_folder, exist_ok=True)
    json_path.parent.mkdir(exist_ok=True, parents=True)

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
                images_folder=images_folder,
                skip_images=args.skip_images,
                txts_folder=txts_folder,
                skip_txts=args.skip_txts
            )
            books.append(book)
        except requests.HTTPError:
            continue

    with open(json_path, 'w', encoding='utf-8') as out:
        json.dump(books, out, ensure_ascii=False, indent=4)
