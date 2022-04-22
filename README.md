# MaximLibrary

Скрипт для скачивания книг и иллюстраций с сайта [Tululu.org](https://https://tululu.org/), а также генерации сайта-библиотеки на его основе.

Пример сайта - [Репозиторий](https://github.com/valeriy131100/MaximLibraryWebsiteExample), [Сайт](https://valeriy131100.github.io/MaximLibraryWebsiteExample/pages/index1.html).

## Установка
Вам понадобится установленный Python 3.6+ и git.

Склонируйте репозиторий:
```bash
$ git clone https://github.com/valeriy131100/MaximLibrary
```

Создайте в этой папке виртуальное окружение:
```bash
$ cd MaximLibrary
$ python3 -m venv venv
```

Активируйте виртуальное окружение и установите зависимости:
```bash
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Использование

### Скачивание книг
Находясь в директории MaximLibrary исполните:
```bash
$ venv/bin/python download_books.py
```

#### Опциональные аргументы
* `-s`, `--start_page` и `-e`, `--end_page` - промежуток страниц категории книг для загрузки. По умолчанию - `1` и `None`. Если конец промежутка не задан, то будут скачаны книги до последней страницы.
* `-c`, `--category` - код категории на [Tululu.org](https://https://tululu.org/). Для этого необходимо перейти на страницу жанра и скопировать код после буквы l - `https://tululu.org/l{код будет здесь}/`. По умолчанию - 55 (Научная фантастика).
* `-f`, `--dest_folder` - путь до базовой папки загрузки. Относительно нее будут рассчитаны прочие пути. По умолчанию - `books/`.
* `-j`, `--json_path` - путь по которому будет сохранен json-файл с информацией о книгах.
* `-i`, `--skip_images` - если передан, то изображения не будут загружены.
* `-t`, `--skip_txts` - если передан, то txt книг не будут загружены.

### Генерация и запуск веб-сайта
Предварительно загрузите книги используя стандартные настройки для пути к json-файлу и базовой папке загрузки.

Затем находясь в директории MaximLibrary исполните:
```bash
$ venv/bin/python render_website.py
```

Сайт можно будет посмотреть по адресу [127.0.0.1/pages/index1.html](http://127.0.0.1/pages/index1.html).
Сгенерированные странички будут находиться в папке pages.
