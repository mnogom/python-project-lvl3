"""Main features tests."""

import tempfile
import os

import pytest
import requests_mock
import requests
from urllib.parse import urljoin

from page_loader.loader import download
from page_loader.errors import PLHTTPStatusError, \
    PLPermissionError, PLFileNotFoundError, PLTooManyRedirectsError, \
    PLTimeoutError, PLConnectionError

from tests.loader_tests import _get_contents

URL = "https://example.ru"


@pytest.mark.parametrize("status_code",
                         [404, 503])
def test_requests_errors(status_code):
    """Check if raise error with response status codes 4** and 5**."""

    with requests_mock.Mocker() as mock_up:
        mock_up.get(URL, status_code=status_code)

        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(PLHTTPStatusError):
                _ = download(URL, temp_dir)


def test_too_many_redirects():
    """Check if raise error for too many redirects."""

    with requests_mock.Mocker() as mock_up:
        mock_up.get(URL, status_code=301, headers={"Location": URL})

        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(PLTooManyRedirectsError):
                _ = download(URL, temp_dir)


def test_timeout_error():
    """Check if raise timeout error."""

    with requests_mock.Mocker() as mock_up:
        mock_up.register_uri("GET", URL, exc=requests.exceptions.Timeout)

        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(PLTimeoutError):
                _ = download(URL, temp_dir)


def test_connection_error():
    """Check if raise connection error."""

    with requests_mock.Mocker() as mock_up:
        mock_up.register_uri("GET", URL,
                             exc=requests.exceptions.ConnectionError)

        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(PLConnectionError):
                _ = download(URL, temp_dir)


@pytest.mark.parametrize("with_asserts", [True, False])
def test_write_permission_error(with_asserts):
    """Check if raise error with writing to non access directory."""

    sys_dir = list(filter(lambda x: x.lower().startswith("sys"),
                          os.listdir("/")))[0]

    with requests_mock.Mocker() as mock_up:
        if with_asserts:
            (html_text,
             css_content,
             img_content,
             js_content) = _get_contents()

            mock_up.get(URL, text=html_text)
            mock_up.get(urljoin(URL, "css/styles.css"), content=css_content)
            mock_up.get(urljoin(URL, "img/googlelogo.png"), content=img_content)
            mock_up.get(urljoin(URL, "js/scripts.js"), content=js_content)

        else:
            mock_up.get(URL, text="empty")

        with pytest.raises(PLPermissionError):
            _ = download(URL, f"/{sys_dir}")


@pytest.mark.parametrize("with_asserts", [True, False])
def test_write_to_nonexistent_directory(with_asserts):
    """Check if raise error with writing to no nonexistent directory."""

    with requests_mock.Mocker() as mock_up:
        if with_asserts:
            (html_text,
             css_content,
             img_content,
             js_content) = _get_contents()

            mock_up.get(URL, text=html_text)
            mock_up.get(urljoin(URL, "css/styles.css"), content=css_content)
            mock_up.get(urljoin(URL, "img/googlelogo.png"), content=img_content)
            mock_up.get(urljoin(URL, "js/scripts.js"), content=js_content)

        else:
            mock_up.get(URL, text="empty")

        with tempfile.TemporaryDirectory() as temp_dir:
            tempfile.TemporaryDirectory()
            with pytest.raises(PLFileNotFoundError):
                _ = download(URL, f"{temp_dir}/not/existent/dir")
