# # -*- coding: utf-8 -*-
# #!/usr/bin/env python
"""Ekergy's reeinfosys CLI
>   Note:    usage must be preceded by 'python -m':
>   Example: python -m reeinfosys status

Usage:
  reeinfosys [options] <operation> [<type>]
  reeinfosys (-h | --help)
  reeinfosys updatedb

Arguments:
  operation:            Operation that you like to do. It can be:
            updatedb    Update data from the the omir ewb site into database.
                        Needs internet connection.

Options:
  -h --help             Show this screen.

"""
from docopt import docopt
from pprint import pprint

if __name__ == '__main__':
    args = docopt(__doc__, version='Calculator with docopt')
    try:
        from . import updatedb
    except:
        print "Note: usage must be preceded by 'python -m' Example:\n\
              python -m reeinfosys status"
    else:
        operation = args["<operation>"]
        optype = args["<type>"]
        if operation:
            if optype is None:
                if operation == "updatedb":
                    try:
                        updatedb()
                    except:
                        raise
                    else:
                        print "Done"
                    exit
            else:
                print("-"*80)
                print("ERROR:: Invalid <operation> <type> combination. Check help below:")
                print("-"*80)
                print(__doc__)
            if operation == "volumenes":
                if optype is not None:
                    pass
                else:
                    pprint(pprint(volumenesanhoStudyDataMIBEL()))
                    exit
            else:
                print("-"*80)
                print("ERROR:: Invalid <operation> <type> combination. Check help below:")
                print("-"*80)
                print(__doc__)

        else:
            pass