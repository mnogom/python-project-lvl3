"""Loader."""
import logging

import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time


def get_local_name(url: str) -> str:
    if url.endswith("/"):
        url = url[:-1]
    parsed_url = urlparse(url)
    filename = "{}{}{}".format(parsed_url.netloc,
                               parsed_url.path,
                               f"?{parsed_url.query}" if parsed_url.query else "")
    filename = re.sub("[!@#$%^*()`~/<>|\\\"'.,]", "-", filename)

    return f"{filename}"


def is_local_resource(item_url, page_url):
    page_url_parsed = urlparse(page_url)
    item_url_parsed = urlparse(item_url)

    return (item_url_parsed.netloc == page_url_parsed.netloc or  # noqa: W504, E501
                    not item_url_parsed.netloc) and item_url and \
                    not item_url.startswith("data:")


def download_local_resources(page_url: str,
                             page_html: str,
                             page_dir: str,
                             path: str):

    resources_types = {
        "img": "src",
        "script": "src",
        "link": "href"
    }

    soup = BeautifulSoup(page_html, features="html.parser")

    for tag, attr in resources_types.items():
        resource_items = soup.find_all(tag)
        for item in resource_items:

            item_url = item.get(attr)

            if is_local_resource(item_url, page_url):
                full_item_url = urljoin(page_url, item_url)

                _, ext = os.path.splitext(urlparse(full_item_url).path)
                ext_len = len(ext) if ext else 1

                local_name = get_local_name(full_item_url[:-ext_len]) + ext
                full_local_path = f"{path}/{page_dir}/{local_name}"
                rel_local_path = f"{page_dir}/{local_name}"

                response = requests.get(full_item_url)

                with open(full_local_path, "wb") as file:
                    file.write(response.content)
                    item[attr] = rel_local_path

    return soup.prettify()


def download(url: str, path: str) -> str:
    response = requests.get(url)

    page_name = f"{get_local_name(url)}.html"
    page_dir = f"{get_local_name(url)}_files"
    try:
        os.makedirs(f"{path}/{page_dir}")
    except FileExistsError:
        pass

    page_html = download_local_resources(url,
                                         response.text,
                                         page_dir,
                                         path)

    with open(f"{path}/{page_name}", "w") as file:
        file.write(page_html)

    return f"{path}/{page_name}"
