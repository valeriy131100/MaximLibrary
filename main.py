import os
import urllib.parse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response: requests.Response):
    if not response.history:
        return

    raise requests.HTTPError


def get_url_file_extension(url):
    parsed_url = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed_url.path)
    extension = os.path.splitext(path)[1]
    return extension


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

    return {
        'title': title.strip(),
        'image_url': image.attrs['src']
    }


def download_file(url, filename, folder):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    filepath = os.path.join(folder, sanitize_filename(filename))

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def download_books(count, books_folder='books/', images_folder='images/'):
    for book_id in range(1, count + 1):
        try:
            parsed_book = parse_book(book_id)

            title = parsed_book['title']

            download_file(
                url=f'https://tululu.org/txt.php?id={book_id}',
                filename=f'{book_id}. {title}.txt',
                folder=books_folder,
            )

            image_url = parsed_book['image_url']
            full_image_url = urllib.parse.urljoin(
                'https://tululu.org', image_url
            )

            download_file(
                url=full_image_url,
                filename=os.path.basename(image_url),
                folder=images_folder,
            )

        except requests.HTTPError:
            continue


if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    download_books(10)
