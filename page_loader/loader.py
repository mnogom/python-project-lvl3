"""Loader."""

import os
import re
from urllib.parse import urlparse, urljoin
import logging

from bs4 import BeautifulSoup

from page_loader.file_manager import create_directory, save_file
from page_loader.request_manager import get_response


def get_local_name(url: str, ext="") -> str:
    """Convert url to local name.

    :param url: input url
    :param ext: extension (ending of filename)
    """

    if url.endswith("/"):
        url = url[:-1]
    if not ext:
        ext = ".html"

    parsed_url = urlparse(url)
    filename = "{}{}{}".format(
        parsed_url.netloc,
        parsed_url.path,
        f"?{parsed_url.query}" if parsed_url.query else "")
    filename = re.sub("[!@#$%^*()`~/<>|\\\"'.,]", "-", filename)

    logging.info(f"Create name '{filename}{ext}' for url '{url}{ext}'")

    return filename + ext


def is_local_resource(item_url: str, page_url: str) -> bool:
    """Check if resource is local.

    :param item_url: reference url
    :param page_url: page url
    :return: True/False
    """

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
                             abs_ref_dir: str,
                             rel_ref_dir: str) -> str:
    """Find and download local resources.
    Switch references to downloaded files

    :param page_url: page url
    :param page_html: html page data
    :param abs_ref_dir: absolute reference path
    :param rel_ref_dir: relative reference path
    :return: updated html page data
    """

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
                save_file(f"{abs_ref_dir}{local_name}", "wb", response.content)

                item[attr] = f"{rel_ref_dir}{local_name}"
                logging.info(f"Switch resource reference "
                             f"from '{item_url}' to '{item[attr]}'")

    logging.info("End of analyzing page resources")

    return soup.prettify(formatter="html5")


def download(url: str, path: str) -> str:
    """Download page and all local resources.

    :param url: requested url
    :param path: path to download
    :return: path to downloaded page
    """

    if not path.endswith("/"):
        path += "/"
    response = get_response(url)

    page_name = get_local_name(url, ".html")
    rel_ref_dir = get_local_name(url, '_files/')
    abs_ref_dir = create_directory(f"{path}{rel_ref_dir}")

    page_text = download_local_resources(url,
                                         response.text,
                                         abs_ref_dir,
                                         rel_ref_dir)

    return save_file(f"{path}{page_name}", "w", page_text)
