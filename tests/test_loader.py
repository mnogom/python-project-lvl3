import os
import tempfile

import pytest
from requests_mock import Mocker

from page_loader.loader import download
from urllib.parse import urljoin


URL = "http://example.ru"
ASSETS_PATHS = ("css/abs-styles.css",
                "css/rel-styles.css",
                "img/abs-googlelogo.png",
                "img/rel-googlelogo.png",
                "js/abs-scripts.js",
                "js/rel-scripts.js", )
EXPECTED_HTML_DIR = "tests/fixtures/demo_page/out"
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
    for asset_path in ASSETS_PATHS:
        element = {"url": asset_path}
        with open(os.path.join(FIXTURE_DIR, asset_path), "rb") as file:
            element["content"] = file.read()
        data.append(element)
    return data


def _setup_mock(mock_up, html, assets):
    """Setup mock up for url.
    :param mock_up: mock object
    :param html: html fixture
    :param assets: assets fixtures
    """

    url = html["url"]
    mock_up.get(url, text=html["text"])

    for asset in assets:
        mock_up.get(urljoin(url, asset["url"]), content=asset["content"])


def _compare_files_content(result_path, expected_path):
    """Compare two files with 'rb' flag."""

    with open(result_path, "rb") as file:
        result_content = file.read()
    with open(expected_path, "rb") as file:
        expected_content = file.read()

    return result_content == expected_content


def test_download_page(html, assets):
    """Check main features of app.
    :param html: html fixture
    :param assets: assets fixtures
    """

    with Mocker() as mock_up:
        _setup_mock(mock_up, html, assets)

        with tempfile.TemporaryDirectory() as temp_dir:
            result = download(URL, temp_dir)

            result_path, _ = os.path.split(result)
            result_tree = sorted(list(os.walk(result_path)))
            expected_tree = sorted(list(os.walk(EXPECTED_HTML_DIR)))

            for result_node, expected_node in zip(result_tree, expected_tree):
                result_dir_name, result_dirs, result_files = result_node
                expected_dir_name, expected_dirs, expected_files = expected_node

                assert sorted(result_dirs) == sorted(expected_dirs)
                assert sorted(result_files) == sorted(expected_files)

                result_files = sorted(result_files)
                expected_files = sorted(expected_files)

                for result_file, expected_file in zip(result_files,
                                                      expected_files):
                    assert _compare_files_content(
                        os.path.join(result_dir_name, result_file),
                        os.path.join(expected_dir_name, expected_file)
                    )
