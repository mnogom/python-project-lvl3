#!/usr/bin/env python3

"""Entry point."""

from page_loader.loader import download
from page_loader.cli import parse_args
from page_loader.logger_agent import get_logger


def main():
    url, path, debug = parse_args()
    if debug:
        get_logger()
    download(url, path)


if __name__ == '__main__':
    main()
