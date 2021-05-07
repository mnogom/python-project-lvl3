"""Request manager."""

import logging

import requests


def get_response(url: str):
    """Get response from server.

    :param url: requested url
    :return: full response"""

    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.ConnectionError as error:
        logging.warning(f"Connection error. {error}")
        raise error

    except requests.Timeout as error:
        logging.warning(f"Timeout error. {error}")
        raise error

    except requests.TooManyRedirects as error:
        logging.warning(f"TooManyRedirectsError. {error}")
        raise error

    except requests.HTTPError as error:
        logging.warning(f"Status bad code: {response.status_code}. {error}")
        raise error

    return response
