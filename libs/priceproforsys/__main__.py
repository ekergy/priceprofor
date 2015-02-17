"""Ekergy's omieinfosys CLI
>   Note:    usage must be preceded by 'python -m'. Example:
>   python -m priceprofor status

Usage:
  priceprofor [options] <operation> [<type>]
  priceprofor (-h | --help)
  priceprofor status
  priceprofor updatedb
  priceprofor ultimodiaprecios ( ES | MI | PT)

Options:
  -h --help             Show this screen.

"""
from docopt import docopt
from pprint import pprint


if __name__ == '__main__':
    args = docopt(__doc__, version='Calculator with docopt')
    try:
        from omieinfosys import status
        from omieinfosys.omieMercadoDiarioAggregations import volumenesanhoStudyDataMIBEL
        from .priceproforReports import ultimodiaprecios
        from . import populateMercadoDiarioMixEs
    except:
        print "Note: usage must be preceded by 'python -m' Example:\n\
              python -m priceprofor status"
        raise
    else:
        operation = args["<operation>"]
        optype = args["<type>"]
        if operation:
            if optype is None:
                if operation == "status":
                    pprint(status())
                    exit
                elif operation == "updatedb":

                    pprint(populateMercadoDiarioMixEs())
                    exit
            elif optype in ['ES','PT','MI']:
                if operation == "ultimodiaprecios":
                    pprint(ultimodiaprecios(optype))
                    exit
            else:
                print("-"*80)
                print("ERROR:: Invalid <operation> <type> combination. Check help below:")
                print("-"*80)
                print(__doc__)
        else:
            pass