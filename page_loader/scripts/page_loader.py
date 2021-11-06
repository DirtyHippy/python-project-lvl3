import argparse
import os
from page_loader.loader import download


def main():
    parser = argparse.ArgumentParser(description='page loader')
    parser.add_argument('url', type=str)
    parser.add_argument('-o',
                        '--output',
                        default=os.getcwd(),
                        help='set output path',
                        type=str)
    args = parser.parse_args()
    download(args.url, args.output)


if __name__ == '__main__':
    main()
