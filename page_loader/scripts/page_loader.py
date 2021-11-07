import argparse
import os
import sys
from page_loader.loader import download


def main():
    try:
        parser = argparse.ArgumentParser(description='page loader')
        parser.add_argument('url', type=str)
        parser.add_argument('-o',
                            '--output',
                            default=os.getcwd(),
                            help='set output path',
                            type=str)
        args = parser.parse_args()
        download(args.url, args.output)
    except Exception:
        sys.exit()


if __name__ == '__main__':
    main()
