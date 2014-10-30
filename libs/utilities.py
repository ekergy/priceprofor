# -*- coding: utf-8 -*
'''
Created on 11/2013
@author: hmarrao & david
'''

from datetime import datetime, timedelta
from pymongo import Connection

# connectiondetails = dict(host=None)

''' LOCAL '''
# connecPrices = Connection(host=None).mercadodiario.precioses
# connecTechnologies = Connection(host=None).mercadodiario.tecnologiases

''' SERVIDOR '''
connecPrices = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.precioses
connecTechnologies = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.tecnologiases

CALENDARIONOLABORAL = {'2010': [datetime(2010,  1,  1),
                                datetime(2010,  1,  6),
                                datetime(2010,  4,  1),
                                datetime(2010,  4,  2),
                                datetime(2010,  4,  5),
                                datetime(2010,  5,  1),
                                datetime(2010, 10, 12),
                                datetime(2010, 11,  1),
                                datetime(2010, 12,  6),
                                datetime(2010, 12,  8),
                                datetime(2010, 12, 25),
                                ],
                       '2011': [datetime(2011,  1,  1),
                                datetime(2011,  1,  6),
                                datetime(2011,  4, 21),
                                datetime(2011,  4, 22),
                                datetime(2011,  4, 25),
                                datetime(2011,  5,  1),
                                datetime(2011, 10, 12),
                                datetime(2011, 11,  1),
                                datetime(2011, 12,  6),
                                datetime(2011, 12,  8),
                                datetime(2011, 12, 25)
                                ],
                       '2012': [datetime(2012,  1,  1),
                                datetime(2012,  1,  6),
                                datetime(2012,  4,  5),
                                datetime(2012,  4,  6),
                                datetime(2012,  4,  9),
                                datetime(2012,  5,  1),
                                datetime(2012, 10, 12),
                                datetime(2012, 11,  1),
                                datetime(2012, 12,  6),
                                datetime(2012, 12,  8),
                                datetime(2012, 12, 25)
                                ],
                       '2013': [datetime(2013,  1,  1),
                                datetime(2013,  1,  7),
                                datetime(2013,  4,  5),
                                datetime(2013,  4,  6),
                                datetime(2013,  4,  9),
                                datetime(2013,  5,  1),
                                datetime(2013, 10, 12),
                                datetime(2013, 11,  1),
                                datetime(2013, 12,  6),
                                datetime(2013, 12,  8),
                                datetime(2013, 12, 25)
                                ],
                       '2014': [datetime(2014,  1,  1),
                                datetime(2014,  1,  6),
                                datetime(2014,  4, 18),
                                datetime(2014,  5,  1),
                                datetime(2014,  8, 15),
                                datetime(2014, 11,  1),
                                datetime(2014, 12,  6),
                                datetime(2014, 12,  8),
                                datetime(2014, 12,  25),
                                ]
                      }

# from sys import path
# path.append('libs')
# from utilities import findLastDayDocumentPrice
# findLastDayDocumentPrice()
def findLastDayDocumentPrice():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ''' LOCAL '''
#     connec = Connection(host=None)
    ''' SERVIDOR '''
#     connec = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario')

    connec = Connection(host=connecPrices)
    collection = connec.mercadodiario.precioses

#     currentDT = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
#     cursor = collection.find({"fecha": {"$lte": currentDT}})
#     for element in cursor:
#         lastelement = element
#         # print element

#     cursor = collection.find().sort("fecha",-1).limit(1)
    cursor = collection.find().sort([("fecha",-1),("hora",-1)]).limit(1)
    for element in cursor:
        fecha = element['fecha']
        # fecha.replace(hour=0, minute=0, second=0, microsecond=0)
    del connec

#     return lastelement['fecha']
    return fecha

# from sys import path
# path.append('libs')
# from utilities import findLastDayDocumentTechnology
# findLastDayDocumentTechnology()
def findLastDayDocumentTechnology():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ''' LOCAL '''
#     connec = Connection(host=None)
    ''' SERVIDOR '''
#     connec = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario')

    connec = Connection(host=connecTechnologies)
    collection = connec.mercadodiario.tecnologiases

#     currentDT = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
#     cursor = collection.find({"fecha": {"$lte": currentDT}})
#     for element in cursor:
#         lastelement = element

#     cursor = collection.find().sort("fecha",-1).limit(1)
    cursor = collection.find().sort([("fecha",-1),("hora",-1)]).limit(1)
    for element in cursor:
        fecha = element['fecha']
        # fecha.replace(hour=0, minute=0, second=0, microsecond=0)
    del connec

