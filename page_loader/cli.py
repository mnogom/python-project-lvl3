"""CLI."""

import argparse
import os


def parse_args():
    """Parse input parameters.

    :return: url, file path and debug status
    """

    parser = argparse.ArgumentParser(description="Page loader")
    parser.add_argument(dest="url", help="URL")
    parser.add_argument("-o", "--output",
                        help="destination for download",
                        default=os.getcwd())
    parser.add_argument("-d", "--debug",
                        help="activate DEBUG mode",
                        default=False,
                        action="store_true")
    args = parser.parse_args()

    return args.url, args.output, args.debug
