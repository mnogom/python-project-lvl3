"""Exceptions."""


class PLPermissionException(Exception):
    """Permission error."""

    pass


class PLFileExistsException(Exception):
    """File not found error."""

    pass


class PLHTTPStatusException(Exception):
    """Http status error."""

    pass


class PLTooManyRedirectsException(Exception):
    """Too many redirects error."""

    pass


class PLTimeoutException(Exception):
    """Timeout error."""

    pass


class PLConnectionException(Exception):
    """Connection error."""

    pass
