#!/usr/bin/env python3

"""Entry point."""
import sys

from page_loader.loader import download
from page_loader.cli import parse_args
from page_loader.logger_agent import get_logger
from page_loader.errors import (
    PLTimeoutError,
    PLPermissionError,
    PLConnectionError,
    PLFileExistsError,
    PLTooManyRedirectsError,
    PLHTTPStatusError
)


def main():
    """Parse arguments, get logger, run loader, print result."""

    url, path, debug = parse_args()
    get_logger(debug_mode=debug)

    try:
        final_path = download(url, path)
    except (PLTimeoutError,
            PLConnectionError,
            PLPermissionError,
            PLFileExistsError,
            PLTooManyRedirectsError,
            PLHTTPStatusError) as exception:
        print(str(exception))
        sys.exit(1)

    print(f"Page was successfully downloaded into '{final_path}'")


if __name__ == '__main__':
    main()
