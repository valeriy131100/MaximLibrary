import json
import math
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


BOOKS_PER_PAGE = 10


def reload_website():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open('books/books.json', encoding='utf-8') as books_file:
        books = json.load(books_file)

    pages_count = math.ceil(len(books) / BOOKS_PER_PAGE)

    chunked_books = chunked(books, BOOKS_PER_PAGE)
    for page_num, page_books in enumerate(chunked_books, start=1):
        rendered_page = template.render(
            books=chunked(page_books, 2),
            current_page=page_num,
            pages_count=pages_count
        )

        page_path = f'pages/index{page_num}.html'

        with open(page_path, 'w', encoding='utf8') as file:
            file.write(rendered_page)


if __name__ == '__main__':
    os.makedirs('pages', exist_ok=True)
    reload_website()

    server = Server()
    server.watch('template.html', reload_website)
    server.serve(root='.')
