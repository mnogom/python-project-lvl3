"""Loader."""
import logging

import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import logging


logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)


def get_local_name(url: str, ext="") -> str:
    if url.endswith("/"):
        url = url[:-1]
    parsed_url = urlparse(url)
    filename = "{}{}{}".format(parsed_url.netloc,
                               parsed_url.path,
                               f"?{parsed_url.query}" if parsed_url.query else "")
    filename = re.sub("[!@#$%^*()`~/<>|\\\"'.,]", "-", filename)

    logging.info(f"Create name '{filename}{ext}' for url '{url}{ext}'")

    return filename + ext


def is_local_resource(item_url: str, page_url: str) -> bool:
    page_url_parsed = urlparse(page_url)
    item_url_parsed = urlparse(item_url)

    is_local = (item_url_parsed.netloc == page_url_parsed.netloc or  # noqa: W504, E501
                    not item_url_parsed.netloc) and item_url and \
                    not item_url.startswith("data:")

    logging.info(f"Item '{item_url}' is {'local' if is_local else 'not local'}")

    return is_local


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

                cut_item_url, ext = os.path.splitext(full_item_url)

                local_name = get_local_name(cut_item_url, ext)

                response = requests.get(full_item_url)
                with open(f"{path}/{page_dir}/{local_name}", "wb") as file:
                    file.write(response.content)
                    item[attr] = f"{page_dir}/{local_name}"

    return soup.prettify()


def download(url: str, path: str) -> str:
    response = requests.get(url)

    page_name = get_local_name(url, ".html")
    page_dir = get_local_name(url, "_files")
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
