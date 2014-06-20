# -*- coding: utf-8 -*-
'''
Created on 10/2013
@author: hmarrao
'''

from datetime import timedelta, datetime, tzinfo

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)

class GMT1(tzinfo):
    '''
    docstring
    '''

    def utcoffset(self, dt):
        '''
        '''
        return timedelta(hours=1) + self.dst(dt)
    def dst(self, dt):
        '''
        '''
       # DST starts last Sunday in March
        d = datetime(dt.year, 4, 1)   # ends last Sunday in October
        self.dston = d - timedelta(days=d.weekday() + 1)
        d = datetime(dt.year, 11, 1)
        self.dstoff = d - timedelta(days=d.weekday() + 1)
        if self.dston <=  dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

    def tzname(self,dt):
        return "GMT +1"

# needed definitions:
def deduceGDTType(value):
    '''
    if data represents a number the number should be the value
    otherwise a string
    '''
    try:
        if isinstance(value,float) or isinstance(value,int) or value.isdigit() or value.isnumeric():
            return 'number'
        else:
            raise
    except:
        return 'string'

def isNumber(value):
    '''
    Check if value is representing a number.
    '''
    def num(s):
        '''
        '''
        try:
            return int(s)
        except ValueError:
            return float(s)

    if isinstance(value, str) or isinstance(value, unicode):
        if value.isdigit():
            return num(value)
        elif unicode(value).isnumeric():
            return num(value)
        else:
            return value
    else:
        return value

def toGoogleDataTable(**kargs):
    # Control inputs
    try:
        resultadoGDT = {}
        OptionsAndValues = {'DataToTransform': None, 'FirstElementAreLabels': False}
        OptionsAndValues.update(**kargs)
        if not(isinstance(OptionsAndValues['DataToTransform'],list)):
            raise Exception('Oh no, I have no data to transform')
    except:
        raise
    else:

    # Assemble Cols
        if OptionsAndValues['FirstElementAreLabels']:
            Labels = OptionsAndValues['DataToTransform'].pop(0)
            resultadoGDT['cols'] = [{'label':label,'type': deduceGDTType(variable)} for (label, variable) in zip(Labels, OptionsAndValues['DataToTransform'][0])]
        else:
                resultadoGDT['cols']=[{'type': deduceGDTType(variable)} for variable in OptionsAndValues['DataToTransform'][0]]
    # Assemble Rows
        resultadoGDT['rows'] = [{'c':map(lambda x: {'v': isNumber(x)},tuplo)} for tuplo in OptionsAndValues['DataToTransform']]
    # Spit result
        return resultadoGDT

def str2datetime(value):
    '''
    takes 
    Using know parsers "%Y-%m-%dT%H:%MZ", "%Y-%m-%d"
    check if a string can represent one of the defined formats and return a datetime.datetime,
    else just return the value given.
    
    '''
    import datetime
    if value is None:
        return value
    else:
        if not isinstance(value, datetime.datetime):
            if isinstance(value, str) \
            or isinstance(value, unicode):
                try:
                    value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%MZ")
                except ValueError:
                    value = datetime.datetime.strptime(value, "%Y-%m-%d")
                finally:
                    if isinstance(value, datetime.datetime):
                        return value
                    else:
                        raise Exception('Error parsing sistema de medicion fechas')
        else:
            return value

def toD3jsDataFormat(*args,**kwargs):
    '''
    TODO: After studing the data driven document Lib we will construct a method similiar to the one done the
    toGoogleDataTable.
    '''
    pass
