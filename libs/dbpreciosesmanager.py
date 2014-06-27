# -*- coding: utf-8 -*-
'''
Created on 05/2014
@author: hmarrao & david
'''
from os import path
direc = path.abspath(__file__)
machine = direc[direc.find("e")+2:direc.find("w")-1]

# from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import Connection
from datetime import datetime, timedelta
from utilities import omiepreciosurl, stringtofloat, cambiohoraverano, cambiohorainvierno
# from utilities import validafecha
from urllib2 import urlopen
# from urllib2 import Request, URLError
from csv import reader

# # -*- coding: utf-8 -*-
# '''
# Created on 05/2014
# @author: hmarrao & david
# '''

from utilities import validafecha, omiepreciosurl, stringtofloat
# from urllib2 import urlopen
# from csv import reader
# from pymongo import Connection
# from datetime import datetime, timedelta


# from sys import path
# path.append('libs')
# from datetime import datetime
# # startDT = datetime(2014,1,1)
# # endDT = datetime(2014,2,1)
# from dbpreciosesmanager import populatePrecios
# populatePrecios()
# # populatePrecios(startDT,endDT)
def populatePrecios(startDate=None, endDate=None):
    '''
    '''
    try:
        ONEDAY = timedelta(1)
        if startDate == None:
            startDate = findLastPriceDocument()
        if endDate == None:
            currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
            # endDate = currentDate - timedelta(3)
            if datetime.now().hour >= 0 and datetime.now().hour < 14:
                print 'TODAY'
                # print 'TODAY is the last day'
                endDate = currentDate
            elif datetime.now().hour >= 14 and datetime.now().hour <= 23:
                print 'TOMORROW'
                # print 'TOMORROW is the last day'
                endDate = currentDate + timedelta(1)
    except:
        raise
    else:
        # listDaysUpdated = list()
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
            # listDaysUpdated.append(iterDate.date())
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
        # return listDaysUpdated

# from sys import path
# path.append('libs')
# from omelinfosys.dbpreciosesmanager import findLastPriceDocument
# findLastPriceDocument()
def findLastPriceDocument():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ins = DBPreciosES()
    return ins.getlastrecordfromdatabase()['fecha']

# from sys import path
# path.append('libs')
# from datetime import datetime
# fecha = datetime(2014,1,1)
# from dbpreciosesmanager import getpreciosesfromweb
# getpreciosesfromweb(fecha)
def getLastDayPriceVector():
    '''
    '''
    ins = DBPreciosES()
    listofvalues = ins.getlastdayfromdatabase()
    prices = [value['PreciosES'] for value in listofvalues]
    return prices

def getpreciosesfromweb(fecha,numero=None):
        '''
        This is the main method so the usage of PreciosMibelHandler is more strainfoward.
        '''
        try:
#             currentDate = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
#             if fecha == currentDate + datetime.timedelta(1):
#                 validafecha(fecha - datetime.timedelta(1))
#             else:
#                 validafecha(fecha)
            URL = omiepreciosurl(fecha)
            # print URL
            toparsePRECIOS = urlopen(URL)
        except:
            raise
#             req = Request(omiepreciosurl(fecha))
#             urlopen(req)
#         except URLError, e:
#             print e.reason
        else:
            Precios = PreciosMibelHandler(toparsePRECIOS)
            # print Precios.precioses
            if Precios.precioses == []:
#                 print ''
#                 print 'ERROR'
#                 print 'la fecha',fecha.date(),'no tiene precios horarios'
#                 print ''
                numero = '2'
                print fecha.date()
                URL = omiepreciosurl(fecha)[:len(omiepreciosurl(fecha))-1]+str(numero)
                print URL
                toparsePRECIOS = urlopen(URL)
                Precios = PreciosMibelHandler(toparsePRECIOS)
                print Precios.precioses
                return {"PreciosES": Precios.precioses}
            else:
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

class PreciosMibelHandler(object):
    '''
    Class to parse the Spanish and Portguese Electric Market Prices.
    Introduced the concept of Mibel Price as the market price set before market split operation.
    What is used here is not the concept only an aproximation. Because the split can occur in both markets and not only one.
    But it is a good aproximation to assume that the mibel price is the lower price from the Spanish and Portguese Electric Market Prices
    '''
    def __init__(self, thefile=None):
        try:
            self.toparsePRECIOS = reader(thefile, delimiter=';')
            self.precioses = list()
            self.preciospt = list()
            self.preciosmibel = list()
        except:
            raise
        else:
            for row in self.toparsePRECIOS:
                if row.__len__() != 0 and row.__len__() > 3:
                    precioes = stringtofloat(row[5], decimalsep='.', groupsep='')
                    preciopt = stringtofloat(row[4], decimalsep='.', groupsep='')
                    self.precioses.append(precioes)
                    self.preciospt.append(preciopt)
                    self.preciosmibel.append(min(precioes, preciopt))

