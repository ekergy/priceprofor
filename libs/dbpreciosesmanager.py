# -*- coding: utf-8 -*-
'''
Created on 05/2014
@author: hmarrao & david
'''

'''
Cuenta en mongolab y cambiar URL de base de datos precioses a mi cuenta con el nombre actual
'''

from os import path
direc = path.abspath(__file__)
machine = direc[direc.find("e")+2:direc.find("w")-1]

from pymongo import Connection
from datetime import datetime, timedelta, date
# from utilities import validafecha, omiepreciosurl, stringtofloat, cambiohoraverano, cambiohorainvierno
from utilities import omiepreciosurl, cambiohoraverano, cambiohorainvierno
# from utilities import stringtofloat
from urllib2 import urlopen
# from csv import reader
from omelinfosys.omelhandlers import PreciosMibelHandler

# from sys import path
# path.append('libs')
# # from datetime import datetime
# # startDT = datetime(2014,1,1)
# # endDT = datetime(2014,2,1)
# from dbpreciosesmanager import populatePrecios
# populatePrecios()
# # populatePrecios(startDT,endDT)
def populatePrecios(startDate=None, endDate=None):
    '''
    populatePrecios por si solo gestiona la actualizacion de base de datos en LOCAL o SERVIDOR
    '''
    try:
        ONEDAY = timedelta(1)
        if startDate == None:
            startDate = findLastPriceDocument()
        if endDate == None:
            currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
            # endDate = currentDate - timedelta(3)
            ''' no se seleccionan los precios "day ahead" de mañana publicados hoy a las 13:00 '''
            endDate = currentDate
    except:
        raise
    else:
        listCHV = list()
        listCHI = list()
        for indi in range(endDate.year - startDate.year + 1):
            fechaCHV = cambiohoraverano(startDate.year + indi)
            fechaCHI = cambiohorainvierno(startDate.year + indi)
            listCHV.append(fechaCHV)
            listCHI.append(fechaCHI)

        iterDate = startDate
        while (endDate >= iterDate):
            print iterDate.date()
            ins = DBPreciosES()
            ins.fecha = iterDate
            priceDay = getpreciosesfromweb(ins.fecha)['PreciosES']

            if len(priceDay) == 24:
                pass
            elif len(priceDay) == 23:
                horaCHV = 3
                priceDay.insert(horaCHV,priceDay[horaCHV-1])
            elif len(priceDay) == 25:
                horaCHI = 3
                priceDay.pop(horaCHI)

            for i in range(len(priceDay)):
                ins.hora = i
                ins.priceHour = priceDay[ins.hora]
                ins.updatedbprecioses()
            del ins
            iterDate += ONEDAY

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import findLastPriceDocument
# findLastPriceDocument()
def findLastPriceDocument():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ins = DBPreciosES()
    collection = ins.get_connection()
    currentDT = datetime.now()
    cursor = collection.find({"fecha": {"$lte": currentDT}})
    for element in cursor:
        lastelement = element
    return lastelement['fecha']

# from sys import path
# path.append('libs')
# from datetime import datetime
# fecha = datetime(2014,1,1)
# from omelinfosys.dbpreciosesmanager import getpreciosesfromweb
# getpreciosesfromweb(fecha)
def getpreciosesfromweb(fecha):
        '''
        This is the main method so the usage of PreciosMibelHandler is more strainfoward.
        '''
        try:
            ''' Se comenta validafecha dado que si existen los precios de dia de mañana '''
            # validafecha(fecha)
            toparsePRECIOS = urlopen(omiepreciosurl(fecha))
        except:
            raise
        else:
            Precios = PreciosMibelHandler(toparsePRECIOS)
            return {"PreciosES": Precios.precioses}
        #finally:
        #    del toparsePRECIOS,Precios



# from sys import path
# path.append('libs')
# from omelinfosys.dbpreciosesmanager import mercadodiarioD3
# mercadodiarioD3()
def mercadodiarioD3():
    '''
    '''

# from pymongo import Connection
# collection = Connection().mercadodiario.precioses

# cursor = collection.find()
# for element in cursor:
#     print element

