# -*- coding: utf-8 -*-

"""modelling system CLI

Usage:
modellingsys --arnn <dayahead>
modellingsys --hwtes <dayahead>
modellingsys --status

Arguments
<dayahead>        The dayahead to perform modelling and prediction

Options:
-h --help            Shows this help page
--arnn <dayahead>    Use arnn method to perform modelling and construct predictions
--hwtes <dayahead>   Use hwtes method to perform modelling and construct predictions
--status             Check last prediction made with configured modelling

"""

from pprint import pprint
from datetime import datetime

# importacion correcta aunque eclipse crea que es un error
from docopt import docopt

def execute_hwtes(dayahead):
    """perform modelling and construct predictions using hwtes Method
    devuelve:
    """
    try:
        from models import hwtes
        # result = hwtes.mainHWTES()
        hwtes.mainHWTES()
    except:
        raise
    else:
        print ''
#         print("execute_hwtes done")
#         pprint(result)

def execute_arnn(dayahead):
    """perform modelling and construct predictions using arnn Method
    """
    print("execute_arnn done")

def check_status():
    """perform modelling and construct predictions using hwtes Method
    """
    result = {'arnn':{"last_dayahead":datetime(2011,1,1)},'hwtes':{"last_dayahead":datetime(2011,1,1)}}
    pprint(result)

arguments = docopt(__doc__,version="alpha")

if arguments["--arnn"]:
    print arguments["--arnn"]
    execute_arnn(arguments["--arnn"])
if arguments["--hwtes"]:
    if arguments["--hwtes"] == "now":
        # print "\nel dayahead es hoy\n"
        execute_hwtes(arguments["--hwtes"])
    else:
        print "\nno encuentra la funcion\n"
if arguments["--status"]:
    check_status()
