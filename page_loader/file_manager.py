"""File manager."""

import logging
import os
# import sys


def create_directory(path: str) -> str:
    logging.info(f"Creating '{path}'")

    try:
        os.mkdir(f"{path}")

    except FileExistsError:
        logging.info(f"{path} already exists.")

    except Exception as error:
        logging.warning(error)
        raise error

    logging.info(f"{path} was created")
    return f"{path}"


def save_file(filename, mode, file_data) -> str:
    logging.info(f"Starting to save '{filename}'")

    try:
        with open(filename, mode) as file:
            file.write(file_data)

    except Exception as error:
        logging.warning(error)
        raise error

    logging.info(f"File '{filename}' was saved with mode '{mode}'")
    return filename
