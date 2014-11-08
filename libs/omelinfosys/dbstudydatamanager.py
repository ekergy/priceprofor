# -*- coding: utf-8 -*-
'''
Created on 02/2013
@author: hmarrao & david
'''

# from datosEnFaltaEnergias import centralEuropeanTime
from pymongo import Connection
from datetime import datetime, timedelta
from dbrawdatamanager import DBRawData
from datosEnFaltaEnergias import datosEnFalta, diasEnFalta
from omelinfosys.omelhandlers import ProduccionMibelHandler
from utilities import omieproduccionurl, diasconcambiodehora
from urllib2 import urlopen

# from sys import path
# path.append('libs')
# from omelinfosys.dbstudydatamanager import DBStudyData
# hostOpenShift = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
# DBStudyData.connectiondetails['host'] = hostOpenShift
# from datetime import datetime
# startDate = datetime(2014,10,1)
# from omelinfosys.dbstudydatamanager import populateStudyData
# populateStudyData(startDate)
def populateStudyData(startDate=None, endDate=None):
    '''
    Requirements:
    1st:    Gathering information of StudyDataES collection. Last data inserted.
    2nd:    Gathering information of RawData collection . Last data available.
            (NOTE: not needed: just use RawData class to 
            grep data from web and not from database. 
            The idea here is to make this work without a RawData collection so it will work on openshift)
    3rd:    Study data will take into account the change of hour days with the following logic:
            23 hours day: hour 3 will be replicated.
            25 hours day: hour 3 will be removed.

    Working flow:
        populateStudyData must take into account the missing data and identify the days with 23hours and 25hours.

    Input data:
    startDate as by default the last available data in the Study collection
    endDate as by default the last available data omel server (for now it cames with 3 days delay.)
    '''
    # setting up input data:
    try:
        currentDate = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        availableDate = currentDate - timedelta(3)
        if startDate == None:
            doc = findLastStudyDocument()
            startDate = doc['fecha']
        if startDate > availableDate:
                startDate = availableDate
                # Disponemos de los datos de la web de la "OMIE" con 3 dias de retraso
        if endDate == None:
            endDate = availableDate
        if endDate > availableDate:
                endDate = availableDate
    except:
        raise
    else:
        listaux = diasconcambiodehora(startDate,endDate)
        listCHV = listaux['DiasCambioDeHoraAverano']
        listCHI = listaux['DiasCambioDeHoraAinvierno']

        emptyPD, zeroPD = diasEnFalta()
        listDT = emptyPD + zeroPD
        iterDate = startDate
        ONEDAY = timedelta(1)
        while (endDate >= iterDate):
            print 'Updating',iterDate.date()
            ins_raw = DBRawData()
            ins_raw.set_fecha(iterDate)
            ins_raw.getDataFromWeb()
            # VERANO: arreglar dias con 23 horas y dejarlos en 24
            if iterDate in listCHV:
                ins_raw.PreciosES.insert(3,ins_raw.PreciosES[2])
                ins_raw.PrevisionDemandaES.insert(3,ins_raw.PrevisionDemandaES[2])
                ins_raw.PrevisionEolicaES.insert(3,ins_raw.PrevisionEolicaES[2])
                for key,value in ins_raw.ProduccionyDemandaES.iteritems():
                    if isinstance(value,list):
                        value.insert(3,value[2])
            # INVIERNO: arreglar dias con 25 horas y dejarlos en 24
            if iterDate in listCHI:
                ins_raw.PreciosES.pop(3)
                ins_raw.PrevisionDemandaES.pop(3)
                ins_raw.PrevisionEolicaES.pop(3)
                for key,value in ins_raw.ProduccionyDemandaES.iteritems():
                    if isinstance(value,list):
                        value.pop(3)
            for i in range(len(ins_raw.PreciosES)):
                ins_study = DBStudyData()
                ins_study.fecha = iterDate
                ins_study.hora = i
                # PRODUCCION
                ins_study.NUCLEAR = ins_raw.ProduccionyDemandaES['NUCLEAR'][i]
                ins_study.HIDRAULICA_CONVENCIONAL = ins_raw.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][i]
                ins_study.REGIMEN_ESPECIAL = ins_raw.ProduccionyDemandaES['REGIMEN_ESPECIAL_A_MERCADO'][i]
                ins_study.CARBON = ins_raw.ProduccionyDemandaES['CARBON_IMPORTACION'][i]
                ins_study.CICLO_COMBINADO = ins_raw.ProduccionyDemandaES['CICLO_COMBINADO'][i]
                ins_study.HIDRAULICA_BOMBEO = ins_raw.ProduccionyDemandaES['CONSUMO_DE_BOMBEO'][i]
                ins_study.TERMICO_CON_PRIMA = ins_raw.ProduccionyDemandaES['TOTAL_TERMICA_(3+4+5+6+7+8)'][i]
                ins_study.IMPORTACION_FRANCIA = ins_raw.ProduccionyDemandaES['IMPORTACION_FRANCIA'][i]
                ins_study.IMPORTACION_PORTUGAL = ins_raw.ProduccionyDemandaES['IMPORTACION_PORTUGAL'][i]
                ins_study.IMPORTACION_MARRUECOS = ins_raw.ProduccionyDemandaES['IMPORTACION_MARRUECOS'][i]
                ins_study.IMPORTACION_ANDORRA = ins_raw.ProduccionyDemandaES['IMPORTACION_ANDORRA'][i]

                if iterDate not in listDT:
                    ins_study.ENERGIA_GESTIONADA = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA'][i]
                    ins_study.REGIMEN_ESPECIAL_A_DISTRIBUCION = ins_raw.ProduccionyDemandaES['REGIMEN_ESPECIAL_A_DISTRIBUCION'][i]
                    ins_study.FUEL_GAS = ins_raw.ProduccionyDemandaES['FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)'][i]
                    ins_study.UNIDADES_GENERICAS = ins_raw.ProduccionyDemandaES['UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION'][i]
                    # DEMANDA
                    ins_study.TOTAL_DEMANDA_NACIONAL_CLIENTES = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)'][i]
                    ins_study.TOTAL_CONSUMO_BOMBEO = ins_raw.ProduccionyDemandaES['TOTAL_CONSUMO_BOMBEO_(24)'][i]
                    ins_study.TOTAL_EXPORTACIONES = ins_raw.ProduccionyDemandaES['TOTAL_EXPORTACIONES_(25+26+27+28+29)'][i]
                    ins_study.TOTAL_GENERICAS = ins_raw.ProduccionyDemandaES['TOTAL_GENERICAS_(30+31)'][i]

                if iterDate in listDT:
                    dic = datosEnFalta(iterDate)

                    # if i == 0:
                    #     print dic
                    if dic['PreciosES']:
                        ins_study.Precios = dic['PreciosES'][i]
                    else:
                        ins_study.Precios = ins_raw.PreciosES[i]
                    if dic['PrevisionEolicaES']:
                        ins_study.PrevisionEolica = dic['PrevisionEolicaES'][i]
                    else:
                        ins_study.PrevisionEolica = ins_raw.PrevisionEolicaES[i]
                    if dic['PrevisionDemandaES']:
                        ins_study.PrevisionDemanda = dic['PrevisionDemandaES'][i]
                    else:
                        ins_study.PrevisionDemanda = ins_raw.PrevisionDemandaES[i]

                else:
                    ins_study.Precios = ins_raw.PreciosES[i]
                    ins_study.PrevisionEolica = ins_raw.PrevisionEolicaES[i]
                    ins_study.PrevisionDemanda = ins_raw.PrevisionDemandaES[i]

                ins_study.insertorupdatedataintodb()

            if currentDate == iterDate + timedelta(3):
                raise Exception('En la web del OMIE no hay datos de hoy, ayer y antes de ayer')

            iterDate += ONEDAY

