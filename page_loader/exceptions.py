"""Exceptions."""

import requests


class PLPermissionException(PermissionError):
    """Permission error."""

    pass


class PLFileExistsException(FileExistsError):
    """File not found error."""

    pass


class PLHTTPStatusException(requests.HTTPError):
    """Http status error."""

    pass


class PLTooManyRedirectsException(requests.TooManyRedirects):
    """Too many redirects error."""

    pass


class PLTimeoutException(requests.Timeout):
    """Timeout error."""

    pass


class PLConnectionException(requests.ConnectionError):
    """Connection error."""

    pass
