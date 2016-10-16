# Juno Address Book Transformations

This project helps migrate data from the Juno Microsoft Windows email
client into formats that can be imported into other email
systems. Currently it supports the CSV file format used by Google Gmail.

## Gmail

To convert a Juno address book to a CSV file for importing to Gmail, run
the command `juno2gmail`. It has a `--help` option documenting its usage.

## The Juno address book file format

Juno keeps its address book in a text file, usually in
`C:\ProgramData\Juno\Isp\OER\User0000\addrbook.nv`. It consists of groups
of lines separated from each other by a blank line. Each line consists of a
key and a value, separated by a colon. Each group of lines starts with the
key `Type`, which has three values that I have observed:

* `Version`, the file format version. The examples that I have to work with
  have the additional key and value `Version:AB 0.3.0`.
* `Entry`, a single address book entry.
* `MList`, a mailing list.
