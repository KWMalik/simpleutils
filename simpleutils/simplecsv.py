"""
simple csv - set of simple utilities for handling csv

For all functions:
==================


some common keywords are listed for convenience. Only non-None
keywords are passed.

Convert to csv:
================

in general, can just use default settings, which are of form
convert_ABC_to_csv(lstofABC[,path) where 'ABC' is list or dict
and 'lstofABC' is a list of lists or dicts. 'path' is optional.

if no path given, defaults to inserting the time into the filename

read from csv:
==============

general format:
read_csv_to_ABC(path) -> ABC
where path is a path to a csv file and ABC is 'list' or 'dict'.
All keywords for python csv module are accepted, also possible to
specify a header row to get titles/keys, etc

All functions work with lists, dicts, or any object that works similarly
"""



import csv
from .simplesets import get_all_keys
from .simplefile import get_fileobject
import sys


def convert_dict_to_csv(
        *args, **kwargs):
    """ Deprecated, wrapper for simplecsv.write_dict"""
    return write_dict(*args, **kwargs)

def write_dict(
        lstofdicts,
        filename = None,
        header_row = None,
        fieldnames = None,
        dialect='excel',
        **kwargs):
    """Takes dict and converts to csv, see csv.DictWriter for more,
    ``**kwargs`` are passed on, default filename is
    :func:`~.simplefile.pretty_time`().csv e.g. call structure:
    ``csv.DictReader(csvfile[, fieldnames=None[, restkey=None[,
    restval=None[, dialect='excel'[, *args, **kwds]]]]])`` Use keyword
    arguments so you don't have to worry about position.

    :param lstofdicts: list of dicts to be converted to csv
    :param filename: path/fileobject/None for storing csv. See
        :func:`.simplefile.get_fileobject` for more.
    :param integer header_row: if given, pops that item in the list of
        of ``lstofdicts`` and uses it as headers (assumes it has a
        :meth:`keys` method.

    """
    # store defaults in kwargs
    f = get_fileobject(filename,mode='wb',ext='.csv')
    try:
        if fieldnames:
            # if fieldnames, store them
            names = fieldnames
        elif header_row:
            # sort keys in header_row for fieldnames
            names = sorted(lstofdicts[header_row].keys())
        else:
            try:
                # try to get fieldnames by getting all keys within lstofdicts
                names = sorted(list(get_all_keys(lstofdicts)))
                print("No fieldnames entered, getting all keys:\nKeys: {!r}".format(names))
            except Exception as inst:
                print("Couldn't grab all keys...probably won't work.")
                print("MESSAGE: {!r}".format(inst.MESSAGE))
                print("ARGS: {!r}".format(inst.args))
                names = lstofdicts[0].keys()
        # write fieldnames as first row
        csvwriter = csv.writer(f, **kwargs)
        csvwriter.writerow(names)
        # add fieldnames to kwargs for dictwriter
        kwargs['fieldnames'] = names
        csvDict = csv.DictWriter(f, **kwargs)
        sys.stdout.write("Wrote field names to first row. Continuing")
        i = 0
        for elem in lstofdicts:
            i += 1
            sys.stdout.write('.')
            csvDict.writerow(elem)
        print ("\nWrote {!d} items".format(i))
    except Exception as inst:
        print inst.message
        print inst.args
    finally:
        f.close()
        return filename

def convert_list_to_csv(*args, **kwargs):
    """ deprecated, wrapper for write_list"""
    return write_list(*args, **kwargs)

def write_list(
        lst,
        filename = None,
        header_row = 0,
        num_columns = None,
        delimiter = None,
        quotechar = None,
        quoting = None,
        dialect = 'excel',
        **kwargs):
    """Takes a list of data (generally list of list) and writes it to a
    file as a csv.

    :param header_row: specifies index where titles are located
        (becomes first row of csv)
    :param filename: default is ``pretty_time``, filename can also be a :class:`fileobject`
        (passed through :func:`~simplefile.get_fileobject`)

    All other args passed to :class:`~csv.writer`, args with None are written for convenience
    reminder.
    Default filename is pretty_time(), filename can also be a fileobject"""
    # store defaults in kwargs
    if delimiter is not None: kwargs['delimiter'] = delimiter
    if quotechar is not None: kwargs['quotechar'] = quotechar
    if quoting is not None: kwargs['quoting'] = quoting
    # get file object
    f = get_fileobject(filename,mode='wb',ext='.csv')
    # write with csvwriter
    try:
        mycsvwriter =  csv.writer(f,**kwargs)
        mycsvwriter.writerow(lst.pop(header_row))
        print "Writing rows",
        i = 0
        for elem in lst:
            mycsvwriter.writerow(elem)
            print ".",
            i += 1
        print("\nWrote {!d} rows.".format(i))
    finally:
        f.close()
        return filename

def read_csv_to_list(*args, **kwargs):
    """deprecated, wrapper for read_to_list"""
    return read_to_list(*args, **kwargs)

def read_to_list(
        path,
        dialect='excel',
        delimiter=None,
        quotechar = None,
        encoding = None,
        **kwargs):
    """ reads the csv at 'path' and outputs a list with all lines maintained
    (so, the column titles) any keywords for csvreader can be passed
    through if desired)"""
    # store defaults
    kwargs['dialect'] = dialect
    if delimiter is not None: kwargs['delimiter'] = delimiter
    if quotechar is not None: kwargs['quotechar'] = quotechar

    f = get_fileobject(path,mode='rb')

    try:
        mycsvreader = csv.reader(f,**kwargs)
        # if an encoding was specified, decodes the characters and return
        # otherwise just return using list generators
        if encoding:
            return [map(lambda y: y.decode(encoding),x) for x in mycsvreader]
        return [x for x in mycsvreader]
    finally:
        f.close()


def read_csv_to_dict(*args, **kwargs):
    """deprecated, wrapper for read_to_dict"""
    return read_to_dict(*args, **kwargs)
def read_to_dict(
        path,
        dialect='excel',
        delimiter=None,
        quotechar=None,
        encoding = None,
        **kwargs):
    """ reads the csv at 'path' and outputs a dict with keywords from the
    firstline (so, the column titles) any keywords for csvreader can be passed
    through if desired).
    path can be fileobject or system path
    Keywords are listed for convenience, only non-None are kept"""
    kwargs['dialect'] = dialect
    if not delimiter is None: kwargs['delimiter'] = delimiter
    if not quotechar is None: kwargs['quotechar'] = quotechar
    f = get_fileobject(path,mode='rb')
    try:
        mycsvreader = csv.DictReader(f,**kwargs)
        return [x for x in mycsvreader]
    finally:
        f.close()