# from sys import path
# path.append('libs')
# from omelinfosys.dbstudydatamanager import findLastStudyDocument
# findLastStudyDocument()
def findLastStudyDocument():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ins_study = DBStudyData()
    collection = ins_study.getCollection()
    # cursor = collection.find().sort("fecha",-1).limit(1)
    cursor = collection.find().sort([("fecha",-1),("hora",-1)]).limit(1)
    for element in cursor:
        # print element['hora']
        # fecha = element['fecha']
        docu = element
    del ins_study
    return docu

# from sys import path
# path.append('libs')
# from omelinfosys.dbstudydatamanager import findFirstStudyDocument
# findFirstStudyDocument()
def findFirstStudyDocument():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ins_study = DBStudyData()
    collection = ins_study.getCollection()
    # cursor = collection.find().sort("fecha",-1).limit(1)
    cursor = collection.find().sort([("fecha",1),("hora",1)]).limit(1)
    for element in cursor:
        # print element['hora']
        # fecha = element['fecha']
        docu = element
    del ins_study
    return docu

####################################################################################################

# from sys import path
# path.append('libs')
# from datetime import datetime
# fecha = datetime(2014,1,1)
# from omelinfosys.dbstudydatamanager import gettecnologiasesfromweb
# gettecnologiasesfromweb(fecha)
def gettecnologiasesfromweb(fecha):
        '''
        This is the main method so the usage of PreciosMibelHandler is more strainfoward.
        '''
        try:
            # validafecha(fecha)
            # The marginalpdbc data have the Spanish and the Portuguese prices.
            toparsePRODUCCION = urlopen(omieproduccionurl(fecha))
        except:
            raise
        else:
            Produccion = ProduccionMibelHandler(toparsePRODUCCION)
            # return {"ProduccionyDemandaMIBEL":Produccion.ProduccionyDemandaMIBEL,"ProduccionyDemandaES":Produccion.ProduccionyDemandaES,"ProduccionyDemandaPT":Produccion.ProduccionyDemandaPT}
            return {"ProduccionyDemandaES":Produccion.ProduccionyDemandaES}

