# Copyright 2016, Kevin Christen and the juno-addresses contributors.

import io
import unittest

from juno_addresses.parser import *


class TestParsing(unittest.TestCase):

    def test_parse_empty_line(self):
        self.assertEqual(parse_line(''), None)

    def test_parse_whitespace_line(self):
        self.assertEqual(parse_line(' '), None)

    def test_parse_line_without_value(self):
        self.assertEqual(parse_line('Name:'), ('Name',))

    def test_parse_line_with_whitespace_but_no_value(self):
        self.assertEqual(parse_line('Name :'), ('Name',))

    def test_parse_line(self):
        self.assertEqual(parse_line('Name:Value'), ('Name', 'Value'))

    def test_parse_line_with_whitespace(self):
        self.assertEqual(parse_line('Name :Value '), ('Name', 'Value'))

    def test_parse_line_with_colon(self):
        self.assertEqual(parse_line('Name:http://foo.com'), ('Name', 'http://foo.com'))

    entries = '''

Type:Version
Version:AB 0.3.0


Type:Entry
Email:help@support.juno.com
Name:Juno
Deleted:1

Type:Entry
Email:president@whitehouse.gov
Name:POTUS
Deleted:0
Address:1600 Pennsylvania Ave. NW^^Washington DC, 20500

'''

    def test_parse_entries(self):
        address_book = io.StringIO(TestParsing.entries)

        entry = parse_entry(address_book)
        self.assertEqual(len(entry), 2)
        self.assertEqual(entry['Type'], 'Version')
        self.assertEqual(entry['Version'], 'AB 0.3.0')

        entry = parse_entry(address_book)
        self.assertEqual(len(entry), 4)
        self.assertEqual(entry['Type'], 'Entry')
        self.assertEqual(entry['Email'], 'help@support.juno.com')
        self.assertEqual(entry['Name'], 'Juno')
        self.assertTrue(entry['Deleted'])

        entry = parse_entry(address_book)
        self.assertEqual(len(entry), 5)
        self.assertEqual(entry['Type'], 'Entry')
        self.assertEqual(entry['Email'], 'president@whitehouse.gov')
        self.assertEqual(entry['Address'],
                         ['1600 Pennsylvania Ave. NW', 'Washington DC, 20500'])
        self.assertFalse(entry['Deleted'])


    def test_parser(self):
        address_book = io.StringIO(TestParsing.entries)
        self.assertEqual(len([entry for entry in parser(address_book)]), 3)

if __name__ == '__main__':
    unittest.main()
