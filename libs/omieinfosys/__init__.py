# -*- coding: utf-8 -*-
#!/usr/bin/env python

__author__ = ("Hugo M. Marrao Rodrigues")
__version__ = "0.0.1"
__revision__ = "dev"

# from mongoengine import MongoEngine

CONN_DETAILS = {'db':'omieMercadoDiario'}

# db = MongoEngine()
import os
try:
    host = os.environ['OPENSHIFT_MONGODB_IP']
except:
    host = 'localhost'
#host = os.environ['MONGODB_URL'][:-1]+str(27017)+'/'
# host="127.3.118.130"
#host="priceprofor-ekergy.rhcloud.com"
# imports

from utilities import cambiohoraverano, cambiohorainvierno
from .omieMercadoDiarioWebParsers import PreciosMercadoDiarioHandler, TecnologiasMercadoDiarioHandler, EnergiaGestionadaMercadoDiarioHandler
from .omieMercadoDiarioDBManager import PreciosWeb, TecnologiasWeb, EnergiaGestionadaWeb, StudyDataES, StudyDataMIBEL
import datetime
from urllib2 import urlopen
from mongoengine.connection import get_db, connect

try:
    get_db(CONN_DETAILS['db'],reconnect=True)
except:
    connect(CONN_DETAILS['db'],host=host)



class NoUpdateNeeded(Exception):
    """
    """
    def __init__(self, value):
        self.value = ""
    def __str__(self):
        return repr(self.value)

def status():
    """Gives status on collections used by this module.

    """
    try:
        from omieinfosys import omieMercadoDiarioDBManager
    except:
        result = 'failed'
        raise
    else:
        precioswebstatus = omieMercadoDiarioDBManager.PreciosWeb.status

        tecnologiaswebstatus = omieMercadoDiarioDBManager.TecnologiasWeb.status

        studydatamibelstatus = omieMercadoDiarioDBManager.StudyDataMIBEL.status
        
        energiagestionadawebstatus = omieMercadoDiarioDBManager.EnergiaGestionadaWeb.status

        result = {'StudyDataMIBEL':studydatamibelstatus,
                  'PreciosWeb':precioswebstatus,
                  'TecnologiasWeb':tecnologiaswebstatus,
                  'EnergiaGestionadaWeb':energiagestionadawebstatus,}
    finally:
        return result

def updatedb():
    """Update current database for the 3 Collection so far managed:
    """
    try:
        populatepreciosweb()
        populatetecnologiasweb()
        populateenergiagestionadaweb()
        populatestudydatamibel()
    except:
        raise

def omiepreciosurl(fecha):
    """omiepreciosurl
    Builds the omie url that gives Mibel Daily prices
    
    doctest:
    ++++++++

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
    """
    URL_OMIE_DATOSPUB = 'http://www.omie.es/datosPub'
    URL_OMIE_PRECIOMARGINAL = URL_OMIE_DATOSPUB + '/' + 'marginalpdbc/marginalpdbc_'
    URL_FIN = '.1'
    try:
        fechaURL= fecha.strftime("%Y%m%d")
        # return result as a str.
        return URL_OMIE_PRECIOMARGINAL+fechaURL+URL_FIN
    except:
        raise

def omieenergiasurl(fecha):
    """omieenergiasurl
    Builds the omie url that gives Mibel Daily energy volumes negociated
    
    doctest:
    ++++++++

    """
    URL_OMIE_DATOSPUB = 'http://www.omie.es/datosPub'
    URL_OMIE_ENERGIA = URL_OMIE_DATOSPUB + '/' + 'pdbc_tot/pdbc_tot_'
    URL_FIN = '.1'
    try:
        fechaURL= fecha.strftime("%Y%m%d")
        # return result as a str.
        return URL_OMIE_ENERGIA+fechaURL+URL_FIN
    except:
        raise

def omietecnologiasurl(fecha):
    '''
    doctest
    '''
    URL_OMIE_DATOSPUB = 'http://www.omie.es/datosPub'
    URL_OMIE_TECNOLOGIAS_ACUMULADOS = URL_OMIE_DATOSPUB + '/' + 'pdbc_stota/pdbc_stota_'
    URL_FIN = '.1'
    try:
        fechaURL= fecha.strftime("%Y%m%d")
        # return result as a str.
        return URL_OMIE_TECNOLOGIAS_ACUMULADOS+fechaURL+URL_FIN
    except:
        raise
        