#     return lastelement['fecha']
    return fecha

# from sys import path
# path.append('libs')
# from utilities import findLastDayDocumentPriceThree
# findLastDayDocumentPriceThree()
def findLastDayDocumentPriceThree():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ''' LOCAL '''
#     connec = Connection(host=None)
    ''' SERVIDOR '''
#     connec = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario')

    connec = Connection(host=connecPrices)
    collection = connec.mercadodiario.precioses

#     currentDT = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
#     fecha = currentDT - timedelta(3)
#     cursor = collection.find({"fecha": {"$lte": fecha}})
#     for element in cursor:
#         lastelement = element
#         # print element

#     cursor = collection.find().sort("fecha",-1).limit(1)
    cursor = collection.find().sort([("fecha",-1),("hora",-1)]).limit(1)
    for element in cursor:
        # print element
        fecha = element['fecha']
        # fecha.replace(hour=0, minute=0, second=0, microsecond=0)
        fecha = fecha - timedelta(3)
    del connec

#     return lastelement['fecha']
    return fecha

# from sys import path
# path.append('libs')
# from omelinfosys.utilities import cambiohoraverano
# cambiohoraverano(2014)
def cambiohoraverano(anho=None):
    '''
    cambiohoraverano(anho) -> datetime.datetime

    doc

    >>> cambiohoraverano(2010)
    datetime.datetime(2010, 3, 28, 0, 0)

    >>> cambiohoraverano(2011)
    datetime.datetime(2011, 3, 27, 0, 0)

    >>> cambiohoraverano(2012)
    datetime.datetime(2012, 3, 25, 0, 0)

    >>> cambiohoraverano(2013)
    datetime.datetime(2013, 3, 31, 0, 0)

    >>> cambiohoraverano(123)
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1254, in __run
        compileflags, 1) in test.globs
      File "<doctest utilities.cambiohoraverano[4]>", line 1, in <module>
        cambiohoraverano(123)
      File "utilities.py", line 41, in cambiohoraverano
        deseado. <int> con 4 dijitos.')
    Exception: La variable de entrada no tiene el formato deseado. \
<int> con 4 dijitos.

    >>> cambiohoraverano('2013')
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1254, in __run
        compileflags, 1) in test.globs
      File "<doctest utilities.cambiohoraverano[5]>", line 1, in <module>
        cambiohoraverano('2013')
      File "utilities.py", line 38, in cambiohoraverano
        raise Exception('La variable de entrada no es del tipo correcto.')
    Exception: La variable de entrada no es del tipo correcto.
    '''
    try:
        if not isinstance(anho, int):
            raise Exception('La variable de entrada no es del tipo correcto')
        elif len(anho.__str__()) != 4:
            raise Exception('La variable de entrada no tiene el formato deseado <int> con 4 dijitos')
    except:
        raise
    fechacandidato = datetime(anho, 3, 31)
    resultdate = None
    while not resultdate:
        if fechacandidato.weekday() == 6:
            resultdate = fechacandidato
        else:
            fechacandidato = fechacandidato - timedelta(1)
    return resultdate

# from sys import path
# path.append('libs')
# from omelinfosys.utilities import cambiohorainvierno
# cambiohorainvierno(2014)
def cambiohorainvierno(anho=None):
    '''
    cambiohorainvierno(anho) -> datetime.datetime
    doctest

    >>> cambiohorainvierno(2010)
    datetime.datetime(2010, 10, 31, 0, 0)

    >>> cambiohorainvierno(2011)
    datetime.datetime(2011, 10, 30, 0, 0)

    >>> cambiohorainvierno(2012)
    datetime.datetime(2012, 10, 28, 0, 0)

    >>> cambiohorainvierno(2013)
    datetime.datetime(2013, 10, 27, 0, 0)

    >>> cambiohorainvierno(123)
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1254, in __run
        compileflags, 1) in test.globs
      File "<doctest utilities.cambiohoraverano[4]>", line 1, in <module>
        cambiohoraverano(123)
      File "utilities.py", line 41, in cambiohoraverano
        deseado. <int> con 4 dijitos.')
    Exception: La variable de entrada no tiene el formato deseado. \
<int> con 4 dijitos.

    >>> cambiohorainvierno('2013')
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1254, in __run
        compileflags, 1) in test.globs
      File "<doctest utilities.cambiohoraverano[5]>", line 1, in <module>
        cambiohoraverano('2013')
      File "utilities.py", line 38, in cambiohoraverano
        raise Exception('La variable de entrada no es del tipo correcto.')
    Exception: La variable de entrada no es del tipo correcto.

    '''
    try:
        if not isinstance(anho, int):
            raise Exception('La variable de entrada no es del tipo correcto.')
        elif len(anho.__str__()) != 4:
            raise Exception('La variable de entrada no tiene el formato deseado <int> con 4 dijitos')
    except:
        raise
    fechacandidato = datetime(anho, 10, 31)
    resultdate = None
    while not resultdate:
        if fechacandidato.weekday() == 6:
            resultdate = fechacandidato
        else:
            fechacandidato = fechacandidato - timedelta(1)
    return resultdate

def diasconcambiodehora(StartDate,EndDate):
    '''
    diasconcambiodehora(datetime.datetime,datetime.datetime)
    doctest

    >>> diasconcambiodehora(datetime.datetime(2010,1,1),datetime.datetime(2013,1,1))
    {'DiasCambioDeHoraAverano': [datetime.datetime(2010, 3, 28, 0, 0), datetime.datetime(2011, 3, 27, 0, 0), datetime.datetime(2012, 3, 25, 0, 0)], 'DiasCambioDeHoraAinvierno': [datetime.datetime(2010, 10, 31, 0, 0), datetime.datetime(2011, 10, 30, 0, 0), datetime.datetime(2012, 10, 28, 0, 0)]}
    
    
    '''
    DiasCambioDeHoraAverano = [];
    DiasCambioDeHoraAinvierno = [];
    for i in range(EndDate.year - StartDate.year +1):
        candidatoInvierno = cambiohorainvierno(StartDate.year+i)
        candidatoVerano = cambiohoraverano(StartDate.year+i)
        if EndDate > candidatoVerano > StartDate:
            DiasCambioDeHoraAverano.append(candidatoVerano)
        if EndDate > candidatoInvierno > StartDate:
            DiasCambioDeHoraAinvierno.append(candidatoInvierno)
    return {'DiasCambioDeHoraAverano':DiasCambioDeHoraAverano,
            'DiasCambioDeHoraAinvierno':DiasCambioDeHoraAinvierno}

def stringtofloat(string=str(), groupsep='.', decimalsep=',', decimalplaces=2):
    '''
    stringtofloat('string',kwargs*) -> <float>
    doctest

    >>> stringtofloat('1')
    1.0

    >>> stringtofloat('10,0')
    10.0

    >>> stringtofloat('1.000,54')
    1000.54

    >>> stringtofloat(1)
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1254, in __run
        compileflags, 1) in test.globs
      File "<doctest utilities.stringtofloat[3]>", line 1, in <module>
        stringtofloat(1)
      File "utilities.py", line 149, in stringtofloat
        raise Exception('El argumento de entrada no es del tipo <str>.')
    Exception: El argumento de entrada no es del tipo <str>.

    >>> stringtofloat('1.000,00')
    1000.0

    >>> stringtofloat('1,000.00')
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1254, in __run
        compileflags, 1) in test.globs
      File "<doctest utilities.stringtofloat[5]>", line 1, in <module>
        stringtofloat('1,000.00')
      File "utilities.py", line 171, in stringtofloat
        aplican a este numero.')
    Exception: Los separadores de grupo y de decimales no se aplican a este \
numero.

    >>> stringtofloat('1,000.00',groupsep=',',decimalsep='.')
    1000.0


    '''
    try:
        if not isinstance(string, str):
            raise Exception('El argumento de entrada no es del tipo <str>.')
        groupseposition = string.find(groupsep)
        decimalseposition = string.find(decimalsep)
        if (groupseposition > decimalseposition):
            if not (groupseposition == 0 and decimalseposition == -1):
                raise Exception('Los separadores de grupo y de decimales no se aplican a este numero')
    except:
        raise
    else:
        if string == '':
            result = float(0)
        else:
            string = string.replace(groupsep, '')
            string = string.replace(decimalsep, '.')
            result = round(float(string), decimalplaces)
        return result

def floattostring(number=float(), groupsep='.', decimalsep=',', decimalplaces=2):
    '''
    floattostring(float,kwargs*) -> <str>
    '''
    if number == float():
        result = round(float(0), decimalplaces)
    else:
        result = str(round(number, decimalplaces))
        result = result.replace(groupsep, '')
        result = result.replace('.', decimalsep)
    return result