# from datetime import datetime
# cursor = collection.find({"fecha": {"$gte": datetime(2014,3,1), "$lte": datetime(2014,3,2)} })
# for element in cursor:
#     print element

    ins = DBPreciosES()
    collection = ins.get_connection()
    # cursor = collection.find({u'fecha': datetime(2014, 1, 1)})
    # cursor = collection.find({"fecha": {"$gte": datetime(2014,1,1), "$lte": datetime(2014,4,30)} })
    cursor = collection.find({"fecha": {"$gte": datetime(2011,1,1), "$lte": datetime(2014,4,30)} })
    # cursor = collection.find()
    listD3 = list()
    for element in cursor:
        listD3.append(element)

    listCSV = list()
    for element in listD3:
        newDT = datetime(element['fecha'].year, element['fecha'].month, element['fecha'].day, element['hora'])
        # listCSV.append([element['fecha'],element['hora'],element['PreciosES']])
        listCSV.append([newDT,element['hora'],element['PreciosES']])

    thelist = listCSV
    rutaData = '/home/'+machine+'/workspace/profordes/data/mercadodiario/'
    # f = open(rutaData+"sp500.txt","w")
    f = open(rutaData+"sp500.csv","w")
    thefile = f
    thefile.write("date,price\n")
    # thefile.write("datetime,hour,price\n")
    for item in thelist:
        thefile.write("%s" % item[0])
        # thefile.write(",")
        # thefile.write("%s" %item[1])
        thefile.write(",")
        thefile.write("%s\n" %item[2])
    f.close()
#     return listD3

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import preciosDiarios
# preciosDiarios()
def preciosDiarios(fechayhora=None):
    '''
    notar que en el proyecto "profordes" dentro del script con el mismo nombre que este
    esta implementado el metodo "populatePrecios" que actualiza esta misma base de datos

    transformar fechayhora en un date de mongo.

    '''
    if fechayhora is None:
        fechayhora = None
    else:
        fechayhora = datetime(fechayhora.year,fechayhora.month,fechayhora.day,)

    dic = dict()
    priceList = list()
    nameList = [ 'HORA', 'PRECIO' ]
    hourList = ['00-01','01-02','02-03','03-04','04-05','05-06','06-07','07-08','08-09','09-10','10-11','11-12',
                '12-13','13-14','14-15','15-16','16-17','17-18','18-19','19-20','20-21','21-22','22-23','23-24']
    messageList = ''
    # noneList = [None, None]
    # noneList = [0, 0]
    noneList = []

    ''' LOCAL '''
#     collection = Connection(host=None).mercadodiario.precioses
    ''' SERVIDOR '''
    collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.precioses

    cursor = collection.find({ "fecha": {"$in": [fechayhora]} })
    if fechayhora == None:
        priceList.append(noneList)
        messageList = 'Se debe seleccionar una fecha del calendario'
    elif  cursor.count() == 0:
        priceList.append(noneList)
        messageList = 'No hay datos de la fecha seleccionada'
    else:
        priceList.append(nameList)
        indice = 0
        for element in cursor:
                vectorList = [ hourList[indice], element['PreciosES']  ]
                priceList.append(vectorList)
                indice = indice + 1
    dic['fecha'] = fechayhora
    dic['precios'] = priceList
    dic['mensaje'] = messageList
    return dic

# from sys import path
# path.append('libs')
# from dbtecnologiasesmanager import tecnologiasDiarias
# tecnologiasDiarias()
def tecnologiasDiarias(fecha=None, hora=None):
    '''
    '''
#     ''' fecha dummy '''
#     fecha = datetime(2014,5,20)
    dic = dict()
    technologyList = list()
    nameList = [ 'HORA',
                'NUCLEAR', 'REGIMEN_ESPECIAL', 'HIDRAULICA_CONVENCIONAL',
                'CARBON', 'CICLO_COMBINADO', 'FUEL_GAS' ]
    hourList = ['00-01','01-02','02-03','03-04','04-05','05-06','06-07','07-08','08-09','09-10','10-11','11-12',
                '12-13','13-14','14-15','15-16','16-17','17-18','18-19','19-20','20-21','21-22','22-23','23-24']
    messageList = ''
    noneList = []

    ''' LOCAL '''
#     collection = Connection(host=None).OMIEData.OMIEStudyData
    ''' SERVIDOR '''
    collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.tecnologiases

    ''' un dia '''
    cursor = collection.find({ "fecha": {"$in": [fecha]} })
    ''' una hora '''