####################################################################################################

class DBStudyData():
    '''
    Esta clase es solo para gestionar la informacion a la hora de meter datos en la base de datos.
    Las consultas que nos interesa hacer las podemos filtrar con queries directas a la base de datos de registros.
    Asi es más facil consultar la importacion haciendo filtros de los datos y ordenar los datos a nuestro antojo.
    Creo que tambien sera más rapido.

    "fecha":,
    "hora":,
    "Precios":,
    "PrevisionDemanda":,
    "PrevisionEolica":,
    "ENERGIA_GESTIONADA":,

    -> Produccion
    "NUCLEAR":,
    "REGIMEN_ESPECIAL":,
    "HIDRAULICA_CONVENCIONAL":,
    "HIDRAULICA_BOMBEO":,
    "CARBON":,
    "CICLO_COMBINADO":,
    "FUEL_GAS":,
    "TERMICO_CON_PRIMA":,
    "UNIDADES_GENERICAS":,
    "IMPORTACION_PORTUGAL":,
    "IMPORTACION_FRANCIA":,
    "IMPORTACION_ANDORRA":,
    "IMPORTACION_MARRUECOS":,

    "REGIMEN_ESPECIAL_A_DISTRIBUCION:"

    -> Demanda
    La demanda tambien es importante ya que una demanda fuera del comun puede hacer subir los precios un monton
    Las centrales de bombeo pueden demandar energia y ademas con precio alto y asi inflacionar los precios de mercado
    Esto es una supocion
    '''

    connectiondetails = dict(host=None)
