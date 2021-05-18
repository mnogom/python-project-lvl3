"""Request manager."""

import logging

import requests

from page_loader.errors import PLTimeoutError, PLHTTPStatusError, \
    PLTooManyRedirectsError, PLConnectionError


def get_response(url: str):
    """Get response from server.

    :param url: requested url
    :return: full response"""

    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.ConnectionError as exception:
        logging.info(f"Connection error. {exception}")
        raise PLConnectionError(exception)

    except requests.Timeout as exception:
        logging.info(f"Timeout error. {exception}")
        raise PLTimeoutError(exception)

    except requests.TooManyRedirects as exception:
        logging.info(f"TooManyRedirectsError. {exception}")
        raise PLTooManyRedirectsError(exception)

    except requests.HTTPError as exception:
        logging.info(f"Status bad code: {response.status_code}. {exception}")
        raise PLHTTPStatusError(exception)

    return response
