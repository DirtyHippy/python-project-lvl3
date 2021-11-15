import argparse
import os
import sys
from page_loader.loader import download
from page_loader.exceptions import AppInternalError
from page_loader.logging_utils import init_logger


logger = init_logger()


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
        file_name = download(args.url, args.output)
    except AppInternalError as e:
        logger.debug(e)
        sys.exit(1)
    print(f"\n{args.url} saved to {file_name}")
    sys.exit(0)


if __name__ == '__main__':
    main()
