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
    """Check if raise error with writing to no nonexistent directory"""

    with requests_mock.Mocker() as mock_up:
        mock_up.get(DEMO_URL, text="demo")

        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(FileNotFoundError):
                _ = download(DEMO_URL, f"{temp_dir}/not/existent/dir")
