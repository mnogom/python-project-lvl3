"""File manager."""

import os
import logging

from page_loader.exceptions import PLPermissionError, PLFileExistsError


def make_dir(path: str) -> str:
    """Crete directory.

    :param path: full path to directory with its name
    :return: full path
    """

    logging.info(f"Creating '{path}'")

    try:
        os.mkdir(path)

    except FileExistsError:
        logging.info(f"{path} already exists.")

    except PermissionError as exception:
        logging.info(exception)
        raise PLPermissionError(exception)

    except FileNotFoundError as exception:
        logging.info(exception)
        raise PLFileExistsError(exception)

    logging.info(f"{path} was created")
    return path


def save_file(filename: str, mode: str, data: any) -> str:
    """Save data to file.

    :param filename: full path
    :param mode: type of writing possible: 'w' | 'wb'
    :param data: data to save
    :return: full path to file
    """

    logging.info(f"Starting to save '{filename}'")

    try:
        with open(filename, mode) as file:
            file.write(data)

    except PermissionError as exception:
        logging.info(exception)
        raise PLPermissionError(exception)

    except FileNotFoundError as exception:
        logging.info(exception)
        raise PLFileExistsError(exception)

    logging.info(f"File '{filename}' was saved with mode '{mode}'")
    return filename
