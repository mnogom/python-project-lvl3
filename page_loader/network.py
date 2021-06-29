"""Network."""

import logging

import requests

from page_loader.exceptions import (PLTimeoutException,
                                    PLHTTPStatusException,
                                    PLTooManyRedirectsException,
                                    PLConnectionException)


def make_request(url: str):
    """Make request to server.

    :param url: requested url
    :return: full response"""

    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.ConnectionError as exception:
        logging.info(f"Connection error. {exception}")
        raise PLConnectionException(exception)

    except requests.Timeout as exception:
        logging.info(f"Timeout error. {exception}")
        raise PLTimeoutException(exception)

    except requests.TooManyRedirects as exception:
        logging.info(f"TooManyRedirectsError. {exception}")
        raise PLTooManyRedirectsException(exception)

    except requests.HTTPError as exception:
        logging.info(f"Status bad code: {response.status_code}. {exception}")
        raise PLHTTPStatusException(exception)

    return response
