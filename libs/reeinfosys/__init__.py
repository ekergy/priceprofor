# -*- coding: utf-8 -*-
#!/usr/bin/env python
# TODO: Add parsers prior to 2014.
# TODO: Fiz saldos in Programa.
# TODO: Add reeHandlersParsers.py to merge all ree*Parser.
# TODO: Add correct unittest to the last specified values.

__author__ = ("Hugo M. Marrao Rodrigues")
__version__ = "0.0.1"
__revision__ = "dev"

CONN_DETAILS = {'db':'reeMercadoDiario'}

import datetime
from .reeMercadoDiarioWebParsers import ContratacionBilateralHandler, ProgramaBaseFuncHandler, PrevEolHandler, PrevDemandaHandler, EnergiaGestionadaHandler, PreciosHandler
from .reeMercadoDiarioBDManager import PrevDemandaWeb, PrevEolWeb, EnergiaGestionadaWeb, TecnologiasPBFWeb, TecnologiasCBLWeb, PreciosWeb, StudyDataES
from utilities import unicodetodecimal
import datetime
from xml.sax import handler, make_parser
from urllib2 import urlopen

from mongoengine.connection import get_db, connect, get_connection

try:
    get_db(CONN_DETAILS['db'],reconnect=True)
except:
    connect(CONN_DETAILS['db'])

def updatedb():
    """Update current database for the 3 Collection so far managed:
    """
    try:
        populatepreciosweb()
        populateprevdemandaweb()
        populatepreveolweb()
        populateenergiagestionadaweb()
        populatetecnologiascblweb()
        populatetecnologiaspbfweb()
    except:
        raise

def esiosreeurl(fecha=None, xmlid=None):
    URL_ESIOS_REE = "http://www.esios.ree.es/Solicitar/"
    ESIOSREEURLSXMLIDS = ["preveol_DD",
                          "demanda_aux",
                          "BAL_PBF_DD",
                          "CBF_PBF_DD",
                          "DEM_PBF_DD",
                          "MD_EGEST_DD",
                          "MD_PREC_DD"]
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
        # validafecha(fecha)
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

def reecontratacionbilateralparser(fecha):
    '''
    function to simplify PrevDemandaHandler usage
    TODO: here we should put into evidence the difference between <2013 and 2014
    '''
    try:
        # validafecha(fecha)
        url = esiosreeurl(fecha, xmlid="CBF_PBF_DD")
        infile = urlopen(url)
        parser = make_parser()
        handler = ContratacionBilateralHandler()
        parser.setContentHandler(handler)
        parser.parse(infile)
    except:
        raise
    else:
        return handler.parsingresults

def reeprogramabasefuncparser(fecha):
    '''
    function to simplify PrevDemandaHandler usage
    TODO: here we should put into evidence the difference between <2013 and 2014
    '''
    try:
        # validafecha(fecha)
        url = esiosreeurl(fecha, xmlid="BAL_PBF_DD")
        infile = urlopen(url)
        parser = make_parser()
        handler = ProgramaBaseFuncHandler()
        parser.setContentHandler(handler)
        parser.parse(infile)
    except:
        raise
    else:
        return handler.parsingresults

def reepreveolparser(fecha):
    '''
    function to simplify PreveolddHandler usage
    '''
    try:
        # validafecha(fecha)
        url = esiosreeurl(fecha, xmlid="preveol_DD")
        infile = urlopen(url)
        parser = make_parser()
        handler = PrevEolHandler()
        parser.setContentHandler(handler)
        parser.parse(infile)
    except:
        raise
    else:
        return handler.listavalores

def reeprevdemandaparser(fecha):
    '''
    function to simplify PrevDemandaHandler usage
    '''
    try:
        # validafecha(fecha)
        url = esiosreeurl(fecha, xmlid="demanda_aux")
        infile = urlopen(url)
        parser = make_parser()
        handler = PrevDemandaHandler()
        parser.setContentHandler(handler)
        parser.parse(infile)
    except:
        raise
    else:
        return handler.listavalores

