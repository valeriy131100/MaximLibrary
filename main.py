import os

import requests


def check_for_redirect(response: requests.Response):
    if not response.history:
        return

    raise requests.HTTPError


def download_books(count, folder_path):
    book_url = 'http://tululu.org/txt.php?id={book_id}'

    for book_id in range(1, count + 1):
        try:
            response = requests.get(
                book_url.format(book_id=book_id)
            )
            response.raise_for_status()
            check_for_redirect(response)
        except requests.HTTPError:
            continue

        book_filename = f'{book_id}.txt'
        book_filepath = os.path.join(folder_path, book_filename)
        with open(book_filepath, 'wb') as file:
            file.write(response.content)


os.makedirs('books', exist_ok=True)
download_books(10, 'books')
