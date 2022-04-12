# MaximLibrary

Скрипт для скачивания книг и иллюстраций с сайта [Tululu.org](https://https://tululu.org/).

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

### Запуск
Находясь в директории MaximLibrary исполните:
```bash
$ venv/bin/python telegram_bot.py
```

### Опциональные аргументы
* `-s`, `--start_id` и `-e`, `--end_id` - промежуток id книг для загрузки. По умолчанию - `1` и `10`.
* `-b`, `--books_folder` - путь до папки куда будут загружены книги. По умолчанию - `books/`.
* `-i`, `--images_folder` - путь до папки куда будут загружены изображения. По умолчанию - `images/`.