def preciosmercadodiarioparser(fecha):
    '''
    This is the main method so the usage of PreciosMibelHandler is more strainfoward.
    '''
    try:
        # TODO: validafecha(fecha)
        URL = omiepreciosurl(fecha)
        # print URL
        toparsePRECIOS = urlopen(URL)
    except:
        raise
    else:
        Precios = PreciosMercadoDiarioHandler(toparsePRECIOS)
        # print Precios.precioses
        # TODO: make this better code and also include .3 in the search path!
        if Precios.precioses == []:
            numero = '2'
            URL = omiepreciosurl(fecha)[:len(omiepreciosurl(fecha))-1]+str(numero)
            toparsePRECIOS = urlopen(URL)
            Precios = PreciosMercadoDiarioHandler(toparsePRECIOS)
            return {"PreciosMibel":Precios.preciospt,"PreciosES":Precios.precioses,"PreciosPT":Precios.preciosmibel}
        else:
            return {"PreciosMibel":Precios.preciospt,"PreciosES":Precios.precioses,"PreciosPT":Precios.preciosmibel}

def energiagestionadamercadodiarioparser(fecha):
    '''
    This is the main method so the usage of PreciosMibelHandler is more strainfoward.
    '''
    try:
        # TODO: validafecha(fecha)
        URL = omieenergiasurl(fecha)
        # print URL
        toparseEnergia = urlopen(URL)
    except:
        raise
    else:
        Energia = EnergiaGestionadaMercadoDiarioHandler(toparseEnergia)
        # print Precios.precioses
        # TODO: make this better code and also include .3 in the search path!
        if Energia.energiaes == []:
            numero = '2'
            URL = omiepreciosurl(fecha)[:len(omiepreciosurl(fecha))-1]+str(numero)
            toparseEnergia = urlopen(URL)
            Energia = EnergiaGestionadaMercadoDiarioHandler(toparseEnergia)
            return {"EnergiaMI":Energia.energiami,"EnergiaES":Energia.energiaes,"EnergiaPT":Energia.energiapt}
        else:
            return {"EnergiaMI":Energia.energiami,"EnergiaES":Energia.energiaes,"EnergiaPT":Energia.energiapt}

def tecnologiasmercadodiarioparser(fecha):
    '''
    This is the main method so the usage of PreciosMibelHandler is more strainfoward.
    '''
    try:
        # The marginalpdbc data have the Spanish and the Portuguese prices.
        toparsePRODUCCION = urlopen(omietecnologiasurl(fecha))
    except:
        raise
    else:
        tecnologias = TecnologiasMercadoDiarioHandler(toparsePRODUCCION)
        return {"ProduccionyDemandaMIBEL":tecnologias.ProduccionyDemandaMIBEL,"ProduccionyDemandaES":tecnologias.ProduccionyDemandaES,"ProduccionyDemandaPT":tecnologias.ProduccionyDemandaPT}