#     cursor = collection.find({ "fecha": {"$in": [fecha]}, "hora": {"$in": [0]} })

    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)

    if fecha == None:
        technologyList.append(noneList)
        messageList = 'Se debe seleccionar una fecha del calendario'
    elif  fecha == currentDate:
        technologyList.append(noneList)
        messageList = 'Existen datos de tecnologias 3 dias atras'
    elif  fecha == currentDate - timedelta(1):
        technologyList.append(noneList)
        messageList = 'Existen datos de tecnologias 2 dias atras'
    elif  fecha == currentDate - timedelta(2):
        technologyList.append(noneList)
        messageList = 'Existen datos de tecnologias 1 dia atras'
    elif  cursor.count() == 0:
        technologyList.append(noneList)
        messageList = 'No hay datos de la fecha seleccionada'
    else:
        technologyList.append(nameList)
        indice = 0
        for element in cursor:
            vectorList = [ hourList[indice],
                           element['NUCLEAR'], element['REGIMEN_ESPECIAL'], element['HIDRAULICA_CONVENCIONAL'],
                           element['CARBON'], element['CICLO_COMBINADO'], element['FUEL_GAS']  ]
            technologyList.append(vectorList)
            indice = indice + 1
    dic['fecha'] = fecha
    dic['tecnologias'] = technologyList
    dic['mensaje'] = messageList
#     print dic
#     print dic['tecnologias']
#     print dic['tecnologias'][0]
#     print dic['tecnologias'][1]
    return dic

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import priceAppli
# priceAppli()
def priceAppli():
    '''
    Proporciona un json con vector precios y horas precio maximo/minimo (3 ultimos dias)
    '''

    def maxList(priceList):
        '''
        '''
        maxIndexList = list()
        for index in range(len(priceList)):
            if priceList[index] == max(priceList):
                maxValue = priceList[index]
                maxIndexList.append(index)
        return {'precio': maxValue, 'hora': maxIndexList}

    def minList(priceList):
        '''
        '''
        minIndexList = list()
        for index in range(len(priceList)):
            if priceList[index] == min(priceList):
                minValue = priceList[index]
                minIndexList.append(index)
        return {'precio': minValue, 'hora': minIndexList}

    priceDic = dict()
    # currentDate = datetime(datetime.now().year, datetime.now().month, datetime.now().day)

    ''' LOCAL '''
#     collection = Connection(host=None).mercadodiario.precioses
    ''' SERVIDOR '''
    collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.precioses

    fecha = findLastPriceDocument()
    fecha2 = fecha - timedelta(1)
    fecha3 = fecha - timedelta(2)

    cursor = collection.find({ "fecha": {"$in": [fecha]} })
    priceList = list()
    for element in cursor:
        priceList.append(element['PreciosES'])
    priceDic[date.strftime(fecha, '%Y-%m-%d')] = {'mercado': priceList,
                                                  'horamax': maxList(priceList),
                                                  'horamin': minList(priceList) }

    cursor = collection.find({ "fecha": {"$in": [fecha2]} })
    priceList = list()
    for element in cursor:
        priceList.append(element['PreciosES'])
    priceDic[date.strftime(fecha2, '%Y-%m-%d')] = {'mercado': priceList,
                                                   'horamax': maxList(priceList),
                                                   'horamin': minList(priceList) }

    cursor = collection.find({ "fecha": {"$in": [fecha3]} })
    priceList = list()
    for element in cursor:
        priceList.append(element['PreciosES'])
    priceDic[date.strftime(fecha3, '%Y-%m-%d')] = {'mercado': priceList,
                                                   'horamax': maxList(priceList),
                                                   'horamin': minList(priceList) }

    return priceDic



''' PROFOR necesitaba esta clase para que funcionara de manera independiente al resto de codigo '''
# class PreciosMibelHandler(object):
#     '''
#     Class to parse the Spanish and Portguese Electric Market Prices.
#     Introduced the concept of Mibel Price as the market price set before market split operation.
#     What is used here is not the concept only an aproximation. Because the split can occur in both markets and not only one.
#     But it is a good aproximation to assume that the mibel price is the lower price from the Spanish and Portguese Electric Market Prices
#     '''
#     def __init__(self, thefile=None):
#         try:
#             self.toparsePRECIOS = reader(thefile, delimiter=';')
#             self.precioses = list()
#             self.preciospt = list()
#             self.preciosmibel = list()
#         except:
#             raise
#         else:
#             for row in self.toparsePRECIOS:
#                 if row.__len__() != 0 and row.__len__() > 3:
#                     precioes = stringtofloat(row[5], decimalsep='.', groupsep='')
#                     preciopt = stringtofloat(row[4], decimalsep='.', groupsep='')
#                     self.precioses.append(precioes)
#                     self.preciospt.append(preciopt)
#                     self.preciosmibel.append(min(precioes, preciopt))

