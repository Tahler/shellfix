#!/usr/bin/env python3

import sys

from fixer import shellcheck


def main():
    paths = sys.argv[1:]

    histogram = {}
    for path in paths:
        errs = shellcheck.run(path)
        for err in errs:
            code = err['code']
            if code not in histogram:
                histogram[code] = 0
            histogram[code] += 1

    sorted_keys = sorted(histogram, key=histogram.get, reverse=True)
    lines = map(lambda key: '{}: {}'.format(key, histogram[key]), sorted_keys)
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
