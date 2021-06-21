import os
import tempfile

import requests_mock

from page_loader.loader import download
from tests.configurator import setup_mock


DEMO_URLS = [
    "http://example.ru",
    "http://example.ru/",
]
RIGHT_HTML_DIR = "tests/fixtures/demo_page/out"
FIXTURE_DIR = "tests/fixtures/demo_page/"


def _compare_files_content(result_path, right_path):
    with open(result_path, "rb") as file:
        result_content = file.read()
    with open(right_path, "rb") as file:
        right_content = file.read()

    return result_content == right_content


def test_download_page():
    """Check main features of app."""

    for url in DEMO_URLS:

        with requests_mock.Mocker() as mock_up:
            setup_mock(mock_up, url, include_assets=True)

            with tempfile.TemporaryDirectory(dir=FIXTURE_DIR) as temp_dir:
                result = download(url, temp_dir)

                result_path, _ = os.path.split(result)
                result_tree = sorted(list(os.walk(result_path)))
                right_tree = sorted(list(os.walk(RIGHT_HTML_DIR)))

                for result_node, right_node in zip(result_tree, right_tree):
                    result_dir_name, result_dirs, result_files = result_node
                    right_dir_name, right_dirs, right_files = right_node

                    assert sorted(result_dirs) == sorted(right_dirs)
                    assert sorted(result_files) == sorted(right_files)

                    result_files = sorted(result_files)
                    right_files = sorted(right_files)

                    for result_file, right_file in zip(result_files,
                                                       right_files):
                        assert _compare_files_content(
                            f"{result_dir_name}/{result_file}",
                            f"{right_dir_name}/{right_file}"
                        )
