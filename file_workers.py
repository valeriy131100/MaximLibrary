import os
import urllib.parse

import requests
from pathvalidate import sanitize_filename

from main import check_for_redirect


def get_url_file_extension(url):
    parsed_url = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed_url.path)
    extension = os.path.splitext(path)[1]
    return extension


def download_file(url, filename, folder):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    filepath = os.path.join(folder, sanitize_filename(filename))

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath
