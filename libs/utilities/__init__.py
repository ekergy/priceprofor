# -*- coding: utf-8 -*-
#!/usr/bin/env python

__author__ = ("Hugo M. Marrao Rodrigues")
__version__ = "0.0.1"
__revision__ = "dev"

"""Ekergy's python projects utilities:

Contains a collection of utilities functions using for calendar and data type format.
Use docstring/doctest for usage:

"""

# imports:
from datetime import datetime, timedelta

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

        