def populatepreciosweb(initfecha=None,endfecha=None):
    """
    This will populate data into mongo collection as delivered by omie web

    usage:: if is the first time then:


            if is only updateing then:


    """
    # by default initfecha = datetime.datetime(2012,1,1)
    def _check_args(initfecha,endfecha):
        """
        Function arguments validator
        """
        if initfecha is None:
            try:
                initfecha = PreciosWeb.lastdateindb
            except IndexError:
                print "No data in the collection! using 2011-1-1 as start date"
                initfecha = datetime.datetime(2010,12,31)
            finally:
                initfecha += datetime.timedelta(days=1)
        initfecha = initfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = datetime.datetime.now()
        if endfecha is None:
            if todaydatetime.hour > 14:
                endfecha = datetime.datetime.now()+datetime.timedelta(days=1)
                todaydatetime += datetime.timedelta(days=1)
            else:
                endfecha = datetime.datetime.now()
        endfecha = endfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = todaydatetime.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        if initfecha > todaydatetime:
            raise NoUpdateNeeded("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
        if initfecha > endfecha:
            raise ValueError("invalid dates given -->%s is bigger then -->%s"%(initfecha,endfecha))
        if endfecha > todaydatetime:
            raise ValueError("invalid dates given -->%s is bigger then -->%s \
which is the last available data in esios.ree.es "%(initfecha,todaydatetime))
        # Returning needed data as specified.
        return initfecha,endfecha
    try:
        # # Check inputs consistency:
        # if initfecha > endfecha:
        #     raise Exception("invalid dates given"+' '+str(endfecha)+' '+str(initfecha))
        
        # # first lets try to deduce the last available fecha at collection 
        # # if it is first run count should be empty
        # # else just get me the needed values!
        # initfecha=datetime.datetime(initfecha.year,initfecha.month,initfecha.day)
        # endfecha=datetime.datetime(endfecha.year,endfecha.month,endfecha.day,endfecha.hour)
        # nowfecha=datetime.datetime.now()
        # # Check if database already have data:
        # if PreciosWeb.numofrecords != 0:
        #     initfecha = PreciosWeb.lastdateindb
        #     initfecha += datetime.timedelta(days=1) 

        # # Handle todays date as defined:
        # if (endfecha.year == nowfecha.year) and (endfecha.month == nowfecha.month) and (endfecha.day == nowfecha.day):
        #     if endfecha.hour <= 13:
        #         endfecha=datetime.datetime(endfecha.year,endfecha.month,endfecha.day)
        #     else:
        #         endfecha=datetime.datetime(endfecha.year,endfecha.month,endfecha.day)
        #         endfecha = endfecha + datetime.timedelta(days=1)

        initfecha,endfecha = _check_args(initfecha,endfecha)
        # # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            preciosweb = preciosmercadodiarioparser(iterfecha)
            preciosindb = PreciosWeb.objects(fecha=iterfecha)
            if preciosindb.count() ==0:
                preciosdb = PreciosWeb(fecha=iterfecha)
            elif preciosindb.count() ==1:
                for p in preciosindb:
                    preciosdb = p
            preciosdb = PreciosWeb(fecha=iterfecha)
            preciosdb.PreciosMI = preciosweb["PreciosMibel"]
            preciosdb.PreciosES = preciosweb["PreciosES"]
            preciosdb.PreciosPT = preciosweb["PreciosPT"]
            preciosdb.save()
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del preciosdb,preciosweb
    except NoUpdateNeeded:
        print "Collection up to date"
    except:
        raise

def populateenergiagestionadaweb(initfecha=None,endfecha=None):
    """
    This will populate data into mongo collection as delivered by omie web

    usage:: if is the first time then:


            if is only updateing then:


    """
    # by default initfecha = datetime.datetime(2012,1,1)
    def _check_args(initfecha,endfecha):
        """
        Function arguments validator
        """
        if initfecha is None:
            try:
                initfecha = EnergiaGestionadaWeb.lastdateindb
            except IndexError:
                print "No data in the collection! using 2011-1-1 as start date"
                initfecha = datetime.datetime(2010,12,31)
            finally:
                initfecha += datetime.timedelta(days=1)
        initfecha = initfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = datetime.datetime.now()
        if endfecha is None:
            if todaydatetime.hour > 14:
                endfecha = datetime.datetime.now()+datetime.timedelta(days=1)
                todaydatetime += datetime.timedelta(days=1)
            else:
                endfecha = datetime.datetime.now()
        endfecha = endfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = todaydatetime.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        if initfecha > todaydatetime:
            raise NoUpdateNeeded("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
        if initfecha > endfecha:
            raise ValueError("invalid dates given -->%s is bigger then -->%s"%(initfecha,endfecha))
        if endfecha > todaydatetime:
            raise ValueError("invalid dates given -->%s is bigger then -->%s \
which is the last available data in esios.ree.es "%(initfecha,todaydatetime))
        # Returning needed data as specified.
        return initfecha,endfecha
    try:
        initfecha,endfecha = _check_args(initfecha,endfecha)
        # # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            energiaweb = energiagestionadamercadodiarioparser(iterfecha)
            energiaindb = EnergiaGestionadaWeb.objects(fecha=iterfecha)
            if energiaindb.count() ==0:
                energiadb = EnergiaGestionadaWeb(fecha=iterfecha)
            elif energiaindb.count() ==1:
                for p in preciosindb:
                    energiadb = p
            energiadb = EnergiaGestionadaWeb(fecha=iterfecha)
            energiadb.EnergiaMI = energiaweb['EnergiaMI']
            energiadb.EnergiaES = energiaweb['EnergiaES']
            energiadb.EnergiaPT = energiaweb['EnergiaPT']
            energiadb.save()
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del energiadb,energiaweb
    except NoUpdateNeeded:
        print "Collection up to date"
    except:
        raise

        

def populatetecnologiasweb(initfecha=None,endfecha=None):
    """
    This will populate data into mongo collection as delivered by omie web

    usage:: if is the first time then:


            if is only updateing then:


    """
    def _check_args(initfecha,endfecha):
        """
        Function arguments validator
        """
        if initfecha is None:
            try:
                initfecha = TecnologiasWeb.lastdateindb
            except IndexError:
                print "No data in the collection! using 2011-1-1 as start date"
                initfecha = datetime.datetime(2010,12,31)
            finally:
                initfecha += datetime.timedelta(days=1)
        initfecha = initfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = datetime.datetime.now()
        if endfecha is None:
            if todaydatetime.hour > 14:
                endfecha = datetime.datetime.now()-datetime.timedelta(days=2)
                todaydatetime -= datetime.timedelta(days=2)
            else:
                endfecha = datetime.datetime.now()-datetime.timedelta(days=3)
                todaydatetime -= datetime.timedelta(days=3)
        endfecha = endfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = todaydatetime.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        if initfecha > todaydatetime:
            raise NoUpdateNeeded("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
        if initfecha > endfecha:
            raise ValueError("invalid dates given -->%s is bigger then -->%s"%(initfecha,endfecha))
        if endfecha > todaydatetime:
            raise ValueError("invalid dates given -->%s is bigger then -->%s \
which is the last available data in esios.ree.es "%(initfecha,todaydatetime))
        # Returning needed data as specified.
        return initfecha,endfecha
    # by default initfecha = datetime.datetime(2012,1,1)
    try:
        # TODO: handle properly web availability of data!
        # Check inputs consistency:
        # if initfecha > endfecha:
        #     raise Exception("invalid dates given"+' '+str(endfecha)+' '+str(initfecha))
        
        # # first lets try to deduce the last available fecha at collection 
        # # if it is first run count should be empty
        # # else just get me the needed values!
        # initfecha=datetime.datetime(initfecha.year,initfecha.month,initfecha.day)
        # endfecha=datetime.datetime(endfecha.year,endfecha.month,endfecha.day,endfecha.hour)
        # nowfecha=datetime.datetime.now()
        # # Check if database already have data:
        # if TecnologiasWeb.numofrecords != 0:
        #     initfecha = TecnologiasWeb.lastdateindb
        #     initfecha += datetime.timedelta(days=1) 

        # # Handle todays date as defined:
        # if (endfecha.year == nowfecha.year) and (endfecha.month == nowfecha.month) and (endfecha.day == nowfecha.day):
        #     if endfecha.hour <= 13:
        #         endfecha=datetime.datetime(endfecha.year,endfecha.month,endfecha.day)
        #     else:
        #         endfecha=datetime.datetime(endfecha.year,endfecha.month,endfecha.day)
        #         endfecha = endfecha + datetime.timedelta(days=1)

        initfecha,endfecha = _check_args(initfecha,endfecha)
        # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            tecnologiasweb = tecnologiasmercadodiarioparser(iterfecha)
            tecnologiasindb = TecnologiasWeb.objects(fecha=iterfecha)
            if tecnologiasindb.count() ==0:
                tecnologiasdb = TecnologiasWeb(fecha=iterfecha)
            elif tecnologiasindb.count() ==1:
                for p in tecnologiasindb:
                    tecnologiasdb = p
            tecnologiasdb.ProduccionyDemandaMIBEL = tecnologiasweb["ProduccionyDemandaMIBEL"]
            tecnologiasdb.ProduccionyDemandaES = tecnologiasweb["ProduccionyDemandaES"]
            tecnologiasdb.ProduccionyDemandaPT = tecnologiasweb["ProduccionyDemandaPT"]
            tecnologiasdb.save()
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del tecnologiasdb
    except NoUpdateNeeded:
        print "Collection up to date"
    except:
        raise



def populatestudydataes():
    """
    utility to prepare data for study!
    """
    try:
        # else just get me the needed values!
        initfecha=datetime.datetime(2014,1,1)
        endfecha=datetime.datetime(2014,12,1)        
        # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            # Must include special dates like chang of time dates:
            preciosindb = PreciosWeb.objects(fecha=iterfecha)[0]
            tecnologiasindb = TecnologiasWeb.objects(fecha=iterfecha)[0]
            if cambiohoraverano(iterfecha.year) == iterfecha:
                # days with 23 hours: replicate hour 2 for 3
                for h in range(23):
                    if h == 2:
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                        studydataes = StudyDataES(fecha=iterfechaaux)
                        studydataes.precio = preciosindb.PreciosES[h]
                        studydataes.HIDRAULICA_CONVENCIONAL = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][h]
                        studydataes.HIDRAULICA_BOMBEO_PURO = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_BOMBEO_PURO'][h]
                        studydataes.NUCLEAR = tecnologiasindb.ProduccionyDemandaES['NUCLEAR'][h]
                        studydataes.CARBON_NACIONAL = tecnologiasindb.ProduccionyDemandaES['CARBON_NACIONAL'][h]
                        studydataes.CARBON_IMPORTACION = tecnologiasindb.ProduccionyDemandaES['CARBON_IMPORTACION'][h]
                        studydataes.CICLO_COMBINADO = tecnologiasindb.ProduccionyDemandaES['CICLO_COMBINADO'][h]
                        studydataes.save()

                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h+1)
                        studydataes = StudyDataES(fecha=iterfechaaux)
                        studydataes.precio = preciosindb.PreciosES[h]
                        studydataes.HIDRAULICA_CONVENCIONAL = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][h]
                        studydataes.HIDRAULICA_BOMBEO_PURO = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_BOMBEO_PURO'][h]
                        studydataes.NUCLEAR = tecnologiasindb.ProduccionyDemandaES['NUCLEAR'][h]
                        studydataes.CARBON_NACIONAL = tecnologiasindb.ProduccionyDemandaES['CARBON_NACIONAL'][h]
                        studydataes.CARBON_IMPORTACION = tecnologiasindb.ProduccionyDemandaES['CARBON_IMPORTACION'][h]
                        studydataes.CICLO_COMBINADO = tecnologiasindb.ProduccionyDemandaES['CICLO_COMBINADO'][h]
                        studydataes.save()
                    elif h >= 3:
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h+1)
                        studydataes = StudyDataES(fecha=iterfechaaux)
                        studydataes.precio = preciosindb.PreciosES[h]
                        studydataes.HIDRAULICA_CONVENCIONAL = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][h]
                        studydataes.HIDRAULICA_BOMBEO_PURO = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_BOMBEO_PURO'][h]
                        studydataes.NUCLEAR = tecnologiasindb.ProduccionyDemandaES['NUCLEAR'][h]
                        studydataes.CARBON_NACIONAL = tecnologiasindb.ProduccionyDemandaES['CARBON_NACIONAL'][h]
                        studydataes.CARBON_IMPORTACION = tecnologiasindb.ProduccionyDemandaES['CARBON_IMPORTACION'][h]
                        studydataes.CICLO_COMBINADO = tecnologiasindb.ProduccionyDemandaES['CICLO_COMBINADO'][h]
                        studydataes.save()
                    else:
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                        studydataes = StudyDataES(fecha=iterfechaaux)
                        studydataes.precio = preciosindb.PreciosES[h]
                        studydataes.HIDRAULICA_CONVENCIONAL = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][h]
                        studydataes.HIDRAULICA_BOMBEO_PURO = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_BOMBEO_PURO'][h]
                        studydataes.NUCLEAR = tecnologiasindb.ProduccionyDemandaES['NUCLEAR'][h]
                        studydataes.CARBON_NACIONAL = tecnologiasindb.ProduccionyDemandaES['CARBON_NACIONAL'][h]
                        studydataes.CARBON_IMPORTACION = tecnologiasindb.ProduccionyDemandaES['CARBON_IMPORTACION'][h]
                        studydataes.CICLO_COMBINADO = tecnologiasindb.ProduccionyDemandaES['CICLO_COMBINADO'][h]
                        studydataes.save()
                    del studydataes
            elif cambiohorainvierno(iterfecha.year) == iterfecha:
                # days with 25 hours: elimitate hour 3
                for h in range(25):
                    if h < 2:
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                        studydataes = StudyDataES(fecha=iterfechaaux)
                        studydataes.precio = preciosindb.PreciosES[h]
                        studydataes.HIDRAULICA_CONVENCIONAL = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][h]
                        studydataes.HIDRAULICA_BOMBEO_PURO = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_BOMBEO_PURO'][h]
                        studydataes.NUCLEAR = tecnologiasindb.ProduccionyDemandaES['NUCLEAR'][h]
                        studydataes.CARBON_NACIONAL = tecnologiasindb.ProduccionyDemandaES['CARBON_NACIONAL'][h]
                        studydataes.CARBON_IMPORTACION = tecnologiasindb.ProduccionyDemandaES['CARBON_IMPORTACION'][h]
                        studydataes.CICLO_COMBINADO = tecnologiasindb.ProduccionyDemandaES['CICLO_COMBINADO'][h]
                        studydataes.save()
                    elif h > 2:
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h-1)
                        studydataes = StudyDataES(fecha=iterfechaaux)
                        studydataes.precio = preciosindb.PreciosES[h-1]
                        studydataes.HIDRAULICA_CONVENCIONAL = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][h+1]
                        studydataes.HIDRAULICA_BOMBEO_PURO = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_BOMBEO_PURO'][h+1]
                        studydataes.NUCLEAR = tecnologiasindb.ProduccionyDemandaES['NUCLEAR'][h+1]
                        studydataes.CARBON_NACIONAL = tecnologiasindb.ProduccionyDemandaES['CARBON_NACIONAL'][h+1]
                        studydataes.CARBON_IMPORTACION = tecnologiasindb.ProduccionyDemandaES['CARBON_IMPORTACION'][h+1]
                        studydataes.CICLO_COMBINADO = tecnologiasindb.ProduccionyDemandaES['CICLO_COMBINADO'][h+1]
                        studydataes.save()
                    del studydataes
            else:
                # process Normal
                for h in range(24):
                    iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                    studydataes = StudyDataES(fecha=iterfechaaux)
                    studydataes.precio = preciosindb.PreciosES[h]
                    studydataes.HIDRAULICA_CONVENCIONAL = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][h]
                    studydataes.HIDRAULICA_BOMBEO_PURO = tecnologiasindb.ProduccionyDemandaES['HIDRAULICA_BOMBEO_PURO'][h]
                    studydataes.NUCLEAR = tecnologiasindb.ProduccionyDemandaES['NUCLEAR'][h]
                    studydataes.CARBON_NACIONAL = tecnologiasindb.ProduccionyDemandaES['CARBON_NACIONAL'][h]
                    studydataes.CARBON_IMPORTACION = tecnologiasindb.ProduccionyDemandaES['CARBON_IMPORTACION'][h]
                    studydataes.CICLO_COMBINADO = tecnologiasindb.ProduccionyDemandaES['CICLO_COMBINADO'][h]
                    studydataes.save()
                    del studydataes
            del preciosindb, tecnologiasindb
            iterfecha = iterfecha + datetime.timedelta(days=1)
    except:
        raise

