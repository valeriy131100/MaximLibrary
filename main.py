import os

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response: requests.Response):
    if not response.history:
        return

    raise requests.HTTPError


def get_book_title(book_id):
    response = requests.get(
        f'http://tululu.org/b{book_id}/'
    )
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')
    book_header = soup.find('h1')
    title, _ = book_header.text.split('::')
    return title.strip()


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    book_filepath = os.path.join(folder, sanitize_filename(filename))

    with open(book_filepath, 'wb') as file:
        file.write(response.content)


def download_books(count, folder='books/'):
    for book_id in range(1, count + 1):
        try:
            title = get_book_title(book_id)
            download_txt(
                url=f'http://tululu.org/txt.php?id={book_id}',
                filename=f'{book_id}. {title}.txt',
                folder=folder,
            )
        except requests.HTTPError:
            continue


os.makedirs('books', exist_ok=True)
download_books(10)