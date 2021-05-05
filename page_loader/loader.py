"""Loader."""

import os
import re
from urllib.parse import urlparse, urljoin
import logging

from bs4 import BeautifulSoup
from bs4.element import Tag
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


def _is_local_resource(item_url: str, page_url: str) -> bool:
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


def _switch_resource_path(item: Tag,
                          attr: str,
                          page_dir: str,
                          local_name: str):
    """Switch resource from url to local path.

    :param item: item type
    :param attr: attribute to switch
    :param page_dir: absolute reference path
    :param local_name: relative reference path
    """

    item[attr] = os.path.join(page_dir, local_name)
    logging.info(f"Switch resource reference "
                 f"'{item[attr]}'")
    return


def parse_resources(page_url: str,
                    page_html: str,
                    abs_dir: str,
                    page_dir: str) -> str:
    """Find and download local resources.
    Switch references to downloaded files

    :param page_url: page url
    :param page_html: html page data
    :param abs_dir: absolute reference path
    :param page_dir: relative reference path
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
        if not resource_items:
            break

        bar_name = f"Searching '{attr}' in <{tag}>: "
        for item in PixelBar(bar_name).iter(resource_items):
            logging.info(f"Analyze '{attr}' in '{tag}'")

            item_url = item.get(attr)

            if _is_local_resource(item_url, page_url):
                full_item_url = urljoin(page_url, item_url)

                local_name = _download_resource(full_item_url, abs_dir)
                _switch_resource_path(item, attr, page_dir, local_name)

    logging.info("End of analyzing page resources")

    return soup.prettify(formatter="html5")


def _download_resource(resource_url: str,
                       abs_ref_dir: str) -> str:
    """Download resource by url to dir.

    :param resource_url: url
    :param abs_ref_dir: absolute path
    """
    response = get_response(resource_url)

    local_name = _receive_name(resource_url)
    if not os.path.isdir(abs_ref_dir):
        make_dir(abs_ref_dir)
    full_path = os.path.join(abs_ref_dir, local_name)
    save_file(full_path, "wb", response.content)
    return local_name


def download(url: str, path: str) -> str:
    """Download page and all local resources.

    :param url: requested url
    :param path: path to download
    :return: path to downloaded page
    """

    response = get_response(url)

    # TODO: #1.2 some trouble when root url ends without "/"
    full_url = url if url.endswith("/") else url + "/"
    page_name = _receive_name(full_url)
    page_dir = _receive_name(full_url, isdir=True)
    abs_dir = os.path.join(path, page_dir)
    page_text = parse_resources(url,
                                response.text,
                                abs_dir,
                                page_dir)

    return save_file(os.path.join(path, page_name), "w", page_text)
