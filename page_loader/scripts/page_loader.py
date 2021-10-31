import argparse
import os
from page_loader.loader import download


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('--output',
                        default=os.getcwd(),
                        help='set output path',
                        type=str)
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    print(download(args.output, args.url))


if __name__ == '__main__':
    main()
