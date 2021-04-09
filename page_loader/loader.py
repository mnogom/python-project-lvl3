"""Loader."""

import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def print_result(func):
    def inner(*args):
        print(f"input: {args}")
        result = func(*args)
        print(f"output: {result}")
        return result
    return inner


def get_local_name(url: str) -> str:

    parsed_url = urlparse(url)
    filename = "".join((parsed_url.netloc,
                        parsed_url.path,
                        parsed_url.query))
    filename = re.sub("[!@#$%^&*()`~=/<>|\\\".,]", "-", filename)

    return f"{filename}"


def download(url: str, path: str) -> str:

    response = requests.get(url)

    page_name = f"{get_local_name(url)}.html"
    page_dir = f"{get_local_name(url)}_files"
    try:
        os.makedirs(f"{path}/{page_dir}")
    except FileExistsError:
        pass

    page_soup = BeautifulSoup(response.text)

    with open(f"{path}/{page_name}", "w") as file:
        file.write(response.text)
    return f"{path}/{page_name}"