# from sys import path
# path.append('libs')
# from omelinfosys.dbpreciosesmanager import DBPreciosES
# ins = DBPreciosES()
class DBPreciosES(object):
    '''
    LOCAL
    '''
#     connectiondetails = dict(host=None)
    '''
    SERVIDOR
    '''
    connectiondetails = dict(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario')

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
            # print fecha
            # print hora
            # print fechayhora
            # print fechayhora.hour
            results = collection.find({ "fecha": {"$in" : [fecha]}, "hora": {"$in": [hora]} })
            # results = collection.find({ "fecha": {"$in" : [fechayhora]}, "hora": {"$in": [fechayhora.hour]} })
            for result in results:
                # print result
                dic = result
        except:
            raise
        else:
            self.delCollection()
            # print dic
            # print dic['PreciosES']
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

    def getlastprecioindatabase(self):
        try:
            self.setCollection()
            collection = self.getCollection()
            results = collection.find({}).sort(u'fecha', DESCENDING)
            # print results[0]
            #for result in results:
            #    print result
        except:
            raise
        else:
            self.delCollection()
        # return fechaypreci
        return results[0]

    def getlastrecordfromdatabase(self):
        try:
            self.setCollection()
            collection = self.getCollection()
            results = collection.find({}).sort(u'fecha', DESCENDING)
            # print results[0]
            #for result in results:
            #    print result
        except:
            raise
        else:
            self.delCollection()
        # return fechaypreci
        return results[0]

    def getlastdayfromdatabase(self):
        try:
            self.setCollection()
            collection = self.getCollection()
            results = collection.find({}).sort(u'fecha', DESCENDING)
            fecha = results[0]['fecha']
            lastday = []
            i = 0
            while fecha == results[i]['fecha']:
                lastday.append(results[i])
                i = i+1
            #for result in results:
            #    print result hay que asemblar el el vector del dia.
        except:
            raise
        else:
            self.delCollection()
        # return fechaypreci
        return lastday

# # -*- coding: utf-8 -*-
# '''
# Created on 05/2014
# @author: hmarrao & david
# '''
# 
# from utilities import validafecha, omiepreciosurl, stringtofloat
# from urllib2 import urlopen
# from csv import reader
# from pymongo import Connection
# from datetime import datetime, timedelta

# def updatedbprecioses():
#     '''
#     desde 2011.
#     '''
#     startdate = datetime(2011,1,1)
#     today = datetime.now()
#     # 3 dias menos:
#     enddate = None
#     # localhost:
#     # mongolab:
#     # formatear los precios {'fecha':datetime,'precioes':precio}
#     # insertar los precios:

# def getpreciosesfromweb(fecha):
#         '''
#         This is the main method so the usage of PreciosMibelHandler is more strainfoward.
#         '''
#         try:
#             validafecha(fecha)
#             # The marginalpdbc data have the Spanish and the Portuguese prices.
#             toparsePRECIOS = urlopen(omiepreciosurl(fecha))
#         except:
#             raise
#         else:
#             Precios = PreciosMibelHandler(toparsePRECIOS)
#             return {"PreciosES": Precios.precioses}
#         #finally:
#         #    del toparsePRECIOS,Precios

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import preciosDiarios
# preciosDiarios()
def preciosDiarios(fechayhora=None):
    '''
    notar que en el proyecto "profordes" dentro del script con el mismo nombre que este
    esta implementado el metodo "populatePrecios" que actualiza esta misma base de datos
    '''
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

    collection = Connection(host=None).OMIEData.OMIEStudyData
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

class dbpreciosmanager(object):
    '''
    docstring
    '''
    connectiondetails = dict(host=None)

    def __init__(self):
        '''
        SET COLLECTION NAME IN MONGO.
        No need for user uname or coopid.
        '''
        self.connectiondetails['coll_name'] = 'precioses'

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
        self._db = self._connection.profor
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
            collection.insert(fechayprecio)
        except:
            raise
        else:
            self.delCollection()

    def getprecio(self, fechayhora):
        pass

    def getprecios(self, fechaStart, fechaEnd=None):
        pass

    def getallprecios(self):
        pass

    def getlastpreciodate(self):
        pass

# if __name__ == '__main__':
#     '''
#     Actualiza la base de datos de precios diarios
#     '''
#     populatePrecios()
