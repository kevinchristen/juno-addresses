# Copyright 2016, Kevin Christen and the juno-addresses contributors.

from collections import defaultdict
import argparse
import csv
import sys

from juno_addresses import parser


COLUMNS = [
    'Name',
    'Given Name',
    'Family Name',
    'Nickname',
    'E-mail 1 - Value',
    'Phone 1 - Type',
    'Phone 1 - Value',
    'Phone 2 - Type',
    'Phone 2 - Value',
    'Address 1 - Formatted',
]


def format_name(name):
    full = name
    first = last = ''
    names = name.split(',', 1)
    if len(names) == 2:
        first = names[1].strip()
        last = names[0].strip()
        full = '{} {}'.format(first, last)
    return (full, first, last)


def format_address(address):
    return ' '.join(address)


def format_addresses(input, output, include_deleted=False, mappings=[]):
    mapped_fields =  [ mapping.split(':')[0] for mapping in mappings ]
    mapped_columns = [ mapping.split(':')[1] for mapping in mappings ]
    writer = csv.writer(output)
    writer.writerow(COLUMNS + mapped_columns)

    for entry in parser.parser(input):
        if entry['Type'] == 'Entry' and (include_deleted or not entry['Deleted']):
            e = defaultdict(str)
            for k, v in entry.items():
                e[k] = v
                row = format_name(e['Name']) + \
                      ( e['Alias'],
                        e['Email'],
                        'Home', e['Primary Phone'],
                        'Mobile', e['Mobile Phone'],
                        format_address(e['Address']),
                      )
                for mapped_field in mapped_fields:
                    row = row + (e[mapped_field],)

            writer.writerow(row)


def main():
    arg_parser = argparse.ArgumentParser(
        description='Convert a Juno address book into a Gmail compatible CSV file.')
    arg_parser.add_argument(
        'input',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='Juno address book file (addrbook.nv). Defaults to stdin.')
    arg_parser.add_argument(
        'output',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout, help='Output file. Defaults to stdout.')
    arg_parser.add_argument(
        '-d', '--deleted',
        action='store_true',
        help='Include deleted entries')
    arg_parser.add_argument(
        '-m', '--map',
        action='append',
        default=[],
        help='Additional mappings of the form from:to')

    args = arg_parser.parse_args()
    format_addresses(args.input, args.output, include_deleted=args.deleted,
                     mappings=args.map)


if __name__ == '__main__':
    main()
