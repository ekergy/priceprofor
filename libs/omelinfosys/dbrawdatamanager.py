# -*- coding: utf-8 -*-
'''
Created on 02/2013
@author: hmarrao & david
'''
from pymongo import Connection
from datetime import datetime, timedelta
from utilities import validafecha
from reehandlers import getdemandeforcast, getpreveoldd
from omelhandlers import getproduccionmibelfromweb, getpreciosmibelfromweb
# from os import sys

# from datetime import datetime
# startDate = datetime(2011,1,1)
# endDate = datetime(2013,12,31)
# from sys import path
# path.append('libs')
# from omelinfosys.dbrawdatamanager import populateRawData
# populateRawData(startDate,endDate)
# populateRawData(startDate)
def populateRawData(startDate, endDate=None):
    '''
    Metodos de usabilidad con las clases definidas
    This Method will performe the following operations:
    1st:    Gathering informacion of StudyDataES collection. Last data inserted.
    2nd:    Gathering informacion of RawData collection. Last data available.
    3rd:    Study data won't take into account the change of hour days with the following logic:
            23 hours day: hour 3 will be replicated.
            25 hours day: hour 3 will be removed.
    '''
    try:
        # ONEHOUR = timedelta(seconds=3600)
        ONEDAY = timedelta(1)
        # Disponemos de los datos de la web "http://www.omie.es/inicio" con 3 dias de retraso
        if endDate == None:
            currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
            endDate = currentDate - timedelta(3)
    except:
        raise
    else:
        iterDate = startDate
        while (endDate >= iterDate):
            print iterDate.date()
            ins = DBRawData()
            ins.set_fecha(iterDate)
            ins.getDataFromWeb()
            ins.insertORupdateDataToDB()
            iterDate += ONEDAY

# from sys import path
# path.append('libs')
# from omelinfosys.dbrawdatamanager import findLastRawDocument
# findLastRawDocument()
def findLastRawDocument():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ins = DBRawData()
    collection = ins.get_connection()
    currentDT = datetime.now()
    cursor = collection.find({"fecha": {"$lte": currentDT}})
    for element in cursor:
        lastelement = element
    return lastelement['fecha']

# from sys import path
# path.append('libs')
# from omelinfosys.dbrawdatamanager import updateRawData
# updateRawData()
def updateRawData():
    '''
    Hace lo mismo que la funcion populateRawData pero su fecha de entrada es la ultima que existe en BBDD
    '''
    try:
        startDate = findLastRawDocument()
    except:
        raise
    else:
        populateRawData(startDate)

class DBRawData():
    '''
    classdocs
    '''
    # Class attribute: pymongo connection.
    # Should this always be an no_attribute¿?
    # Maybe yes, because in this ways we may force to del class instance and put connection and close connection
    # at class init and del methods.
    # Class properties:
    # indatabase -> True if there is data in database.
    # connectar con la base de datos y ver si la fecha esta
    # introducida en la base de datos.
    # Check if the date is in the database.
    # self._indatabase = False

    def __init__(self,fecha=None):
        '''
        '''
        try:
#             self.connection = Connection()
#             self.db = self.connection.OMIEData
#             self.collection = self.db.OMIERawData

            ''' LOCAL '''
