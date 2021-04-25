"""File manager."""

import logging
import os
import sys


def create_directory(path: str, dir_name: str) -> str:
    logging.info(f"Creating '{path}{dir_name}'")
    try:
        os.mkdir(f"{path}{dir_name}")

    except FileExistsError:
        logging.info(f"{path}{dir_name} already exists.")

    except Exception as error:
        logging.warning(error)
        sys.exit()

    logging.info(f"{path}{dir_name} was created")
    return f"{path}{dir_name}"


def save_file(filename, mode, filedata) -> str:
    logging.info(f"Starting to save '{filename}'")
    try:
        with open(filename, mode) as file:
            file.write(filedata)

    except Exception as error:
        logging.warning(error)
        sys.exit()

    logging.info(f"File '{filename}' was saved with mode '{mode}'")
    return filename