def unicodetodecimal(ustr):
    '''
    unicodetodecimal(u'str')-> <float>
    '''
    try:
        from decimal import Decimal
        if (not isinstance(ustr, unicode)) and \
           (not isinstance(ustr, str)):
            raise Exception('Check the data type')
    except:
        raise
    else:
    # stringLength = len(ustr)
        commaposition = ustr.find(',')
        dotposition = ustr.find('.')
        # Check if we have comma decimal seperator
        if dotposition == -1 and commaposition == -1:
            return int(ustr)
        if dotposition > commaposition:
            ustr = ustr.replace(',', '')
        elif dotposition <= commaposition:
            ustr = ustr.replace('.', '')
            ustr = ustr.replace(',', '.')
        else:
            ustr = ustr.replace('.', '')
            ustr = ustr.replace(',', '')
        return float(str(Decimal(ustr)))

# from sys import path
# path.append('libs')
# from datetime import datetime
# fecha = datetime(2014,1,1)
# from omelinfosys.utilities import eslaborable
# eslaborable(fecha)
def eslaborable(dia=None):
    '''
    Esta funcion devuelve True si el "Dia" que pasamos como parametro
    es laborable y definimos dia laborable como aquel que no es un dia
    festivo ni es un domingo.
    '''
    dia = datetime(dia.year,dia.month,dia.day)
    if dia in CALENDARIONOLABORAL[str(dia.year)] or dia.weekday() == 6:
        # return False
        return 0
    else:
        # return True
        return 1

def aquetemporadapertenece(dia=None):
    '''
    aquetemporadapertenence(datetime.datetime) -> n in {0,1}
    Esta funcion devuelve la temporada definida de la siguiente forma:
        0 si es temporada de invierno
        1 si es temporada de verano
    '''
    try:
        if not isinstance(dia, datetime):
            raise Exception('Revisa el dato de entrada')
        else:
            anho = dia.year
            cambioatemporadainvierno = cambiohorainvierno(anho)
            cambioatemporadaverano = cambiohoraverano(anho)
    except:
        raise
    else:
        if dia >= cambioatemporadaverano and dia < cambioatemporadainvierno:
            return 1
        else:
            return 0

def aqueestacionpertenece(dia=None):
    '''
    aqueestacionpertenence(<datetime.datetime>) -> n in {0,1,2,3}
    Esta funcion devuelve la estacion definida de la siguiente forma:
        0 si es estacion de invierno
        1 si es estacion de primavera
        2 si es estacion de verano
        3 si es estacion de otonho
    '''
    try:
        if not isinstance(dia, datetime):
            raise Exception('Revisa el dato de entrada')
        else:
            anho = dia.year
            cambioainvierno = datetime(anho, 12, 21)
            cambioaprimavera = datetime(anho, 3, 20)
            cambioaverano = datetime(anho, 6, 21)
            cambioaotonho = datetime(anho, 9, 21)
    except:
        raise
    else:
        if dia >= cambioaprimavera and dia < cambioaverano:
            return 1
        elif dia >= cambioaverano and dia < cambioaotonho:
            return 2
        elif dia >= cambioaotonho and dia < cambioainvierno:
            return 3
        else:
            return 0

def validafecha(fecha):
    '''
    valida la fecha que se introduce.
    doctest

    >>> validafecha(datetime.datetime(2012,12,1))
    >>>
    
    >>> validafecha(datetime.datetime.now() + datetime.timedelta(days=2))
    Traceback (most recent call last):
        File "/usr/lib/python2.7/doctest.py", line 1254, in __run
            compileflags, 1) in test.globs
        File "<doctest webdatascraping._validafecha[0]>", line 1, in <module>
            _validafecha(datetime.datetime(2013,12,1))
        File "webdatascraping.py", line 34, in _validafecha
            raise Exception('La fecha selecionada es postrior de la de hoy. No tiene datos disponibles en la web.')
    Exception: La fecha selecionada es postrior de la de hoy. No tiene datos disponibles en la web.
    
    '''
    try:
        if not isinstance(fecha, datetime):
            raise Exception('El formato fecha no es del tipo correcto.')
        fecha.replace(hour = 11)
#         if datetime.now() < fecha:
        ''' en desarrollo para dayahead '''
        if datetime.now() + timedelta(1) < fecha:
            raise Exception('La fecha selecionada es posterior a hoy. No hay datos disponibles en la web.')
        fecha.replace(hour = 0)
    except:
        raise
    else:
        return

