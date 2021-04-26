"""Logger agent."""

import sys
import logging


def get_logger():
    """Init logger configuration."""

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

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
