# -*- coding: utf-8 -*-
"""
"""

import rpy2.robjects as robjects
# import datetime
from datetime import datetime, timedelta
import sys
import numpy as np
import pylab

from pymongo import Connection
from sys import exit
from operator import itemgetter

from rpy2.robjects import FloatVector
# sys.path.append("/home/david/workspace/electraPROFOR/MercadoElectrico/ExponentialSmoothing/")
sys.path.append("/home/david/workspace/electraPROFOR/ElectricityMarket/ExponentialSmoothing/")
# from testeHTES import variablesMWH
# from testeHWTES_robjects import variablesMWH
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, WeekdayLocator
from matplotlib.pyplot import figure, show, savefig
from matplotlib.pyplot import title
from pylab import text

# sys.path.append("/home/david/workspace/electraPROFOR/MercadoElectrico/PredictiveAnalysis/")
sys.path.append("/home/david/workspace/electraPROFOR/ElectricityMarket/PredictiveAnalysis/")
# from generalMethods import seleccionarDatosCSV
# from generalMethods import seleccionarDatosHoraCSV
# from validadorDeModelos import Validador
# from generalMethods import trazarGrafica

''' codigo necesario para importar el paquete arnn.R '''
f = file("/home/david/workspace/packagesR/arnn.R")
code = ''.join(f.readlines())
result = robjects.r(code)

def mainHWTES():
    """
    """
#     listDict = list()
# 
#     database = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario
#     horasDelDia = range(24)
#     for miHora in horasDelDia:
#         listWsort, listMsort, listTsort, listU8sort, listU9sort, listL8sort, listL9sort = hourHWTES(listDict, database, miHora)
# 
#     listPast2 = listWsort[(28-7)*24:] + listMsort[(28-7)*24:]
#     listFuture2 = listTsort[0:2*24] + listU8sort[0:2*24] + listU9sort[0:2*24] + listL8sort[0:2*24] + listL9sort[0:2*24]
#     listSort = listPast2 + listFuture2
# 
#     collection = database.modelosHWTES
#     mongodbHWTES(collection, listSort, listPast2, listFuture2)

def hourHWTES(listDict, database, miHora):
    """mainHWTES
    """

#     per = 28
#     currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
