import os
import tempfile

from requests_mock import Mocker

from page_loader.loader import download
from urllib.parse import urljoin


URL = "http://example.ru"
RIGHT_HTML_DIR = "tests/fixtures/demo_page/out"
FIXTURE_DIR = "tests/fixtures/demo_page/"


def _get_contents():
    """Get html, css, img, js test content."""

    with open("tests/fixtures/demo_page/in/example.html", "r") as file:
        html_text = file.read()
    with open("tests/fixtures/demo_page/in/css/styles.css", "rb") as file:
        css_content = file.read()
    with open("tests/fixtures/demo_page/in/img/googlelogo.png", "rb") as file:
        img_content = file.read()
    with open("tests/fixtures/demo_page/in/js/scripts.js", "rb") as file:
        js_content = file.read()

    return html_text, css_content, img_content, js_content


def _setup_mock(mock_up, url: str):
    """Setup mock up for url.
    :param mock_up: mock object
    :param url: url
    """

    (html_text,
     css_content,
     img_content,
     js_content) = _get_contents()

    mock_up.get(url, text=html_text)
    mock_up.get(urljoin(url, "css/styles.css"), content=css_content)
    mock_up.get(urljoin(url, "img/googlelogo.png"), content=img_content)
    mock_up.get(urljoin(url, "js/scripts.js"), content=js_content)


def _compare_files_content(result_path, right_path):
    with open(result_path, "rb") as file:
        result_content = file.read()
    with open(right_path, "rb") as file:
        right_content = file.read()

    return result_content == right_content


def test_download_page():
    """Check main features of app."""

    with Mocker() as mock_up:
        _setup_mock(mock_up, URL)

        with tempfile.TemporaryDirectory(dir=FIXTURE_DIR) as temp_dir:
            result = download(URL, temp_dir)

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
                        os.path.join(result_dir_name, result_file),
                        os.path.join(right_dir_name, right_file)
                    )
