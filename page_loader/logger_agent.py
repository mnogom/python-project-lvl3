"""Logger agent."""

import sys
import logging


def get_logger(debug_mode):
    """Init logger configuration."""

    root = logging.getLogger()

    if debug_mode:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.WARNING)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - "
                                  "[%(levelname)s] -  "
                                  "%(name)s - "
                                  "(%(filename)s)."
                                  "%(funcName)s"
                                  "(%(lineno)d) - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)
