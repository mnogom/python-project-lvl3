"""Exceptions."""

import requests


class PLPermissionError(PermissionError):
    """Permission error."""

    pass


class PLFileExistsError(FileExistsError):
    """File not found error."""

    pass


class PLHTTPStatusError(requests.HTTPError):
    """Http status error."""

    pass


class PLTooManyRedirectsError(requests.TooManyRedirects):
    """Too many redirects error."""

    pass


class PLTimeoutError(requests.Timeout):
    """Timeout error."""

    pass


class PLConnectionError(requests.ConnectionError):
    """Connection error."""

    pass
