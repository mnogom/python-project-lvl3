"""Main features tests."""

import tempfile
import os

import pytest
import requests_mock

from page_loader.loader import download


DEMO_URL = "http://example.ru"


@pytest.mark.parametrize("status_code",
                         [404, 503])
def test_requests_errors(status_code):
    """Check if raise error with response status codes 4** and 5**."""

    with requests_mock.Mocker() as mock_up:
        mock_up.get(DEMO_URL, status_code=status_code)

        with pytest.raises(ConnectionError):
            _ = download(DEMO_URL, os.getcwd())


def test_write_permission_error():
    """Check if raise error with writing to non access directory."""

    sys_dir = list(filter(lambda x: x.lower().startswith("sys"),
                          os.listdir("/")))[0]

    with requests_mock.Mocker() as mock_up:
        mock_up.get(DEMO_URL, text="demo")

        with pytest.raises(PermissionError):
            _ = download(DEMO_URL, f"/{sys_dir}")


def test_write_read_only_error():
    """Check if raise error with writing to non access directory."""

    with requests_mock.Mocker() as mock_up:
        mock_up.get(DEMO_URL, text="demo")

        with pytest.raises(OSError):
            _ = download(DEMO_URL, "/")


def test_write_to_nonexistent_directory():
    """Check if raise error with writing to no nonexistent directory."""

    with requests_mock.Mocker() as mock_up:
        mock_up.get(DEMO_URL, text="demo")

        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(FileNotFoundError):
                _ = download(DEMO_URL, f"{temp_dir}/not/existent/dir")


def _get_all_files(path):
    file_list = os.listdir(path)
    ref_path = list(filter(lambda x: x.endswith("_files"), file_list))[0]
    file_list += os.listdir(f"{path}/{ref_path}")
    return sorted(file_list)


def test_download_page():
    """Check main features of app."""

    with open("tests/fixtures/demo_page/in/example.html", "r") as file:
        html_text = file.read()
    with open("tests/fixtures/demo_page/in/css/styles.css", "rb") as file:
        css_content = file.read()
    with open("tests/fixtures/demo_page/in/img/googlelogo_color_272x92dp.png", "rb") as file:
        img_content = file.read()
    with open("tests/fixtures/demo_page/in/js/scripts.js", "rb") as file:
        js_content = file.read()

    with requests_mock.Mocker() as mock_up:
        mock_up.get(DEMO_URL, text=html_text)
        mock_up.get(f"{DEMO_URL}/css/styles.css", content=css_content)
        mock_up.get(f"{DEMO_URL}/img/googlelogo_color_272x92dp.png", content=img_content)
        mock_up.get(f"{DEMO_URL}/js/scripts.js", content=js_content)

        with tempfile.TemporaryDirectory(dir="tests/fixtures/demo_page/") as temp_dir:
            result = download(DEMO_URL, temp_dir)

            _, filename = os.path.split(result)

            with open(result, "r") as file:
                result_html = file.read()
            with open(f"tests/fixtures/demo_page/out/{filename}", "r") as file:
                right_html = file.read()
            assert result_html == right_html

            refs_main_path = result.replace(".html", "_files")
            for ref_path in os.listdir(refs_main_path):
                _, ref_filename = os.path.split(ref_path)
                with open(f"{refs_main_path}/{ref_path}", "rb") as file:
                    result_ref = file.read()
                with open(f"tests/fixtures/demo_page/out/example-ru_files/{ref_filename}", "rb") as file:
                    right_ref = file.read()
                assert result_ref == right_ref