# from sys import path
# path.append('libs')
# from omelinfosys.dbpreciosesmanager import DBPreciosES
# ins = DBPreciosES()
class DBPreciosES(object):
    '''
    '''
    connectiondetails = dict(host=None)

    def __init__(self):
        '''
        SET COLLECTION NAME IN MONGO.
        No need for user uname or coopid.
        '''
        # self.connectiondetails['db_name'] = 'preciosmercadodiario'
        self.connectiondetails['db_name'] = 'mercadodiario'
        self.connectiondetails['coll_name'] = 'precioses'
        self.setCollection()

    def updatedbprecioses(self):
        '''
        # insert or update
        # no olvidar de poner un sort por fecha y luego por hora.
        '''
        try:
            self.setCollection()
            collection = self.getCollection()
            results = collection.find({ "fecha": {"$in" : [self.fecha]}, "hora": {"$in": [self.hora]} })
            jsontoinsert = dict()
            jsontoinsert['fecha'] = self.fecha
            jsontoinsert['hora'] = self.hora
            # print getpreciosesfromweb(self.fecha)['PreciosES']
            # jsontoinsert['PreciosES']=getpreciosesfromweb(self.fecha)['PreciosES'][self.hora]
            jsontoinsert['PreciosES'] = self.priceHour
            # print jsontoinsert
            if results.count() == 0:
                collection.insert(jsontoinsert)
            if results.count() == 1:
                collection.update({"fecha": {"$in": [self.fecha]} , "hora" : {"$in" : [self.hora]} }, {"$set": jsontoinsert})
            if results.count() > 1:
                raise Exception('La base de datos tiene mas de un registro para la dada fecha.')
        except:
            raise
        else:
            self.setCollection(), jsontoinsert


    def set_fecha(self, fecha):
        self.fecha = fecha

    def get_connection(self):
        return self._collection

    def getCollection(self):
        '''
        get mongo collection cursor.
        '''
        return self._collection

    def setCollection(self, conndetails=None):
        '''
        sets collection to be used.
        '''
        self._connection = Connection(host=self.connectiondetails['host'])
        self._db = self._connection[self.connectiondetails['db_name']]
        self._collection = self._db[self.connectiondetails['coll_name']]

    def delCollection(self):
        '''
        Remove cursors from mongo database and collections.
        '''
        self._connection.close()
        del self._db, self._collection

    Collection = property(getCollection,
                          setCollection,
                          delCollection,
                          "La collection para hacer las queries")

    def setprecios(self, fechayprecio):
        '''
        Ignora los dias de cambio de hora con la regla de la hora 3.
        '''
        try:
            self.setCollection()
            collection = self.getCollection()
            # Should be something like isert or update:
            collection.insert(fechayprecio)
        except:
            raise
        else:
            self.delCollection()

    # from sys import path
    # path.append('libs')
    # from omelinfosys.dbpreciosesmanager import DBPreciosES
    # ins = DBPreciosES()
    # from datetime import datetime
    # fecha = datetime(2014,1,1)
    # ins.getprecio(fecha)
    def getprecio(self, fecha, hora):
    # def getprecio(self, fechayhora):
        '''
        fechayhora es un datetime con hora.
        '''
        try:
            dic = dict()
            self.setCollection()
            collection = self.getCollection()
            print fecha
            print hora
            # print fechayhora
            # print fechayhora.hour
            results = collection.find({ "fecha": {"$in" : [fecha]}, "hora": {"$in": [hora]} })
            # results = collection.find({ "fecha": {"$in" : [fechayhora]}, "hora": {"$in": [fechayhora.hour]} })
            for result in results:
                print result
                dic = result
        except:
            raise
        else:
            self.delCollection()
            # print dic
            print dic['PreciosES']
            return dic['PreciosES']

    def getprecios(self, fechaStart, fechaEnd=None):
        try:
            self.setCollection()
#             collection = self.getCollection()

        except:
            raise
        else:
            self.delCollection()
        # return [fechayprecio]

    def getallprecios(self):
        try:
            self.setCollection()
#             collection = self.getCollection()
            # no olvidar de poner un sort por fecha y luego por hora.
#             results = collection.find()
        except:
            raise
        else:
            self.delCollection()
        # return [fechayprecio]

    def getlastpreciodate(self):
        try:
            self.setCollection()
#             collection = self.getCollection()

        except:
            raise
        else:
            self.delCollection()
        # return fechayprecio
