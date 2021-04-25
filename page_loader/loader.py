"""Loader."""

import os
import re
from urllib.parse import urlparse, urljoin
import logging

from bs4 import BeautifulSoup

from page_loader.file_manager import create_directory, save_file
from page_loader.request_manager import get_response


logging.basicConfig(level=logging.INFO,
                    format=("%(asctime)s - "
                            "[%(levelname)s] -  "
                            "%(name)s - "
                            "(%(filename)s)."
                            "%(funcName)s"
                            "(%(lineno)d) - %(message)s"))


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

    if not item_url:
        logging.info("Item hasn't references in attribute")
        return False
    if item_url.startswith("data:"):
        logging.info("Type of item reference is 'Data URL'")
        return False
    if not item_url_parsed.netloc or \
            item_url_parsed.netloc == page_url_parsed.netloc:
        logging.info(f"Item reference '{item_url}' is local")
        return True
    logging.info(f"Item reference '{item_url}' is not local")
    return False


def download_local_resources(page_url: str,
                             page_html: str,
                             ref_dir: str):

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
                save_file(f"{ref_dir}/{local_name}", "wb", response.content)

                item[attr] = f"{ref_dir}/{local_name}"
                logging.info(f"Switch resource reference "
                             f"from '{item_url}' to '{item[attr]}'")

    logging.info("End of analyzing page resources")

    return soup.prettify()


def download(url: str, path: str) -> str:
    response = get_response(url)

    page_name = get_local_name(url, ".html")
    reference_dir = create_directory(path, get_local_name(url, "_files"))

    page_text = download_local_resources(url,
                                         response.text,
                                         reference_dir)

    return save_file(f"{path}{page_name}", "w", page_text)
