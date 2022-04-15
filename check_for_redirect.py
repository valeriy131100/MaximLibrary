import requests


def check_for_redirect(response: requests.Response):
    if response.history:
        raise requests.HTTPError