#             self.connection = Connection(host=None)

            ''' SERVIDOR '''
            self.connection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario')

            # self.db = self.connection.OMIEData
            self.db = self.connection.mercadodiario
            ''' NOMBRE DOCUMENTO (O TABLA) '''
            # self.collection = self.db.OMIEStudyData
            self.collection = self.db.tecnologiases

            if fecha is not None:
                self.fecha = fecha
                results = self.collection.find({ "fecha": {"$in": [self.fecha]} })
                if results.count() == 1:
                    self._indatabase = True
                elif results.count() > 1:
                    raise Exception('La base de datos tiene mas de un registro para la dada fecha.')
                self.connection.close()
        except:
            raise
        else:
            self.setPreciosES(list())
            self.setPreciosPT(list())
            self.setProduccionyDemandaMIBEL(dict())
            self.setProduccionyDemandaES(dict())
            self.setProduccionyDemandaPT(dict())
            self.setPrevisionDemandaMIBEL(list())
            self.setPrevisionDemandaES(list())
            self.setPrevisionDemandaPT(list())
            self.setPrevisionEolicaMIBEL(list())
            self.setPrevisionEolicaES(list())
            self.setPrevisionEolicaPT(list())

    def get_connection(self):
        return self.collection

    def set_fecha(self, fecha):
        self.fecha = fecha

    def getRawDataFromDB(self):
        '''
        '''
        try:
            if not self.indatabase:
                raise Exception('Los datos no estan en la base de datos!')
            results = self.collection.find({"fecha": {"$in" : [self.fecha]}})
            if results.count() > 1:
                raise Exception('La base de datos tiene mas de un registro para la dada fecha.')
            for result in results:
                self.fecha = result['fecha']
                self.PreciosES = result['PreciosES']
                self.PrevisionDemandaES = result['PrevisionDemandaES']
                self.PrevisionEolicaES = result['PrevisionEolicaES']
                self.ProduccionyDemandaES = result['ProduccionyDemandaES']
                #for key,value in self.ProduccionyDemandaES.items():
                #    self.ProducionES[key] = self.jsontoinsert[key]
        except:
            raise
        else:
            self.connection.close()

    def insertORupdateDataToDB(self):
        '''
        sending all data to database.
        Solamente vamos a manobrar los datos de España.
        Luego hay que implementar lo mismo para Portugal 
        Y por fin para el Mibel en general.
        '''
        try:
            results = self.collection.find({"fecha" : {"$in" : [self.fecha]}})
            jsontoinsert = dict()
            # Add the 3 methods here.
            # for key,value in self.ProducionES.items():
            # TODO add ES to key and remove not needed values.
            # jsontoinsert[key]=value
            jsontoinsert['fecha']=self.fecha
            jsontoinsert['PreciosES']=self.PreciosES
            jsontoinsert['ProduccionyDemandaES']=self.ProduccionyDemandaES
            #jsontoinsert['PrevisionDemandaES']=self.PrevisionDemandaES

