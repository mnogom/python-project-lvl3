"""Request manager."""

import logging
import sys

import requests


def get_response(url: str):
    response = requests.get(url)

    if response.status_code // 100 == 2:
        logging.info(f"Response status code is {response.status_code}")
        return response

    if response.status_code // 100 == 3:
        logging.info(f"Your request was "
                     f"redirected with code "
                     f"{response.status_code}")
        return response

    if response.status_code // 100 == 4:
        logging.warning(f"Bad request. Got error "
                        f"{response.status_code}: "
                        f"{response.reason}")
        sys.exit()

    if response.status_code // 100 == 5:
        logging.warning(f"Bad answer. Got error "
                        f"{response.status_code}: "
                        f"{response.reason}")
        sys.exit()
