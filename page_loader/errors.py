"""Errors."""

import requests


class PLPermissionError(PermissionError):
    """Permission error."""

    pass


class PLFileNotFoundError(FileExistsError):
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