#             print self.PrevisionDemandaES
#             print self._PrevisionDemandaES
#             print self.getPrevisionDemandaES()

            jsontoinsert['PrevisionDemandaES']=self.PrevisionDemandaES
            jsontoinsert['PrevisionEolicaES']=self.PrevisionEolicaES
            jsontoinsert['PreciosPT']=self.PreciosPT
            jsontoinsert['ProduccionyDemandaPT']=self.ProduccionyDemandaPT
            jsontoinsert['PrevisionDemandaPT']=self.PrevisionDemandaPT
            jsontoinsert['PrevisionEolicaPT']=self.PrevisionEolicaPT
            #jsontoinsert['PreciosMIBEL']=self.PreciosMIBEL
            jsontoinsert['ProduccionyDemandaMIBEL']=self.ProduccionyDemandaMIBEL
            jsontoinsert['PrevisionDemandaMIBEL']=self.PrevisionDemandaMIBEL
            jsontoinsert['PrevisionEolicaMIBEL']=self.PrevisionEolicaMIBEL
            if results.count() == 0:
                # construct the json to insert.
                self.collection.insert(jsontoinsert)
            if results.count() == 1:
                self.collection.update({"fecha": {"$in" : [self.fecha]}},
                                       {"$set" : jsontoinsert})
            if results.count() > 1:
                raise Exception('La base de datos tiene mas de un registro para la dada fecha.')
        except:
            raise
        else:
            self.connection.close()
            del self.connection,self.db,self.collection,results

    @property
    def indatabase(self):
        '''
        gives the value of a data if it is in the data base or not.
        No set method because value is set on instance __init__.
        '''
        return self._indatabase

    # Class properties:
    # fecha -> fecha to work with getting the data

    def getfecha(self):
        return self._fecha

    def setfecha(self,fecha):
        try:
            validafecha(fecha)
            # remove minute or something similar. The idea is to always have 00:00:00 00000 in the datetime time parte.
            # it will easy the query. if not query will be more hard to define.
            fecha = datetime(fecha.year,fecha.month,fecha.day)
        except:
            raise
        else:
            self._fecha=fecha

    def delfecha(self):
        del self._fecha

    fecha = property(getfecha, setfecha, delfecha, "fecha del dia de los datos a insertar en db.")

    # Class properties: 
    # PreciosES -> The Precios from Spanish part of Mibel.

    def getPreciosES(self):
        # return self._PreciosES
        return self._PreciosES

    def setPreciosES(self,precios):
        # should this update de database¿?
        # self._PreciosES = precios
        self._PreciosES = precios

    def delPreciosES(self):
        # del self._PreciosES
        del self._PreciosES

    PreciosES = property(getPreciosES, setPreciosES, delPreciosES, "Precio España del resultado del Mibel.")

    # Class properties: 
    # PreciosPT -> The Precios from Portuguese part of Mibel.

    def getPreciosPT(self):
        return self._PreciosPT

    def setPreciosPT(self,precios):
        self._PreciosPT = precios

    def delPreciosPT(self):
        del self._PreciosPT

    PreciosPT = property(getPreciosPT, setPreciosPT, delPreciosPT, "Precio Portugal del resultado del Mibel.")

    def getProduccionyDemandaMIBEL(self):
        return self._ProduccionyDemandaMIBEL

    def setProduccionyDemandaMIBEL(self,valores):
        # should this update de database¿?
        self._ProduccionyDemandaMIBEL = valores

    def delProduccionyDemandaMIBEL(self):
        del self._ProduccionyDemandaMIBEL

    ProduccionyDemandaMIBEL = property(getProduccionyDemandaMIBEL, setProduccionyDemandaMIBEL, delProduccionyDemandaMIBEL, "ProduccionyDemanda MIBEL.")

    def getProduccionyDemandaES(self):
        return self._ProduccionyDemandaES

    def setProduccionyDemandaES(self,valores):
        # should this update de database¿?
        self._ProduccionyDemandaES = valores

    def delProduccionyDemandaES(self):
        del self._ProduccionyDemandaES

    ProduccionyDemandaES = property(getProduccionyDemandaES, setProduccionyDemandaES, delProduccionyDemandaES, "ProduccionyDemanda ES.")

    def getProduccionyDemandaPT(self):
        return self._ProduccionyDemandaPT

    def setProduccionyDemandaPT(self,valores):
        # should this update de database¿?
        self._ProduccionyDemandaPT = valores

    def delProduccionyDemandaPT(self):
        del self._ProduccionyDemandaPT

    ProduccionyDemandaPT = property(getProduccionyDemandaPT, setProduccionyDemandaPT, delProduccionyDemandaPT, "ProduccionyDemanda PT.")

    def getPrevisionEolicaMIBEL(self):
        return self._PrevisionEolicaMIBEL

    def setPrevisionEolicaMIBEL(self,prevision):
        # should this update de database¿?
        self._PrevisionEolicaMIBEL = prevision

    def delPrevisionEolicaMIBEL(self):
        del self._PrevisionEolicaMIBEL

    PrevisionEolicaMIBEL = property(getPrevisionEolicaMIBEL, 
                                setPrevisionEolicaMIBEL, 
                                delPrevisionEolicaMIBEL, 
                                "Prevision Eolica MIBEL.")

    def getPrevisionEolicaES(self):
        return self._PrevisionEolicaES

    def setPrevisionEolicaES(self,prevision):
        # should this update de database¿?
        self._PrevisionEolicaES = prevision

    def delPrevisionEolicaES(self):
        del self._PrevisionEolicaES

    PrevisionEolicaES = property(getPrevisionEolicaES, 
                                setPrevisionEolicaES, 
                                delPrevisionEolicaES, 
                                "Prevision Eolica ES.")

    def getPrevisionEolicaPT(self):
        return self._PrevisionEolicaPT

    def setPrevisionEolicaPT(self,prevision):
        # should this update de database¿?
        self._PrevisionEolicaPT = prevision

    def delPrevisionEolicaPT(self):
        del self._PrevisionEolicaPT

    PrevisionEolicaPT = property(getPrevisionEolicaPT, 
                                setPrevisionEolicaPT, 
                                delPrevisionEolicaPT, 
                                "Prevision Eolica PT.")

    def getPrevisionDemandaMIBEL(self):
        return self._PrevisionDemandaMIBEL

    def setPrevisionDemandaMIBEL(self,prevision):
        # should this update de database¿?
        self._PrevisionDemandaMIBEL = prevision

    def delPrevisionDemandaMIBEL(self):
        del self._PrevisionDemandaMIBEL

    PrevisionDemandaMIBEL = property(getPrevisionDemandaMIBEL, 
                                setPrevisionDemandaMIBEL, 
                                delPrevisionDemandaMIBEL, 
                                "Prevision Demanda MIBEL.")

    # from sys import path
    # path.append('libs')
    # from omelinfosys.dbrawdatamanager import DBRawData
    # ins = DBRawData()
    # from datetime import datetime
    # fecha = datetime(2011,3,19)
    # ins.fecha = fecha
    # ins.getPrevisionDemandaESfromWeb()
    # ins.getPrevisionDemandaES()
    def getPrevisionDemandaES(self):
        return self._PrevisionDemandaES

    def setPrevisionDemandaES(self,prevision):
        # should this update de database¿?
        self._PrevisionDemandaES = prevision

    def delPrevisionDemandaES(self):
        del self._PrevisionDemandaES

    PrevisionDemandaES = property(getPrevisionDemandaES, 
                                setPrevisionDemandaES, 
                                delPrevisionDemandaES, 
                                "Prevision Demanda ES.")

    def getPrevisionDemandaPT(self):
        return self._PrevisionDemandaPT

    def setPrevisionDemandaPT(self,prevision):
        # should this update de database¿?
        self._PrevisionDemandaPT = prevision

    def delPrevisionDemandaPT(self):
        del self._PrevisionDemandaPT

    PrevisionDemandaPT = property(getPrevisionDemandaPT, 
                                setPrevisionDemandaPT, 
                                delPrevisionDemandaPT, 
                                "Prevision Demanda PT.")

    # Class method:
    # getPreciosMibelFromWeb -> The Precios from Portuguese part of Mibel.

    def getPreciosMibelFromWeb(self):
        result = getpreciosmibelfromweb(self.fecha)
        self.PreciosES = result['PreciosES']
        self.PreciosPT = result['PreciosPT']
        '''
        esta funcion talvez este mejor fuera de la clase y asi la podemos usar con otros metodos y classes
        como esta echo con las Previsiones.
        try:
            # The marginalpdbc data have the Psanish and the Portuguese prices.
            toparsePRECIOSES = reader(urlopen(omiepreciosesurl(self.fecha)),delimiter=';')
            __precioses = list()
            __preciospt = list()
        except:
            raise
        else:
            for row in toparsePRECIOSES:
                if row.__len__()!=0 and row.__len__()>3 :
                    __precioses.append(stringtofloat(row[5],decimalsep='.',groupsep=''))
                    __preciospt.append(stringtofloat(row[4],decimalsep='.',groupsep=''))
        '''

    # Class method:
    # getProducionFromWeb -> The Producion ES PT and MIBEL from the omie web.

    def getProducionFromWeb(self):
        '''
        '''
        result = getproduccionmibelfromweb(self.fecha)
        # must separate Producion from Demanda.
        # Here may not be needed but in the speficic collections it's a must do.
        self.ProduccionyDemandaMIBEL = result['ProduccionyDemandaMIBEL']
        self.ProduccionyDemandaES = result['ProduccionyDemandaES']
        self.ProduccionyDemandaPT = result['ProduccionyDemandaPT']

    def getPrevisionDemandaESfromWeb(self):
        '''
        '''
        self.PrevisionDemandaES = getdemandeforcast(self.fecha)

    def getPrevisionEolicaESfromWeb(self):
        '''
        '''
        self.PrevisionEolicaES = getpreveoldd(self.fecha)

    def getDataFromWeb(self):
        self.getPrevisionDemandaESfromWeb()
        self.getPrevisionEolicaESfromWeb()
        self.getProducionFromWeb()
        self.getPreciosMibelFromWeb()

    def writeinfotofile(self,filename):
        '''
        '''
        print self.fecha,self.PreciosES,self.PrevisionDemandaES,self.PrevisionEolicaES,self.ProduccionyDemandaES

    def verificaDatos(self):
        '''
        Este metodo verifica cuantos datos tiene este dia:
        el resultado es un dict con {'numhoras':"el numero de horas del dia":
                                    'obs':["Comentario por si falta algun dato en
                                    alguno de los cammpos"]}
        numhoras = 0
        obs = []
        try:
            if self. is None:
                numhoras = len()
                obs.append("")
            if self. is None:
                obs.append("")
            if self. is None:
                obs.append("")
        except:
            pass
        else:
            pass
            return {'numhoras':,
                    'obs':}
        '''
        pass

