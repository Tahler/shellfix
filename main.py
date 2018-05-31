#!/usr/bin/env python3

import logging
import sys

import fixer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    paths = sys.argv[1:]
    for path in paths:
        fixer.fix_all(path)


if __name__ == '__main__':
    main()
