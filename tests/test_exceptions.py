"""Main features tests."""

import pytest
from requests_mock import Mocker
from requests.exceptions import Timeout, ConnectionError, TooManyRedirects

from page_loader.loader import download
from page_loader.exceptions import (PLHTTPStatusException,
                                    PLPermissionException,
                                    PLFileExistsException,
                                    PLTooManyRedirectsException,
                                    PLTimeoutException,
                                    PLConnectionException)

URL = "https://example.ru"
HTML_PAGE = "Empty page"


@pytest.mark.parametrize("status_code",
                         [404, 503])
def test_requests_errors(status_code):
    """Check if raise exception for response with status codes 4** and 5**."""

    with Mocker() as mock_up:
        mock_up.get(URL, status_code=status_code)

        with pytest.raises(PLHTTPStatusException):
            _ = download(URL)


@pytest.mark.parametrize("error, exception",
                         [(Timeout, PLTimeoutException),
                          (ConnectionError, PLConnectionException),
                          (TooManyRedirects, PLTooManyRedirectsException)])
def test_connection_exceptions(error, exception):
    """Check if raises Timeout, Connection and TooManyRedirect exceptions."""

    with Mocker() as mock_up:
        mock_up.register_uri("GET", URL, exc=error)

        with pytest.raises(exception):
            _ = download(URL)


@pytest.mark.parametrize("dir_path, exception",
                         [("/", PLPermissionException),
                          ("not/existent/dir", PLFileExistsException)])
def test_file_exceptions(dir_path, exception):
    """Check if raises Permission and FileExists exceptions."""

    with Mocker() as mock_up:
        mock_up.register_uri("GET", URL, text=HTML_PAGE)

        with pytest.raises(exception):
            _ = download(URL, dir_path)
