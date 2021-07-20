"""Loader."""

import os
import re
from urllib.parse import urlparse, urljoin
import logging

from bs4 import BeautifulSoup
from progress.bar import PixelBar

from page_loader.file_system import make_dir, save_file
from page_loader.network import make_request


def _generate_name(url: str, is_dir=False) -> str:
    """Convert url to local name.

    :param url: input url
    :param is_dir: is name for directory
    :return: local name for url
    """

    url = url[:-1] if url.endswith("/") else url
    parsed_url = urlparse(url)

    path, ext = os.path.splitext(parsed_url.path)
    path = path if path != "/" else ""
    ext = ext if ext else ".html"

    filename = f"{parsed_url.netloc}{path}"
    filename += f"?{parsed_url.query}" if parsed_url.query else ""
    filename = re.sub(r"\W", "-", filename)

    if is_dir:
        full_filename = filename + "_files"
        logging.info(f"Create name '{full_filename}' for  directory of "
                     f"references of '{url}'")
        return full_filename

    full_filename = filename + ext
    logging.info(f"Create name '{full_filename}' for url '{url}'")

    return full_filename


def _is_local_asset(page_url: str, full_item_url: str) -> bool:
    """Check if asset is local.

    :param full_item_url: full asset url
    :param page_url: page url
    :return: True/False
    """

    page_url_netloc = urlparse(page_url).netloc
    item_url_netloc = urlparse(full_item_url).netloc

    return page_url_netloc == item_url_netloc


def _switch_assets(soup, page_url: str, asset_rel_dir: str) -> list:
    """Find and switch all local assets

    :param soup: soup data
    :param page_url: main url
    :param asset_rel_dir: directory for page assets
    :return: assets urls with local paths
    """

    logging.info("Starting analyzing page assets")

    page_url += "/"

    assets_types = {
        "img": "src",
        "script": "src",
        "link": "href"
    }
    assets_to_download = []

    for tag, attr in assets_types.items():

        asset_items = soup.find_all(tag)
        for item in asset_items:
            logging.info(f"Analyze '{attr}' in '{tag}'")

            asset_url = item.get(attr)

            if asset_url:
                full_asset_url = urljoin(page_url, asset_url)

                if _is_local_asset(page_url, full_asset_url):
                    filename = _generate_name(full_asset_url)

                    rel_filepath = os.path.join(asset_rel_dir, filename)

                    item[attr] = rel_filepath
                    assets_to_download.append({
                        "url": full_asset_url,
                        "filename": filename
                    })

                    logging.info(f"Switch asset reference "
                                 f"'{item[attr]}'")

    logging.info("End of analyzing page assets")
    return assets_to_download


def _download_assets(assets_to_download: list, asset_abs_dir: str) -> None:
    """Download asset by url to dir.

    :param assets_to_download: list of url and path for asset
    :return: local name for asset
    """

    if not os.path.isdir(asset_abs_dir):
        logging.info(f"Create directory '{asset_abs_dir}' for assets")
        make_dir(asset_abs_dir)

    logging.info("Starting downloading assets")

    bar_name = "Downloading assets: "
    for asset in PixelBar(bar_name).iter(assets_to_download):
        response = make_request(asset["url"])
        asset_path = os.path.join(asset_abs_dir, asset["filename"])
        save_file(asset_path, "wb", response.content)


def download(url: str, path=os.getcwd()) -> str:
    """Download page and all local assets.

    :param url: requested url
    :param path: path to download
    :return: path to downloaded page
    """

    response = make_request(url)

    page_name = _generate_name(url)
    asset_rel_dir = _generate_name(url, is_dir=True)
    asset_abs_dir = os.path.join(path, asset_rel_dir)

    soup = BeautifulSoup(response.text, features="html.parser")
    assets_to_download = _switch_assets(soup, url, asset_rel_dir)

    page_path = save_file(os.path.join(path, page_name),
                          "w",
                          soup.prettify(formatter="html5"))

    if assets_to_download:
        _download_assets(assets_to_download, asset_abs_dir)

    return page_path
