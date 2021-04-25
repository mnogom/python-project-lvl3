"""CLI."""

import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Page loader")
    parser.add_argument(dest="url", help="URL")
    parser.add_argument("-o", "--output",
                        help="Destination for download",
                        default=os.getcwd())
    args = parser.parse_args()

    return args.url, args.output
