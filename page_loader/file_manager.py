"""File manager."""

import logging
import os


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

    except OSError as error:
        logging.warning(error)
        raise error

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

    except OSError as error:
        logging.warning(error)
        raise error

    logging.info(f"File '{filename}' was saved with mode '{mode}'")
    return filename