def reeenergiagestionadaparser(fecha):
    '''
    function to simplify PrevDemandaHandler usage
    '''
    try:
        # validafecha(fecha)
        url = esiosreeurl(fecha, xmlid="MD_EGEST_DD")
        infile = urlopen(url)
        parser = make_parser()
        handler = EnergiaGestionadaHandler()
        parser.setContentHandler(handler)
        parser.parse(infile)
    except:
        raise
    else:
        return handler.listavalores

def reepreciosparser(fecha):
    '''
    function to simplify PrevDemandaHandler usage
    '''
    try:
        # validafecha(fecha)
        url = esiosreeurl(fecha, xmlid="MD_PREC_DD")
        infile = urlopen(url)
        parser = make_parser()
        handler = PreciosHandler()
        parser.setContentHandler(handler)
        parser.parse(infile)
    except:
        raise
    else:
        return handler.listavalores
   
def populateprevdemandaweb(initfecha=None,endfecha=None):
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
                initfecha = PrevDemandaWeb.lastdateindb
            except IndexError:
                print "No data in the collection! using 2011-1-1 as start date"
                initfecha = datetime.datetime(2010,12,31)
            finally:
                initfecha += datetime.timedelta(days=1)
        initfecha = initfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = datetime.datetime.now()
        if endfecha is None:
            if todaydatetime.hour > 14:
                endfecha = datetime.datetime.now()+datetime.timedelta(days=8)
                todaydatetime += datetime.timedelta(days=8)
            else:
                endfecha = datetime.datetime.now()++datetime.timedelta(days=7)
                todaydatetime += datetime.timedelta(days=7)
        endfecha = endfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = todaydatetime.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        if initfecha > todaydatetime:
            raise ValueError("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
        if initfecha > endfecha:
            raise ValueError("invalid dates given -->%s is bigger then -->%s"%(initfecha,endfecha))
        if endfecha > todaydatetime:
            raise ValueError("invalid dates given -->%s is bigger then -->%s \
which is the last available data in esios.ree.es "%(initfecha,todaydatetime))
        # Returning needed data as specified.
        return initfecha,endfecha
    try:
        # set proper data:
        initfecha,endfecha = _check_args(initfecha,endfecha)
        # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            prevdemandaweb = reeprevdemandaparser(iterfecha)
            prevdemandaindb = PrevDemandaWeb.objects(fecha=iterfecha)
            if prevdemandaindb.count() ==0:
                prevdemandadb = PrevDemandaWeb(fecha=iterfecha)
            elif prevdemandaindb.count() ==1:
                for p in prevdemandaindb:
                    prevdemandadb = p
            prevdemandadb.PrevDemanda = prevdemandaweb
            prevdemandadb.save()
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del prevdemandadb, prevdemandaweb, prevdemandaindb
    except:
        raise

def populatepreveolweb(initfecha=None,endfecha=None):
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
                initfecha = PrevEolWeb.lastdateindb
            except IndexError:
                print "No data in the collection! using 2011-1-1 as start date"
            finally:
                initfecha = datetime.datetime(2010,12,31)
                initfecha += datetime.timedelta(days=1)
        initfecha = initfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = datetime.datetime.now()
        if endfecha is None:
            if todaydatetime.hour > 14:
                endfecha = datetime.datetime.now()+datetime.timedelta(days=2)
                todaydatetime += datetime.timedelta(days=2)
            else:
                endfecha = datetime.datetime.now()+datetime.timedelta(days=1)
                todaydatetime += datetime.timedelta(days=1)
        endfecha = endfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        todaydatetime = todaydatetime.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        if initfecha > todaydatetime:
            raise ValueError("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
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
            preveolweb = reepreveolparser(iterfecha)
            preveolindb = PrevEolWeb.objects(fecha=iterfecha)
            if preveolindb.count() ==0:
                preveoldb = PrevEolWeb(fecha=iterfecha)
            elif preveolindb.count() ==1:
                for p in preveolindb:
                    preveoldb = p
            preveoldb.PrevEol = preveolweb
            preveoldb.save()
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del preveoldb, preveolweb, preveolindb
    except:
        raise

def populateenergiagestionadaweb(initfecha=None,endfecha=None):
    """
    This will populate data into mongo collection as delivered by omie web

    usage:: if is the first time then:


        if is only updateing then:

    > Note: esios.ree.es have energia gestionada data since 2011-1-1
    """
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
            raise ValueError("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
        if initfecha > endfecha:
            raise ValueError("invalid dates given -->%s is bigger then -->%s"%(initfecha,endfecha))
        if endfecha > todaydatetime:
            raise ValueError("invalid dates given -->%s is bigger then -->%s \
which is the last available data in esios.ree.es "%(initfecha,todaydatetime))
        # Returning needed data as specified.
        return initfecha,endfecha
    try:
        # reformat and check arguments
        initfecha,endfecha = _check_args(initfecha,endfecha)
        # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            energiagestionadaweb = reeenergiagestionadaparser(iterfecha)
            energiagestionadaindb = EnergiaGestionadaWeb.objects(fecha=iterfecha)
            if energiagestionadaindb.count() ==0:
                energiagestionadadb = EnergiaGestionadaWeb(fecha=iterfecha)
            elif energiagestionadaindb.count() ==1:
                for p in energiagestionadaindb:
                    energiagestionadadb = p
            energiagestionadadb.EnergiaGestionada = energiagestionadaweb
            energiagestionadadb.save()
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del energiagestionadadb, energiagestionadaweb, energiagestionadaindb
    except:
        raise

def populatetecnologiaspbfweb(initfecha=datetime.datetime(2012,1,1),endfecha=datetime.datetime.now()+datetime.timedelta(days=1)):
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
                initfecha = TecnologiasPBFWeb.lastdateindb
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
            raise ValueError("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
        if initfecha > endfecha:
            raise ValueError("invalid dates given -->%s is bigger then -->%s"%(initfecha,endfecha))
        if endfecha > todaydatetime:
            raise ValueError("invalid dates given -->%s is bigger then -->%s \
which is the last available data in esios.ree.es "%(initfecha,todaydatetime))
        # Returning needed data as specified.
        return initfecha,endfecha
    try:
        initfecha,endfecha = _check_args(initfecha,endfecha)
        # Check if database already have data:
        if TecnologiasPBFWeb.numofrecords != 0:
            initfecha = TecnologiasPBFWeb.lastdateindb
            initfecha += datetime.timedelta(days=1) 

        # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            tecnologiaspbfweb = reeprogramabasefuncparser(iterfecha)
            tecnologiaspbfindb = TecnologiasPBFWeb.objects(fecha=iterfecha)
            if tecnologiaspbfindb.count() ==0:
                tecnologiaspbfdb = TecnologiasPBFWeb(fecha=iterfecha)
            elif tecnologiaspbfindb.count() ==1:
                for p in tecnologiaspbfindb:
                    tecnologiaspbfdb = p
            tecnologiaspbfdb.TecnologiasPBF = tecnologiaspbfweb
            tecnologiaspbfdb.save()
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del tecnologiaspbfdb, tecnologiaspbfweb, tecnologiaspbfindb
    except:
        raise

def populatetecnologiascblweb(initfecha=datetime.datetime(2012,1,1),endfecha=datetime.datetime.now()+datetime.timedelta(days=1)):
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
                initfecha = TecnologiasCBLWeb.lastdateindb
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
            raise ValueError("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
        if initfecha > endfecha:
            raise ValueError("invalid dates given -->%s is bigger then -->%s"%(initfecha,endfecha))
        if endfecha > todaydatetime:
            raise ValueError("invalid dates given -->%s is bigger then -->%s \
which is the last available data in esios.ree.es "%(initfecha,todaydatetime))
        # Returning needed data as specified.
        return initfecha,endfecha
    try:
        initfecha,endfecha = _check_args(initfecha,endfecha)
        # Check if database already have data:
        if TecnologiasCBLWeb.numofrecords != 0:
            initfecha = TecnologiasCBLWeb.lastdateindb
            initfecha += datetime.timedelta(days=1) 

        # updatedata if needed:
        iterfecha = initfecha
        while iterfecha <= endfecha:
            tecnologiascblweb = reecontratacionbilateralparser(iterfecha)
            tecnologiascblindb = TecnologiasCBLWeb.objects(fecha=iterfecha)
            if tecnologiascblindb.count() ==0:
                tecnologiascbldb = TecnologiasCBLWeb(fecha=iterfecha)
            elif tecnologiascblindb.count() ==1:
                for p in tecnologiascblindb:
                    tecnologiascbldb = p
            tecnologiascbldb.TecnologiasCBL = tecnologiascblweb
            tecnologiascbldb.save()
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del tecnologiascbldb, tecnologiascblweb, tecnologiascblindb
    except:
        raise

def populatepreciosweb(initfecha=None,endfecha=None):
    """
    This will populate data into mongo collection as delivered by omie web

    usage:: if is the first time then:

        if is only updateing then:
    > Note: esios.ree.es have price data since 2011-1-1
    """
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
            raise ValueError("Collection is probably up to date -->%s -->%s"%(initfecha,endfecha))
        if initfecha > endfecha:
            raise ValueError("invalid dates given -->%s is bigger then -->%s"%(initfecha,endfecha))
        if endfecha > todaydatetime:
            raise ValueError("invalid dates given -->%s is bigger then -->%s \
which is the last available data in esios.ree.es "%(initfecha,todaydatetime))
        # Returning needed data as specified.
        return initfecha,endfecha
    try:
        initfecha,endfecha = _check_args(initfecha,endfecha)
        iterfecha = initfecha
        while iterfecha <= endfecha:
            preciosweb = reepreciosparser(iterfecha)
            preciosindb = PreciosWeb.objects(fecha=iterfecha)
            if preciosindb.count() ==0:
                preciosdb = PreciosWeb(fecha=iterfecha)
            elif preciosindb.count() ==1:
                for p in preciosindb:
                    preciosdb = p
            preciosdb.PreciosES = preciosweb
            preciosdb.save()
            iterfecha = iterfecha + datetime.timedelta(days=1)
            del preciosdb, preciosweb, preciosindb
    except:
        raise

def populatestudydataes(initfecha=None,endfecha=None):
    """
    This will populate data into mongo collection as delivered by omie web

    This populate data should manage the 23 and 25 hour conflict.

    usage:: if is the first time then:


        if is only updateing then:

    """
    # by default initfecha = datetime.datetime(2012,1,1)
    if initfecha is None:
        # if no initfecha is given one must use the PreciosWeb.lastdateindb
        initfecha = PreciosWeb.lastdateindb
        if initfecha is None:
            print "No data in the collection!"
        initfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
    if endfecha is None:
        todaydatetime = datetime.datetime.now()
        if todaydatetime.hour > 14:
            endfecha = datetime.datetime.now()+datetime.timedelta(days=1)
        else:
            endfecha = datetime.datetime.now()
        endfecha.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
    # after setting the inputs dates, it must make sure that raw data is available:
    try:
        # Check inputs consistency:
        if initfecha > endfecha:
            raise Exception("invalid dates given"+' '+str(endfecha)+' '+str(initfecha))
        # 
        iterfecha = initfecha
        while iterfecha <= endfecha:
            for p in PreciosWeb.objects(fecha=iterfecha):
                preciosindb = p.PreciosES
            for p in PrevEolWeb.objects(fecha=iterfecha):
                preveolindb = p.PrevEol
            for p in PrevDemandaWeb.objects(fecha=iterfecha):
                prevdemandaindb = p.PrevDemanda
            for p in EnergiaGestionadaWeb.objects(fecha=iterfecha):
                energiagestionadaindb = p.EnergiaGestionada
            for p in TecnologiasCBLWeb.objects(fecha=iterfecha):
                tecnologiascblindb = p.TecnologiasCBL
            for p in TecnologiasPBFWeb.objects(fecha=iterfecha):
                tecnologiaspbfindb = p.TecnologiasPBF
            #
            for h in range(24):
                iterfecha = datetime.datetime(iterfecha.year,iterfecha.month,iterfecha.day,h)
                studydata = StudyDataES(fecha=iterfecha)
                studydata.precio = preciosindb[h]
                studydata.EnergiaGestionada = energiagestionadaindb[h]
                studydata.PrevDemanda = prevdemandaindb[h]
                studydata.PrevEol = preveolindb[h]
                studydata.NUCLEAR = tecnologiaspbfindb['NUCLEAR']['valores'][h] - tecnologiascblindb['NUCLEAR']['valores'][h]
                studydata.save()
    except:
        raise