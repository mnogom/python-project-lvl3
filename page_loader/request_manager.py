"""Request manager."""

import logging

import requests


def get_response(url: str):
    """Get response from server.

    :param url: requested url
    :return: full response"""

    response = requests.get(url)
    status_code = response.status_code

    if status_code // 100 == 2:
        logging.info(f"Response status code is {response.status_code}")
        return response

    if status_code // 100 == 3:
        logging.info(f"Your request was "
                     f"redirected with code "
                     f"{response.status_code}")
        return response

    if status_code // 100 == 4:
        logging.warning(f"Bad request. Got error "
                        f"{response.status_code}: "
                        f"{response.reason}")
        raise response.raise_for_status()

    if status_code // 100 == 5:
        logging.warning(f"Bad answer. Got error "
                        f"{response.status_code}: "
                        f"{response.reason}")
        raise response.raise_for_status()
