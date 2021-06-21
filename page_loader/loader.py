"""Loader."""

import os
import re
from urllib.parse import urlparse, urljoin
import logging

from bs4 import BeautifulSoup
from progress.bar import PixelBar

from page_loader.file_manager import make_dir, save_file
from page_loader.request_manager import get_response


def _generate_name(url: str, isdir=False) -> str:
    """Convert url to local name.

    :param url: input url
    :param isdir: is name for directory
    :return: local name for url
    """

    url_name, ext = os.path.splitext(url)

    # TODO: #1.1 some trouble when root url ends with "/"
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
        return full_filename

    if ext:
        full_filename = filename + ext
    else:
        full_filename = filename + ".html"
        logging.info(f"Create name '{full_filename}' for url '{url}'")

    return full_filename


def _is_local_asset(item_url: str, page_url: str) -> bool:
    """Check if asset is local.

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
    if (not item_url_parsed.netloc
            or item_url_parsed.netloc == page_url_parsed.netloc):  # noqa: W503
        logging.info(f"Item reference '{item_url}' is local")
        return True
    logging.info(f"Item reference '{item_url}' is not local")
    return False


def _switch_assets(soup,
                   page_url: str,
                   asset_rel_dir: str,
                   asset_abs_dir: str) -> list:
    """Find and switch all local assets

    :param soup: soup data
    :param page_url: main url
    :param asset_rel_dir: directory for page assets
    :return: assets urls with local paths
    """

    logging.info("Starting analyzing page assets")

    assets_types = {
        "img": "src",
        "script": "src",
        "link": "href"
    }
    assets_map = []

    for tag, attr in assets_types.items():

        asset_items = soup.find_all(tag)
        if asset_items:
            for item in asset_items:
                logging.info(f"Analyze '{attr}' in '{tag}'")

                item_url = item.get(attr)

                if _is_local_asset(item_url, page_url):
                    item_url = urljoin(page_url, item_url)
                    filename = _generate_name(item_url)

                    rel_filepath = os.path.join(asset_rel_dir, filename)
                    abs_filepath = os.path.join(asset_abs_dir, filename)

                    item[attr] = rel_filepath
                    assets_map.append({
                        "url": item_url,
                        "filepath": abs_filepath
                    })

                    logging.info(f"Switch asset reference "
                                 f"'{item[attr]}'")

    logging.info("End of analyzing page assets")
    return assets_map


def _download_assets(assets_map: list, asset_abs_dir: str) -> None:
    """Download asset by url to dir.

    :param assets_map: list of url and path for asset
    :return: local name for asset
    """
    if assets_map:
        if not os.path.isdir(asset_abs_dir):
            logging.info(f"Create directory '{asset_abs_dir}' for assets")
            make_dir(asset_abs_dir)

        logging.info("Starting downloading assets")

        bar_name = "Downloading assets: "
        for asset in PixelBar(bar_name).iter(assets_map):
            response = get_response(asset["url"])
            asset_name = asset["filepath"]
            save_file(asset_name, "wb", response.content)


def download(url: str, path: str) -> str:
    """Download page and all local assets.

    :param url: requested url
    :param path: path to download
    :return: path to downloaded page
    """

    # TODO: #1.2 some trouble when root url ends without "/"
    full_url = url if url.endswith("/") else url + "/"

    # --- Get response from url
    response = get_response(url)

    # --- Generate names for page and page's assets directory
    page_name = _generate_name(full_url)
    asset_rel_dir = _generate_name(full_url, isdir=True)
    asset_abs_dir = os.path.join(path, asset_rel_dir)

    # --- Prepare soup
    soup = BeautifulSoup(response.text, features="html.parser")

    # --- Switch assets to local
    assets_map = _switch_assets(soup, full_url, asset_rel_dir, asset_abs_dir)

    # --- Save page
    page_path = save_file(os.path.join(path, page_name),
                          "w",
                          soup.prettify(formatter="html5"))

    # --- Download assets
    _download_assets(assets_map, asset_abs_dir)

    return page_path
