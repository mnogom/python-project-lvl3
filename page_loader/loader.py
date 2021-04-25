"""Loader."""
import sys

import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import logging


# logging.basicConfig(filename='example.log',
#                     encoding='utf-8',
#                     level=logging.INFO)
logging.basicConfig(level=logging.INFO,
                    format=("%(asctime)s - "
                            "[%(levelname)s] -  "
                            "%(name)s - "
                            "(%(filename)s)."
                            "%(funcName)s"
                            "(%(lineno)d) - %(message)s"))


def get_response(url: str):
    response = requests.get(url)

    if response.status_code // 100 == 2:
        logging.info(f"Response status code is {response.status_code}")
        return response

    if response.status_code // 100 == 3:
        logging.info(f"Your request was "
                     f"redirected with code "
                     f"{response.status_code}")
        return response

    if response.status_code // 100 == 4:
        logging.warning(f"Bad request. Got error "
                        f"{response.status_code}: "
                        f"{response.reason}")
        sys.exit()

    if response.status_code // 100 == 5:
        logging.warning(f"Bad answer. Got error "
                        f"{response.status_code}: "
                        f"{response.reason}")
        sys.exit()


def get_local_name(url: str, ext="") -> str:
    if url.endswith("/"):
        url = url[:-1]
    parsed_url = urlparse(url)
    filename = "{}{}{}".format(
        parsed_url.netloc,
        parsed_url.path,
        f"?{parsed_url.query}" if parsed_url.query else "")
    filename = re.sub("[!@#$%^*()`~/<>|\\\"'.,]", "-", filename)

    logging.info(f"Create name '{filename}{ext}' for url '{url}{ext}'")

    return filename + ext


def is_local_resource(item_url: str, page_url: str) -> bool:
    page_url_parsed = urlparse(page_url)
    item_url_parsed = urlparse(item_url)

    is_local = (item_url_parsed.netloc == page_url_parsed.netloc or  # noqa: W504, E501
                not item_url_parsed.netloc) and \
        item_url and \
        not item_url.startswith("data:")

    if not item_url:
        logging.info("Item hasn't reference in attribute.")
    else:
        logging.info(f"Item '{item_url}' is "
                     f"{'local' if is_local else 'not local'}")

    return is_local


def download_local_resources(page_url: str,
                             page_html: str,
                             page_dir: str,
                             path: str):

    logging.info("Starting analyzing page resources")

    resources_types = {
        "img": "src",
        "script": "src",
        "link": "href"
    }

    soup = BeautifulSoup(page_html, features="html.parser")

    for tag, attr in resources_types.items():
        resource_items = soup.find_all(tag)
        for item in resource_items:

            logging.info(f"Analyze '{attr}' in '{tag}'")

            item_url = item.get(attr)

            if is_local_resource(item_url, page_url):
                full_item_url = urljoin(page_url, item_url)

                cut_item_url, ext = os.path.splitext(full_item_url)

                local_name = get_local_name(cut_item_url, ext)

                response = get_response(full_item_url)
                with open(f"{path}{page_dir}/{local_name}", "wb") as file:
                    file.write(response.content)
                    logging.info(f"{local_name} was saved to {path}{page_dir}")

                item[attr] = f"{page_dir}/{local_name}"
                logging.info(f"Switch resource reference "
                             f"from '{item_url}' to '{item[attr]}'")

    logging.info("End of analyzing page resources")

    return soup.prettify()


def download(url: str, path: str) -> str:
    response = get_response(url)

    page_name = get_local_name(url, ".html")
    page_dir = get_local_name(url, "_files")
    try:
        logging.info(f"Creating directories '{path}{page_dir}'")
        os.makedirs(f"{path}/{page_dir}")
    except FileExistsError:
        logging.info(f"Directories '{path}{page_dir}' is already exists")

    page_html = download_local_resources(url,
                                         response.text,
                                         page_dir,
                                         path)

    with open(f"{path}/{page_name}", "w") as file:
        file.write(page_html)
        logging.info(f"'{page_name}' was saved to {path}")

    return f"{path}/{page_name}"