#     connectiondetails = dict()

    def __init__(self):
        '''
        if no hour is given get it from the fecha
        in data base hour in fecha timestamp(datetime) is set to zero in order to be able to perform queries of a full day
        '''
        try:
            # Remember to force here the database that one want to work in:
            # self.connectiondetails['host'] = None
            # self.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
            self.connectiondetails['host'] = self.connectiondetails['host']
            self.connectiondetails['db_name'] = 'mercadodiario'
            self.connectiondetails['coll_name'] = 'tecnologiases'
            self.setCollection()

        except:
            raise
        else:
            # instance attributes definitions
            self.Precios = 0
            self.PrevisionDemanda = 0
            self.PrevisionEolica = 0
            self.ENERGIA_GESTIONADA = 0
            self.NUCLEAR = 0
            self.REGIMEN_ESPECIAL = 0
            self.HIDRAULICA_CONVENCIONAL = 0
            self.HIDRAULICA_BOMBEO = 0
            self.CARBON = 0
            self.CICLO_COMBINADO = 0
            self.FUEL_GAS = 0
            self.TERMICO_CON_PRIMA = 0
            self.UNIDADES_GENERICAS = 0
            self.IMPORTACION_PORTUGAL = 0
            self.IMPORTACION_FRANCIA = 0
            self.IMPORTACION_ANDORRA = 0
            self.IMPORTACION_MARRUECOS = 0

            self.TOTAL_DEMANDA_NACIONAL_CLIENTES = 0
            self.TOTAL_CONSUMO_BOMBEO = 0
            self.TOTAL_EXPORTACIONES = 0
            self.TOTAL_GENERICAS = 0

            self.REGIMEN_ESPECIAL_A_DISTRIBUCION = 0

    def getCollection(self):
        '''
        Get mongo collection cursor
        '''
        return self._collection

    def setCollection(self, connectiondetails=None):
        '''
        Sets collection to be used
        '''
        self._connection = Connection(host=self.connectiondetails['host'])
        self._db = self._connection[self.connectiondetails['db_name']]
        self._collection = self._db[self.connectiondetails['coll_name']]

    def delCollection(self):
        '''
        Remove cursors from mongo database and collections
        '''
        self._connection.close()
        del self._db, self._collection

    Collection = property(getCollection,
                          setCollection,
                          delCollection,
                          "La collection para hacer las queries")


    # from sys import path
    # path.append('libs')
    # from datetime import datetime
    # fecha = datetime(2012,1,1)
    # from omelinfosys.DBStudyData import DBStudyData
    # ins = DBStudyData()
    # ins.getStudyDataFromDB(fecha)
    # hora = 6
    # ins.getStudyDataFromDB(fecha,hora)
    def getStudyDataFromDB(self,fecha,hora=None):
        '''
        Get Study data from db.
        If no hora it will return the last document available for that fecha.
        '''
        try:
            if hora is None:
                results = self.collection.find({ "fecha": {"$in" : [fecha]} })
            else:
                results = self.collection.find({ "fecha": {"$in" : [fecha]}, "hora": {"$in": [hora]} })

            for result in results:
                # print result
                self.fecha = result["fecha"]
                self.hora = result["hora"]

                ##############
                # PRODUCCION #
                ##############
                self.Precios = result["Precios"]
                self.PrevisionDemanda = result["PrevisionDemanda"]
                self.PrevisionEolica = result["PrevisionEolica"]
                self.ENERGIA_GESTIONADA = result["ENERGIA_GESTIONADA"]
                self.NUCLEAR = result["NUCLEAR"]
                self.REGIMEN_ESPECIAL = result["REGIMEN_ESPECIAL"]
                self.HIDRAULICA_CONVENCIONAL = result["HIDRAULICA_CONVENCIONAL"]
                self.HIDRAULICA_BOMBEO = result["HIDRAULICA_BOMBEO"]
                self.CARBON = result["CARBON"]
                self.CICLO_COMBINADO = result["CICLO_COMBINADO"]
                self.FUEL_GAS = result["FUEL_GAS"]
                self.TERMICO_CON_PRIMA = result["TERMICO_CON_PRIMA"]
                self.UNIDADES_GENERICAS = result["UNIDADES_GENERICAS"]
                self.IMPORTACION_PORTUGAL = result["IMPORTACION_PORTUGAL"]
                self.IMPORTACION_FRANCIA = result["IMPORTACION_FRANCIA"]
                self.IMPORTACION_ANDORRA = result["IMPORTACION_ANDORRA"]
                self.IMPORTACION_MARRUECOS = result["IMPORTACION_MARRUECOS"]

                ##############
                # DEMANDA #
                ##############
                self.TOTAL_DEMANDA_NACIONAL_CLIENTES = result['TOTAL_DEMANDA_NACIONAL_CLIENTES']
                self.TOTAL_CONSUMO_BOMBEO = result['TOTAL_CONSUMO_BOMBEO']
                self.TOTAL_EXPORTACIONES = result['TOTAL_EXPORTACIONES']
                self.TOTAL_GENERICAS = result['TOTAL_GENERICAS']

                self.REGIMEN_ESPECIAL_A_DISTRIBUCION = result["REGIMEN_ESPECIAL_A_DISTRIBUCION"]

        except:
            raise
        else:
            self.connection.close()

    def insertorupdatedataintodb(self):
        '''
        '''
        try:

            self.setCollection()
            collection = self.getCollection()

            # collection = db[self.collectionName]
            results = collection.find({"fecha" : {"$in": [self.fecha]}, "hora": {"$in": [self.hora]}})
            jsontoinsert = dict()
            jsontoinsert["fecha"] = self.fecha
            jsontoinsert["hora"] = self.hora

            ''' PRODUCCION '''
            jsontoinsert["Precios"] = self.Precios
            jsontoinsert["PrevisionDemanda"] = self.PrevisionDemanda
            jsontoinsert["PrevisionEolica"] = self.PrevisionEolica
            jsontoinsert["ENERGIA_GESTIONADA"] = self.ENERGIA_GESTIONADA
            jsontoinsert["NUCLEAR"] = self.NUCLEAR
            jsontoinsert["REGIMEN_ESPECIAL"] = self.REGIMEN_ESPECIAL
            jsontoinsert["HIDRAULICA_CONVENCIONAL"] = self.HIDRAULICA_CONVENCIONAL
            jsontoinsert["HIDRAULICA_BOMBEO"] = self.HIDRAULICA_BOMBEO
            jsontoinsert["CARBON"] = self.CARBON
            jsontoinsert["CICLO_COMBINADO"] = self.CICLO_COMBINADO
            jsontoinsert["FUEL_GAS"] = self.FUEL_GAS
            jsontoinsert["TERMICO_CON_PRIMA"] = self.TERMICO_CON_PRIMA
            jsontoinsert["UNIDADES_GENERICAS"] = self.UNIDADES_GENERICAS
            jsontoinsert["IMPORTACION_PORTUGAL"] = self.IMPORTACION_PORTUGAL
            jsontoinsert["IMPORTACION_FRANCIA"] = self.IMPORTACION_FRANCIA
            jsontoinsert["IMPORTACION_ANDORRA"] = self.IMPORTACION_ANDORRA
            jsontoinsert["IMPORTACION_MARRUECOS"] = self.IMPORTACION_MARRUECOS

            ''' DEMANDA '''
            jsontoinsert["TOTAL_DEMANDA_NACIONAL_CLIENTES"] = self.TOTAL_DEMANDA_NACIONAL_CLIENTES
            jsontoinsert["TOTAL_CONSUMO_BOMBEO"] = self.TOTAL_CONSUMO_BOMBEO
            jsontoinsert["TOTAL_EXPORTACIONES"] = self.TOTAL_EXPORTACIONES
            jsontoinsert["TOTAL_GENERICAS"] = self.TOTAL_GENERICAS

            jsontoinsert["REGIMEN_ESPECIAL_A_DISTRIBUCION"] = self.REGIMEN_ESPECIAL_A_DISTRIBUCION

            if results.count() == 0:
                # construct the json to insert
                collection.insert(jsontoinsert)
            if results.count() == 1:
                collection.update({"fecha" : {"$in" : [self.fecha]},
                                        "hora" : {"$in" : [self.hora]}},
                                       {"$set" : jsontoinsert })
            if results.count() > 1:
                raise Exception('La base de datos tiene mas de un registro para la dada fecha')
        except:
            raise
        else:
            self.setCollection(), jsontoinsert

class DBManagerStudyDataES(DBStudyData):
    '''
    '''
    def __init__(self,fecha,hour = None):
        #DBStudyData.__init__(self)
        super(DBManagerStudyDataES,self).__init__(fecha,hour,'StudyDataES')

class DBManagerStudyDataPT(DBStudyData):
    '''
    '''
    def __init__(self,fecha,hour = None):
        #DBStudyData.__init__(self)
        super(DBManagerStudyDataPT,self).__init__(fecha,hour,'StudyDataPT')

class DBManagerStudyDataMIBEL(DBStudyData):
    '''
    '''
    def __init__(self,fecha,hour = None):
        #DBStudyData.__init__(self)
        super(DBManagerStudyDataMIBEL,self).__init__(fecha,hour,'StudyDataMIBEL')

