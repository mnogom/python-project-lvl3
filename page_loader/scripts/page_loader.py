#!/usr/bin/env python3

"""Entry point."""

from page_loader.loader import download
from page_loader.cli import parse_args


def main():
    url, path = parse_args()
    download(url, path)


if __name__ == '__main__':
    main()