def populatestudydatapt():
    """

    """
    try:
        # else just get me the needed values!
        initfecha=datetime.datetime(2014,6,1)
        endfecha=datetime.datetime(2014,7,1)        
        # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            preciosindb = PreciosWeb.objects(fecha=iterfecha)[0]

            tecnologiasindb = TecnologiasWeb.objects(fecha=iterfecha)[0]
            for h in range(24):
                iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                studydataes = StudyDataES(fecha=iterfechaaux)
                studydataes.year = iterfecha.year
                studydataes.month = iterfecha.month
                studydataes.day = iterfecha.day
                studydataes.hour = h
                studydataes.precio = preciosindb.PreciosPT[h]
                studydataes.NUCLEAR = tecnologiasindb.ProduccionyDemandaPT['NUCLEAR'][h]
                studydataes.save()
                del studydataes
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del preciosindb, tecnologiasindb
    except:
        raise


def populatestudydatamibel(initfecha=None,endfecha=None):
    """Populate the StudyDataMIBEL Collection using StudyDataMIBEL class.

    It gets data from PreciosWeb and TecnologiasWeb so before executing you
    should check that those collections are properly populated.

    Args: (optional)
        initfecha (datetime): starting date to perform population
        endfecha (datetime): end date to perform population

    Returns:
        Nothing
        raise Exception if some problem occur

    Usage:
    Check that you local mongo db instance is running
    >>> import omieinfosys
    >>> omieinfosys..populatestudydatamibel


    utility to prepare data for study!
    '940':'RESUMEN_DE_PRODUCCION_MIBEL',
    '941':'TOTAL_HIDRAULICA_(901+902)',
    '942':'TOTAL_TERMICA_(903+904+905+906+907+908)',
    '943':'TOTAL_REGIMEN_ESPECIAL_(909+910)',
    '944':'TOTAL_IMPORTACION_(911+912+914+915)',
    '945':'TOTAL_GENERICAS_(916+917)',
    '949':'TOTAL_PRODUCCION_MIBEL',
    '950':'RESUMEN_DE_DEMANDA_MIBEL',
    '951':'TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)',
    '952':'TOTAL_CONSUMO_BOMBEO_(924)',
    '953':'TOTAL_EXPORTACIONES_(925+926+928+929)',
    '954':'TOTAL_GENERICAS_(930+931)',
    '959':'TOTAL_DEMANDA_MIBEL',
    """
    def _check_args(initfecha,endfecha):
        """
        Function arguments validator
        """
        if initfecha is None:
            try:
                initfecha = StudyDataMIBEL.lastdateindb
            except IndexError:
                print "No data in the collection! using 2011-1-1 as start date"
                initfecha = datetime.datetime(2010,12,31)
            finally:
                initfecha += datetime.timedelta(days=1)
        initfecha = initfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = datetime.datetime.now()
        if endfecha is None:
            if todaydatetime.hour > 14:
                endfecha = datetime.datetime.now()-datetime.timedelta(days=2)
                todaydatetime -= datetime.timedelta(days=2)
            else:
                endfecha = datetime.datetime.now()-datetime.timedelta(days=3)
                todaydatetime -= datetime.timedelta(days=3)
        endfecha = endfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = todaydatetime.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        if initfecha > todaydatetime:
            raise NoUpdateNeeded("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
        if initfecha > endfecha:
            raise ValueError("invalid dates given -->%s is bigger then -->%s"%(initfecha,endfecha))
        if endfecha > todaydatetime:
            raise ValueError("invalid dates given -->%s is bigger then -->%s \
which is the last available data in esios.ree.es "%(initfecha,todaydatetime))
        # Returning needed data as specified.
        return initfecha,endfecha
    try:
        initfecha,endfecha = _check_args(initfecha,endfecha)
        # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            # Must include special dates like chang of time dates:
            preciosindb = PreciosWeb.objects(fecha=iterfecha)[0]
            tecnologiasindb = TecnologiasWeb.objects(fecha=iterfecha)[0]
            if cambiohoraverano(iterfecha.year) == iterfecha:
                # days with 23 hours: replicate hour 2 for 3
                for h in range(23):
                    if h == 2:
                        # Fecha
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                        studydatamibel = StudyDataMIBEL(fecha=iterfechaaux)
                        # Precio
                        studydatamibel.precio = preciosindb.PreciosMI[h]
                        # Produccion
                        studydatamibel.P_TOTAL_HIDRAULICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_HIDRAULICA_(901+902)'][h]
                        studydatamibel.P_TOTAL_TERMICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_TERMICA_(903+904+905+906+907+908)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ESPECIAL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ESPECIAL_(909+910)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ORDINARIO_CON_PRIMA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ORDINARIO_CON_PRIMA'][h]
                        studydatamibel.P_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.P_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(916+917)'][h]
                        studydatamibel.P_TOTAL_PRODUCCION_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_PRODUCCION_MIBEL'][h]
                        # Demanda
                        studydatamibel.D_TOTAL_DEMANDA_NACIONAL_CLIENTES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)'][h]
                        studydatamibel.D_TOTAL_CONSUMO_BOMBEO = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_CONSUMO_BOMBEO_(924)'][h]
                        studydatamibel.D_TOTAL_EXPORTACIONES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_EXPORTACIONES_(925+926+928+929)'][h]
                        studydatamibel.D_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.D_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(930+931)'][h]
                        studydatamibel.D_TOTAL_DEMANDA_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_MIBEL'][h]
                        studydatamibel.save()

                        # Fecha
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h+1)
                        studydatamibel = StudyDataMIBEL(fecha=iterfechaaux)
                        # Precio
                        studydatamibel.precio = preciosindb.PreciosMI[h]
                        studydatamibel.P_TOTAL_HIDRAULICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_HIDRAULICA_(901+902)'][h]
                        studydatamibel.P_TOTAL_TERMICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_TERMICA_(903+904+905+906+907+908)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ESPECIAL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ESPECIAL_(909+910)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ORDINARIO_CON_PRIMA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ORDINARIO_CON_PRIMA'][h]
                        studydatamibel.P_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.P_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(916+917)'][h]
                        studydatamibel.P_TOTAL_PRODUCCION_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_PRODUCCION_MIBEL'][h]
                        # Demanda
                        studydatamibel.D_TOTAL_DEMANDA_NACIONAL_CLIENTES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)'][h]
                        studydatamibel.D_TOTAL_CONSUMO_BOMBEO = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_CONSUMO_BOMBEO_(924)'][h]
                        studydatamibel.D_TOTAL_EXPORTACIONES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_EXPORTACIONES_(925+926+928+929)'][h]
                        studydatamibel.D_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.D_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(930+931)'][h]
                        studydatamibel.D_TOTAL_DEMANDA_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_MIBEL'][h]
                        studydatamibel.save()
                    elif h >= 3:
                        # Fecha
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h+1)
                        studydatamibel = StudyDataMIBEL(fecha=iterfechaaux)
                        # Precio
                        studydatamibel.precio = preciosindb.PreciosMI[h]
                        studydatamibel.P_TOTAL_HIDRAULICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_HIDRAULICA_(901+902)'][h]
                        studydatamibel.P_TOTAL_TERMICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_TERMICA_(903+904+905+906+907+908)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ESPECIAL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ESPECIAL_(909+910)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ORDINARIO_CON_PRIMA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ORDINARIO_CON_PRIMA'][h]
                        studydatamibel.P_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.P_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(916+917)'][h]
                        studydatamibel.P_TOTAL_PRODUCCION_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_PRODUCCION_MIBEL'][h]
                        # Demanda
                        studydatamibel.D_TOTAL_DEMANDA_NACIONAL_CLIENTES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)'][h]
                        studydatamibel.D_TOTAL_CONSUMO_BOMBEO = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_CONSUMO_BOMBEO_(924)'][h]
                        studydatamibel.D_TOTAL_EXPORTACIONES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_EXPORTACIONES_(925+926+928+929)'][h]
                        studydatamibel.D_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.D_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(930+931)'][h]
                        studydatamibel.D_TOTAL_DEMANDA_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_MIBEL'][h]
                        studydatamibel.save()
                    else:
                        # Fecha
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                        studydatamibel = StudyDataMIBEL(fecha=iterfechaaux)
                        # Precio
                        studydatamibel.precio = preciosindb.PreciosMI[h]
                        studydatamibel.P_TOTAL_HIDRAULICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_HIDRAULICA_(901+902)'][h]
                        studydatamibel.P_TOTAL_TERMICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_TERMICA_(903+904+905+906+907+908)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ESPECIAL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ESPECIAL_(909+910)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ORDINARIO_CON_PRIMA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ORDINARIO_CON_PRIMA'][h]
                        studydatamibel.P_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.P_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(916+917)'][h]
                        studydatamibel.P_TOTAL_PRODUCCION_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_PRODUCCION_MIBEL'][h]
                        # Demanda
                        studydatamibel.D_TOTAL_DEMANDA_NACIONAL_CLIENTES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)'][h]
                        studydatamibel.D_TOTAL_CONSUMO_BOMBEO = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_CONSUMO_BOMBEO_(924)'][h]
                        studydatamibel.D_TOTAL_EXPORTACIONES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_EXPORTACIONES_(925+926+928+929)'][h]
                        studydatamibel.D_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.D_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(930+931)'][h]
                        studydatamibel.D_TOTAL_DEMANDA_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_MIBEL'][h]
                        studydatamibel.save()
                    del studydatamibel
            elif cambiohorainvierno(iterfecha.year) == iterfecha:
                # days with 25 hours: elimitate hour 3
                for h in range(25):
                    if h < 2:
                        # Fecha
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                        studydatamibel = StudyDataMIBEL(fecha=iterfechaaux)
                        # Precio
                        studydatamibel.precio = preciosindb.PreciosMI[h]
                        studydatamibel.P_TOTAL_HIDRAULICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_HIDRAULICA_(901+902)'][h]
                        studydatamibel.P_TOTAL_TERMICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_TERMICA_(903+904+905+906+907+908)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ESPECIAL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ESPECIAL_(909+910)'][h]
                        studydatamibel.P_TOTAL_REGIMEN_ORDINARIO_CON_PRIMA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ORDINARIO_CON_PRIMA'][h]
                        studydatamibel.P_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.P_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(916+917)'][h]
                        studydatamibel.P_TOTAL_PRODUCCION_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_PRODUCCION_MIBEL'][h]
                        # Demanda
                        studydatamibel.D_TOTAL_DEMANDA_NACIONAL_CLIENTES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)'][h]
                        studydatamibel.D_TOTAL_CONSUMO_BOMBEO = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_CONSUMO_BOMBEO_(924)'][h]
                        studydatamibel.D_TOTAL_EXPORTACIONES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_EXPORTACIONES_(925+926+928+929)'][h]
                        studydatamibel.D_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                        studydatamibel.D_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(930+931)'][h]
                        studydatamibel.D_TOTAL_DEMANDA_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_MIBEL'][h]
                        studydatamibel.save()
                    elif h > 2:
                        # Fecha
                        iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h-1)
                        studydatamibel = StudyDataMIBEL(fecha=iterfechaaux)
                        # Precio
                        studydatamibel.precio = preciosindb.PreciosMI[h-1]
                        studydatamibel.P_TOTAL_HIDRAULICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_HIDRAULICA_(901+902)'][h-1]
                        studydatamibel.P_TOTAL_TERMICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_TERMICA_(903+904+905+906+907+908)'][h-1]
                        studydatamibel.P_TOTAL_REGIMEN_ESPECIAL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ESPECIAL_(909+910)'][h-1]
                        studydatamibel.P_TOTAL_REGIMEN_ORDINARIO_CON_PRIMA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ORDINARIO_CON_PRIMA'][h-1]
                        studydatamibel.P_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h-1]
                        studydatamibel.P_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(916+917)'][h-1]
                        studydatamibel.P_TOTAL_PRODUCCION_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_PRODUCCION_MIBEL'][h-1]
                        # Demanda
                        studydatamibel.D_TOTAL_DEMANDA_NACIONAL_CLIENTES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)'][h-1]
                        studydatamibel.D_TOTAL_CONSUMO_BOMBEO = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_CONSUMO_BOMBEO_(924)'][h-1]
                        studydatamibel.D_TOTAL_EXPORTACIONES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_EXPORTACIONES_(925+926+928+929)'][h-1]
                        studydatamibel.D_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h-1]
                        studydatamibel.D_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(930+931)'][h-1]
                        studydatamibel.D_TOTAL_DEMANDA_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_MIBEL'][h-1]
                        studydatamibel.save()
                    else:
                        # do not do  anything
                        studydatamibel = 'empty'
                    del studydatamibel
            else:
                # process Normal
                for h in range(24):
                    # Fecha
                    iterfechaaux = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                    studydatamibel = StudyDataMIBEL(fecha=iterfechaaux)
                    # Precio
                    studydatamibel.precio = preciosindb.PreciosMI[h]
                    studydatamibel.P_TOTAL_HIDRAULICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_HIDRAULICA_(901+902)'][h]
                    studydatamibel.P_TOTAL_TERMICA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_TERMICA_(903+904+905+906+907+908)'][h]
                    studydatamibel.P_TOTAL_REGIMEN_ESPECIAL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ESPECIAL_(909+910)'][h]
                    studydatamibel.P_TOTAL_REGIMEN_ORDINARIO_CON_PRIMA = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_REGIMEN_ORDINARIO_CON_PRIMA'][h]
                    studydatamibel.P_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                    studydatamibel.P_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(916+917)'][h]
                    studydatamibel.P_TOTAL_PRODUCCION_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_PRODUCCION_MIBEL'][h]
                    # Demanda
                    studydatamibel.D_TOTAL_DEMANDA_NACIONAL_CLIENTES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)'][h]
                    studydatamibel.D_TOTAL_CONSUMO_BOMBEO = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_CONSUMO_BOMBEO_(924)'][h]
                    studydatamibel.D_TOTAL_EXPORTACIONES = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_EXPORTACIONES_(925+926+928+929)'][h]
                    studydatamibel.D_TOTAL_IMPORTACION = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_IMPORTACION_(911+912+914+915)'][h]
                    studydatamibel.D_TOTAL_GENERICAS = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_GENERICAS_(930+931)'][h]
                    studydatamibel.D_TOTAL_DEMANDA_MIBEL = tecnologiasindb.ProduccionyDemandaMIBEL['TOTAL_DEMANDA_MIBEL'][h]
                    studydatamibel.save()
                    del studydatamibel
            del preciosindb, tecnologiasindb
            iterfecha = iterfecha + datetime.timedelta(days=1)
    except NoUpdateNeeded:
        print "Collection up to date"
    except:
        raise