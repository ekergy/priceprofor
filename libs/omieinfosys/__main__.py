# # -*- coding: utf-8 -*-
# #!/usr/bin/env python
"""Ekergy's omieinfosys CLI
>   Note:    usage must be preceded by 'python -m':
>   Example: python -m omieinfosys status

Usage:
  omieinfosys <operation> [<type>] [options]
  omieinfosys (-h | --help)
  omieinfosys status
  omieinfosys updatedb
  omieinfosys reportday --day "2015-01-01"
  omieinfosys reportday --day "2015-01-01" --market "PT"
  omieinfosys reportdaytech --day="2015-01-01" --market="PT"
  omieinfosys reportdaytech --market="PT"
  omieinfosys reportdaytech --day="2015-01-01"
  omieinfosys reportdaytech
  omieinfosys aggregations <type>
  omieinfosys datafiles

Arguments:
  operation:            Operation that you like to do. It can be:
            status      Give the current database status summary.
            updatedb    Update data from the the omir ewb site into database.
                        Needs internet connection.
            updatedb
            reportday   Gives a summary of the given day. if no day is given the last day available
                        is given.
            reportdaytech
                        Gives a summary of the given day. if no day is given the last day available
                        is given.
            volumenes   Give the current Volumns of current data in database
                        in MWh and EURs.
            datafiles   this operation generates data files for each market and each year. 

  type:                 The operation type. Only valid for aggregations.
                        Types can be:
        volumenesanho           aggregado de la produccion por tecnologias anho.
        volumenesmes            aggregado de la produccion por tecnologias anho y mes.
        volumenessemanas        aggregado de la produccion por tecnologias anho y semana del ano.
        volumenesdiassemanas    aggregado de la produccion por tecnologias anho y dia de la semana.





Options:
  -h --help             Show this screen.
  --check               Some check
  --preparedatabase     instert data into database. 
                            Do this only if you database is empty 
                            or this is the first run 
                            of the omieinfosys package.
  --agg VALUE           Gives Aggregations on Study Data Collection:
                            Possible VALUEs are:
                            volumenes     volumenes de EUR y MWh por año
  --day=DAY           Input for report day operation
  --market=MARKET     Select market to process: "PT", "ES" or "MI"

"""
from docopt import docopt
from pprint import pprint
import datetime
import sys

if __name__ == '__main__':
    args = docopt(__doc__, version="Ekergy's omieinfosys CLI zero alpha")

    try:
        from . import status
        from . import updatedb
        from omieMercadoDiarioAggregations import volumenesanhoStudyDataMIBEL
        from omieMercadoDiarioReports import ReportDay, ReportDayTecnologies
        from omieDataFilesGenerators import generateAllOMIEwebdatafiles
        operation = args["<operation>"]
        optype = args["<type>"]
    except:
        print "Note: usage must be preceded by 'python -m' Example:\n\
              python -m omieinfosys status"
        raise
    else:
        #if operation:
        if operation == "datafiles":    
            generateAllOMIEwebdatafiles()
        if args["reportday"]:
            if not args["--day"]:
                pprint(dict(ReportDay().items()),indent=0)
                sys.exit()
            else:
                day = datetime.datetime.strptime(request.json['day'],'%Y-%m-%d')
                #TODO: parse datetime and complete report
                pprint(ReportDay(day=day))
                sys.exit()
        if args["reportdaytech"]:
            day = None
            market = "MI"
            if args["--day"]:
                day = datetime.datetime.strptime(args["--day"],'%Y-%m-%d')
            if args["--market"]:
                market = args["--market"]
            pprint(dict(ReportDayTecnologies(day=day,market=market).items()),indent=0)
            sys.exit()
        if optype is None:
            if operation == "status":
                pprint(status())
                sys.exit()
            elif operation == "updatedb":
                try:
                    updatedb()
                except:
                    raise
                else:
                    print "Done"
                sys.exit()
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

        # else:
        #     sys.exit()

#         # if args["--agg"]:
#         #     if args["--agg"] == "volumenes":
#         #         pprint(volumenesanhoStudyDataMIBEL())
#         #     exit
        
#         # if args["--check"]:
#         #     print args["--check"]
#         # else:
#         #     pass
#         # print functions[args['<operation>']](int(args['<num1>']), int(args['<num2>']))

# # functions = {
#     #     'add': lambda num1, num2: num1 + num2,
#     #     'subtract': lambda num1, num2: num1 - num2,
#     #     'multiply': lambda num1, num2: num1 * num2,
#     #     'divide': lambda num1, num2: num1 / num2
#     # }

# # # -*- coding: utf-8 -*-
# # #!/usr/bin/env python

# # """priceprofor zero alpha CLI

# # Usage:
# #   python omieinfosys [Options]

# # Options:
# #   -h --help            show this help message and exit
# #   --version            show version and exit
# #   --check              check for requirements in the current python
# #   fullstatus         prints out the full status of the mongocollections


# # """

# #   # -v --verbose         print status messages
# #   # -q --quiet           report only file names
# #   # -r --repeat          show all occurrences of the same error
# #   # --exclude=PATTERNS   exclude files or directories which match these comma
# #   #                      separated patterns [default: .svn,CVS,.bzr,.hg,.git]
# #   # -f NAME --file=NAME  when parsing directories, only check filenames matching
# #   #                      these comma separated patterns [default: *.py]
# #   # --select=ERRORS      select errors and warnings (e.g. E,W6)
# #   # --ignore=ERRORS      skip errors and warnings (e.g. E4,W)
# #   # --show-source        show source code for each error
# #   # --statistics         count errors and warnings
# #   # --count              print total number of errors and warnings to standard
# #   #                      error and set exit code to 1 if total is not null
# #   # --benchmark          measure processing speed
# #   # --testsuite=DIR      run regression tests from dir
# #   # --doctest            run doctest on myself

# # from docopt import docopt
# # from pprint import pprint

# # def main(arguments):
# #     # print("----------")
# #     # print("a printout of the command line options as parsed by docopt:")
# #     # #print(options)
# #     # print("----------")
# #     if options["--check"]:
# #         return "try to import things"
# #     # if options["--notrequired"]:
# #     #     print("required option selected")
# #     # if options["--computer"]:
# #     #     print("computer name: {computer}".format(computer=options["COMPUTER"]))
# #     # if options["--network"]:
# #     #     print("computer name: {network}".format(network=options["<network>"]))
# #     # else:
# #     #     print("no options")


# # print "----------------------------"
# # arguments = docopt(__doc__, version='zeroalpha')
# # if arguments["fullstatus"]:
# #     print("this is the full status of the program")
# # exit()
# # #print arguments # DEBUG
# # # print main(arguments)

# # # print(type(arguments))
# # # pprint(arguments)
# # # main(arguments)
# # #print(arguments)


