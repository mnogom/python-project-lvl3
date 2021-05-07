"""Loader."""

import os
import re
from urllib.parse import urlparse, urljoin
import logging

from bs4 import BeautifulSoup
from progress.bar import PixelBar

from page_loader.file_manager import make_dir, save_file
from page_loader.request_manager import get_response


def _receive_name(url: str, isdir=False) -> str:
    """Convert url to local name.

    :param url: input url
    :param isdir: is name for directory
    """

    url_name, ext = os.path.splitext(url)

    # TODO: #1.1 some trouble when root url ends without "/"
    if url_name.endswith("/"):
        url_name = url_name[:-1]

    parsed_name_url = urlparse(url_name)
    filename = "{}{}{}".format(
        parsed_name_url.netloc,
        parsed_name_url.path,
        f"?{parsed_name_url.query}" if parsed_name_url.query else "")
    filename = re.sub(r"\W", "-", filename)

    if isdir:
        full_filename = filename + "_files"
        logging.info(f"Create name '{full_filename}' for  directory of "
                     f"references of '{url}'")

    else:
        if ext:
            full_filename = filename + ext
        else:
            full_filename = filename + ".html"
        logging.info(f"Create name '{full_filename}' for url '{url}'")

    return full_filename


def _is_local_assert(item_url: str, page_url: str) -> bool:
    """Check if assert is local.

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


def _download_assert(assert_url: str,
                     abs_ref_dir: str) -> str:
    """Download assert by url to dir.

    :param assert_url: url
    :param abs_ref_dir: absolute path
    """

    response = get_response(assert_url)

    local_name = _receive_name(assert_url)
    if not os.path.isdir(abs_ref_dir):
        make_dir(abs_ref_dir)
    full_path = os.path.join(abs_ref_dir, local_name)
    save_file(full_path, "wb", response.content)
    return local_name


def download(url: str, path: str) -> str:  # noqa: C901
    """Download page and all local asserts.

    :param url: requested url
    :param path: path to download
    :return: path to downloaded page
    """

    # TODO: #1.2 some trouble when root url ends without "/"
    full_url = url if url.endswith("/") else url + "/"
    response = get_response(url)
    page_name = _receive_name(full_url)
    page_dir = _receive_name(full_url, isdir=True)
    abs_dir = os.path.join(path, page_dir)

    logging.info("Starting analyzing page asserts")
    asserts_types = {
        "img": "src",
        "script": "src",
        "link": "href"
    }
    assert_urls = []

    soup = BeautifulSoup(response.text, features="html.parser")
    for tag, attr in asserts_types.items():

        assert_items = soup.find_all(tag)
        if not assert_items:
            break

        for item in assert_items:
            logging.info(f"Analyze '{attr}' in '{tag}'")

            item_url = item.get(attr)

            if _is_local_assert(item_url, url):
                full_item_url = urljoin(url, item_url)

                assert_urls.append(full_item_url)
                local_name = _receive_name(full_item_url)
                item[attr] = os.path.join(page_dir, local_name)
                logging.info(f"Switch assert reference "
                             f"'{item[attr]}'")
    page_text = soup.prettify(formatter="html5")
    logging.info("End of analyzing page asserts")

    if assert_urls:
        logging.info("Starting downloading asserts")
        bar_name = "Downloading asserts: "
        for url in PixelBar(bar_name).iter(assert_urls):
            _download_assert(url, abs_dir)

    return save_file(os.path.join(path, page_name), "w", page_text)
