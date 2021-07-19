import os
import tempfile

import pytest

from page_loader.loader import download
from urllib.parse import urljoin

URL = "https://example.ru/subpage/"
ASSETS_INFO = ({"path": "css/rel-styles.css",
                "url": "css/rel-styles.css"},
               {"path": "css/abs-styles.css",
                "url": "/css/abs-styles.css"},
               {"path": "css/full-styles.css",
                "url": "https://example.ru/css/full-styles.css"},
               {"path": "img/rel-googlelogo.png",
                "url": "img/rel-googlelogo.png"},
               {"path": "img/abs-googlelogo.png",
                "url": "/img/abs-googlelogo.png"},
               {"path": "img/full-googlelogo.png",
                "url": "https://example.ru/img/full-googlelogo.png"},
               {"path": "js/rel-scripts.js",
                "url": "js/rel-scripts.js"},
               {"path": "js/abs-scripts.js",
                "url": "/js/abs-scripts.js"},
               {"path": "js/full-scripts.js",
                "url": "https://example.ru/js/full-scripts.js"},)

EXPECTED_HTML_DIR = "tests/fixtures/demo_page/out"
EXPECTED_FILENAME = "example-ru-subpage.html"
EXPECTED_ASSETS_DIR = "example-ru-subpage_files"
FIXTURE_DIR = "tests/fixtures/demo_page/in"


@pytest.fixture
def html():
    """Get html fixture."""

    data = {"url": URL}
    with open(os.path.join(FIXTURE_DIR, "example.html"), "r") as file:
        data["text"] = file.read()
    return data


@pytest.fixture
def assets():
    """Get assets fixtures."""

    data = []
    for asset in ASSETS_INFO:
        element = {"url": urljoin(URL, asset["url"])}
        with open(os.path.join(FIXTURE_DIR, asset["path"]), "rb") as file:
            element["content"] = file.read()
        data.append(element)
    return data


def _setup_mock(requests_mock, html, assets):
    """Setup mock up for url.
    :param requests_mock: mock object
    :param html: html fixture
    :param assets: assets fixtures
    """

    url = html["url"]
    requests_mock.get(url, text=html["text"])

    for asset in assets:
        requests_mock.get(asset["url"], content=asset["content"])


def _compare_files_content(result_path, expected_path):
    """Compare two files with 'rb' flag."""

    with open(result_path, "rb") as file:
        result_content = file.read()
    with open(expected_path, "rb") as file:
        expected_content = file.read()

    return result_content == expected_content


def test_download_page(requests_mock, html, assets):
    """Check main features of app.

    :param html: html fixture
    :param assets: assets fixtures
    """

    _setup_mock(requests_mock, html, assets)

    with tempfile.TemporaryDirectory() as temp_dir:
        result = download(URL, temp_dir)

        # Check if path is correct and if page name is correctly generated
        result_filepath, result_filename = os.path.split(result)
        assert result_filepath == temp_dir
        assert result_filename == EXPECTED_FILENAME

        # Check if HTML content is similar
        assert _compare_files_content(result, os.path.join(EXPECTED_HTML_DIR,
                                                           EXPECTED_FILENAME))

        # Check assets
        result_assets_dir = os.path.join(temp_dir,
                                         EXPECTED_ASSETS_DIR)
        expected_assets_dir = os.path.join(EXPECTED_HTML_DIR,
                                           EXPECTED_ASSETS_DIR)

        # Check if assets directory exists
        assert os.path.isdir(result_assets_dir)

        # Check if count of result and expected assets are similar
        result_assets = sorted(os.listdir(result_assets_dir))
        expected_assets = sorted(os.listdir(expected_assets_dir))
        assert len(result_assets) == len(expected_assets)

        # Check if name and content of result and expected assets are similar
        for result_asset_name, expected_asset_name in zip(result_assets,
                                                          expected_assets):
            assert result_asset_name == expected_asset_name

            result_asset_path = os.path.join(temp_dir,
                                             EXPECTED_ASSETS_DIR,
                                             result_asset_name)
            expected_asset_path = os.path.join(EXPECTED_HTML_DIR,
                                               EXPECTED_ASSETS_DIR,
                                               expected_asset_name)
            assert _compare_files_content(result_asset_path,
                                          expected_asset_path)