def esiosreeurl(fecha=None, xmlid=None):
    URL_ESIOS_REE = "http://www.esios.ree.es/Solicitar/"
    ESIOSREEURLSXMLIDS = ["preveol_DD",
                          "demanda_aux",
                          "BAL_PBF_DD",
                          "CBF_PBF_DD",
                          "DEM_PBF_DD",
                          "MD_EGEST_DD"]
    '''
    Esta funcion devuelve la url del xml que contiene los datos
    disponibles en www.esios.ree.es devuelve la url con los datos
    doctest

    >>> esiosreeurl(datetime.datetime(2012,12,10),'preveol_DD')
    'http://www.esios.ree.es/Solicitar/preveol_DD_20121210.xml'

    >>> esiosreeurl(datetime.datetime(2012,12,10),u'demanda_aux')
    'http://www.esios.ree.es/Solicitar/demanda_aux_20121210.xml'

    >>> esiosreeurl(datetime.datetime(2012,12,10),'xmlid')
    Traceback (most recent call last):
        File "/usr/lib/python2.7/doctest.py", line 1254, in __run
            compileflags, 1) in test.globs
        File "<doctest webdatascraping.esiosreeurl[0]>", line 1, in <module>
            esiosreeurl(datetime.datetime(2012,12,10),'xmlid')
        File "webdatascraping.py", line 147, in esiosreeurl
            raise Exception('No se sabe parsear el xmlid dado.')
    Exception: No se sabe parsear el xmlid dado.

    >>> esiosreeurl(datetime.datetime.now() + datetime.timedelta(days=2),'xmlid')
    Traceback (most recent call last):
        File "/usr/lib/python2.7/doctest.py", line 1254, in __run
            compileflags, 1) in test.globs
        File "<doctest webdatascraping.esiosreeurl[0]>", line 1, in <module>
            esiosreeurl(datetime.datetime.now() + datetime.timedelta(days=2),'xmlid')
        File "webdatascraping.py", line 130, in esiosreeurl
            _validafecha(fecha)
        File "webdatascraping.py", line 37, in _validafecha
            raise Exception('La fecha selecionada es postrior de la de hoy. No tiene datos disponibles en la web.')
    Exception: La fecha selecionada es postrior de la de hoy. No tiene datos disponibles en la web.
    '''
    try:
        validafecha(fecha)
        if (not isinstance(xmlid, str)) and (not isinstance(xmlid, unicode)):
            raise Exception('xmlid no es del tipo definido.')
        xmlid = str(xmlid)
        if not xmlid in ESIOSREEURLSXMLIDS:
            raise Exception('No se sabe parsear el xmlid dado.')
    except:
        raise
    else:
        urlpart1 = URL_ESIOS_REE
        urlpart4 = ".xml"
        urlpart3 = fecha.strftime("%Y%m%d")
        urlpart2 = xmlid + "_"
        url = urlpart1 + urlpart2 + urlpart3 + urlpart4
        # print url
        return url

def omiepreciosurl(fecha):
    '''
    doctest

    >>> omiepreciosurl(datetime.datetime(2012,10,10))
    'http://www.omie.es/datosPub/marginalpdbc/marginalpdbc_20121010.1'
    >>> omiepreciosurl(datetime.datetime.now() + datetime.timedelta(days=2))
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "webdatascraping.py", line 46, in omiepreciosesurl
            _validafecha(fecha)
        File "webdatascraping.py", line 37, in _validafecha
            raise Exception('La fecha selecionada es postrior de la de hoy. No tiene datos disponibles en la web.')
    Exception: La fecha selecionada es postrior de la de hoy. No tiene datos disponibles en la web.
    '''
    URL_OMIE_DATOSPUB = 'http://www.omie.es/datosPub'
    URL_OMIE_PRECIOMARGINAL = URL_OMIE_DATOSPUB + '/' + 'marginalpdbc/marginalpdbc_'
    URL_FIN = '.1'
    try:
        validafecha(fecha)
#         currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
#         tomorrow = currentDate + timedelta(1)
#         if (fecha == tomorrow):
#             if datetime.now().hour <= 13 and datetime.now().minute <= 14:
#                 raise Exception('Hasta las 13:15 del dia actual no estan disponibles los precios del Day Ahead')
#             else:
#                 pass
#         else:
#             validafecha(fecha)
    except:
        raise
    else:
        # preform transformation
        fechaURL= fecha.strftime("%Y%m%d")
        # return result as a str.
        return URL_OMIE_PRECIOMARGINAL+fechaURL+URL_FIN

def omieproduccionurl(fecha):
    '''
    doctest
    '''
    URL_OMIE_DATOSPUB = 'http://www.omie.es/datosPub'
    URL_OMIE_PRODUCCION = URL_OMIE_DATOSPUB + '/' + 'pdbc_stota/pdbc_stota_'
    URL_FIN = '.1'
    try:
        validafecha(fecha)
    except:
        raise
    else:
        # preform transformation
        fechaURL= fecha.strftime("%Y%m%d")
        # return result as a str.
        return URL_OMIE_PRODUCCION+fechaURL+URL_FIN
