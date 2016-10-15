from collections import defaultdict
import csv
import sys

from juno_addresses import parser


COLUMNS = [
    'Name',
    'Given Name',
    'Family Name',
    'E-mail 1 - Value',
    'Phone 1 - Type',
    'Phone 1 - Value',
    'Phone 2 - Type',
    'Phone 2 - Value',
    'Address 1 - Formatted',
]
KEYS = [ 'Name', 'Email', 'Primary Phone', 'Mobile Phone', 'Address' ]


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


HEADER = ','.join([ column[0] for column in COLUMNS ])


if __name__ == '__main__':
    writer = csv.writer(sys.stdout)
    writer.writerow(COLUMNS)
    with open(sys.argv[1], 'r') as contacts:
        for entry in parser.parser(contacts):
            if entry['Type'] == 'Entry' and not entry['Deleted']:
                e = defaultdict(str)
                for k, v in entry.items():
                    e[k] = v
                row = format_name(e['Name']) + \
                      ( e['Email'],
                        'Home', e['Primary Phone'],
                        'Mobile', e['Mobile Phone'],
                        format_address(e['Address']) )
                writer.writerow(row)
