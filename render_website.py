import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open('books/books.json', encoding='utf-8') as books_file:
        books = json.load(books_file)

    rendered_page = template.render(
        books=books
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)
