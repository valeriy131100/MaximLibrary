import os
import urllib.parse

import requests
from pathvalidate import sanitize_filename

from check_for_redirect import check_for_redirect


def get_url_file_extension(url):
    parsed_url = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed_url.path)
    extension = os.path.splitext(path)[1]
    return extension


def download_file(url, filename, folder, as_text=False, request_params=None):
    response = requests.get(url, params=request_params)
    response.raise_for_status()
    check_for_redirect(response)

    filepath = os.path.join(folder, sanitize_filename(filename))

    if as_text:
        with open(filepath, 'w') as file:
            file.write(response.text)
    else:
        with open(filepath, 'wb') as file:
            file.write(response.content)

    return filepath
