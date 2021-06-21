"""Main features tests."""

import tempfile
import os

import pytest
import requests_mock
import requests

from page_loader.loader import download
from page_loader.errors import PLHTTPStatusError, \
    PLPermissionError, PLFileExistsError, PLTooManyRedirectsError, \
    PLTimeoutError, PLConnectionError

from tests.configurator import setup_mock

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


@pytest.mark.parametrize("with_assets", [True, False])
def test_write_permission_error(with_assets):
    """Check if raise error with writing to non access directory."""

    sys_dir = list(filter(lambda x: x.lower().startswith("sys"),
                          os.listdir("/")))[0]

    with requests_mock.Mocker() as mock_up:
        setup_mock(mock_up, URL, include_assets=with_assets)

        with pytest.raises(PLPermissionError):
            _ = download(URL, f"/{sys_dir}")


@pytest.mark.parametrize("with_assets", [True, False])
def test_write_to_nonexistent_directory(with_assets):
    """Check if raise error with writing to no nonexistent directory."""

    with requests_mock.Mocker() as mock_up:
        setup_mock(mock_up, URL, with_assets)

        with tempfile.TemporaryDirectory() as temp_dir:
            tempfile.TemporaryDirectory()
            with pytest.raises(PLFileExistsError):
                _ = download(URL, f"{temp_dir}/not/existent/dir")
