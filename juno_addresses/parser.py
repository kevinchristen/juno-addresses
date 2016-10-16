# Copyright 2016, Kevin Christen and the juno-addresses contributors.

import sys


def parse_line(line):
    '''Return the contents of a parsed line from a Juno address book.

    Returns (key, value) unless there is no value, in which case returns
    (key,). Returns None for an empty line.
    '''

    fields = line.rstrip().split(':', 1)
    if len(fields) > 1 and fields[1]:
        return (fields[0].rstrip(), fields[1])
    elif len(fields) > 0 and fields[0]:
        return (fields[0].rstrip(),)
    return


def parse_address(address):
    return [line for line in address.split('^^') if line]


def parse_entry(f):
    '''Returns a dict of the contents of an address book entry read from file f.

    'Entry' here refers to the lines delimited from the surrounding
    entries by one or more blank lines, not just those of Type:Entry.
    '''

    entry = {}
    for line in f:
        parsed = parse_line(line)
        if not parsed:
            if not entry:
                continue # consume leading blank lines
            break # return after consuming first trailing blank line
        elif len(parsed) == 2 and parsed[1]:
            key, value = parsed
            entry[key] = value
        else:
            continue

    if 'Deleted' in entry:
        entry['Deleted'] = bool(int(entry['Deleted']))
    if 'Address' in entry:
        entry['Address'] = parse_address(entry['Address'])
    return entry


def parser(f):
    '''A generator for entries in the file f'''

    while True:
        entry = parse_entry(f)
        if entry:
            yield entry
        else:
            return


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as contacts:
        for entry in parser(contacts):
            print(entry)