# from datetime import datetime
# startDate = datetime(2011,1,1)
# endDate = datetime(2011,6,30)
# from sys import path
# path.append('libs')
# from omelinfosys.dbrawdatamanager import populateRawData2
# populateRawData2(startDate,endDate)
# populateRawData2(startDate)
def populateRawData2(startDate, endDate=None):
    '''
    Metodos de usabilidad con las clases definidas
    This Method will performe the following operations:
    1st:    Gathering informacion of StudyDataES collection. Last data inserted.
    2nd:    Gathering informacion of RawData collection. Last data available.
    3rd:    Study data won't take into account the change of hour days with the following logic:
            23 hours day: hour 3 will be replicated.
            25 hours day: hour 3 will be removed.
    '''
    try:
        from datosEnFaltaEnergias import centralEuropeanTime, datosEnFalta, diasEnFalta
        emptyPD, zeroPD = diasEnFalta()
        listDT = emptyPD + zeroPD
        # ONEHOUR = timedelta(seconds=3600)
        ONEDAY = timedelta(1)
        # Disponemos de los datos de la web "http://www.omie.es/inicio" con 3 dias de retraso
        if endDate == None:
            currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
            endDate = currentDate - timedelta(3)
    except:
        raise
    else:
        iterDate = startDate
        while (endDate >= iterDate):
            print iterDate.date()
            ins = DBRawData()
            ins.set_fecha(iterDate)

            listCHV = list()
            listCHI = list()
            for indi in range(endDate.year - startDate.year + 1):
                fechaCHV, fechaCHI = centralEuropeanTime(startDate.year + indi)
                listCHV.append(fechaCHV)
                listCHI.append(fechaCHI)

            if iterDate in listDT:
                ins.getDataFromWeb()
                dic = datosEnFalta(iterDate)
                if dic['PreciosES']:
                    ins.setPreciosES(dic['PreciosES'])
                if dic['PrevisionEolicaES']:
                    ins.setPrevisionEolicaES(dic['PrevisionEolicaES'])
                if dic['PrevisionDemandaES']:
                    ins.setPrevisionDemandaES(dic['PrevisionDemandaES'])
                if dic['ProduccionyDemandaES']:
                    ins.setProduccionyDemandaES(dic['ProduccionyDemandaES'])

            elif iterDate in listCHV:
                ''' VERANO '''
                ins.getDataFromWeb()
                # Al cambiar de hora a verano pasamos de la hora 2:00 a la 3:00 (haremos ambos datos iguales)
                horaCHV = 3
                preci = ins.getPreciosES()
                if len(preci) == 23:
                    preci.insert(horaCHV,preci[horaCHV-1])
                    ins.setPreciosES(preci)
                    del preci
                eoli = ins.getPrevisionEolicaES()
                if len(eoli) == 23:
                    eoli.insert(horaCHV,eoli[horaCHV-1])
                    ins.setPrevisionEolicaES(eoli)
                    del eoli
                deman = ins.getPrevisionDemandaES()
                if len(deman) == 23:
                    deman.insert(horaCHV,deman[horaCHV-1])
                    ins.setPrevisionDemandaES(deman)
                    del deman

            elif iterDate in listCHI:
                ''' INVIERNO '''
                ins.getDataFromWeb()
                # Al cambiar de hora a invierno pasamos de la hora 3:00 a la 2:00 (eliminamos el dato 3:00)
                horaCHI = 3
                preci = ins.getPreciosES()
                if len(preci) == 25:
                    preci.pop(horaCHI)
                    ins.setPreciosES(preci)
                    del preci
                eoli = ins.getPrevisionEolicaES()
                if len(eoli) == 25:
                    eoli.pop(horaCHI)
                    ins.setPrevisionEolicaES(eoli)
                    del eoli
                deman = ins.getPrevisionDemandaES()
                if len(deman) == 25:
                    deman.pop(horaCHI)
                    ins.setPrevisionDemandaES(deman)
                    del deman

            else:
                ins.getDataFromWeb()

            ins.insertORupdateDataToDB()
            iterDate += ONEDAY
