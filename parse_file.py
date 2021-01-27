#!/usr/local/bin/python3.9
import sys
import os
import gzip
from pprint import pprint

# Check args
if len(sys.argv) != 2:
    print('Invalid number of arguments')
    sys.exit(1)

# Get file path
file = sys.argv[1]

# Check if file exists
if not os.path.exists(file):
    print('File doesn\'t exist')
    sys.exit(1)


def open_file(file):
    if file.endswith('gz'):
        with gzip.open(file) as f:
            return parse_file(f)
    else:
        with open(file) as f:
            return parse_file(f)


def parse_file(file):
    result = []
    key = None  # Init key variable to track lines with values
    while line := file.readline():
        # Decode line to str if opened gzip file
        if type(line) is bytes:
            line = line.decode('utf-8')

        # Create new document
        if line == '\n':
            document = {}
            result.append(document)
            continue

        # Check if line doesn't include key
        if line.startswith(' '):
            value = line.strip()
            document[key] = ''.join([document[key], value])
        else:
            line = line.strip().split(' ')
            # Check if line includes key
            if line[0].endswith(':'):
                key, value = get_key_value(line)
                if key in document.keys():
                    document[key] = '\n'.join([document[key], value])
                else:
                    document[key] = value
    return result


def get_key_value(line: str):
    key = line[0].replace(':', '')
    value = ' '.join(line[1:]).lstrip()
    return key, value


def load_data(text_file):
    res = open_file(text_file)

    for el in res:
        pprint(el)
        print('\n')


if __name__ == '__main__':
    load_data(file)
