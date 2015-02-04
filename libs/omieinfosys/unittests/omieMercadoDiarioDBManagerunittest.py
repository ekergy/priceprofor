# importing 
import sys
import os
import unittest
import datetime
import time
try:
    # to import the module needed.
    sys.path.append('..')
    sys.path.append('../..')
except:
    pass
finally:
    from omieMercadoDiarioDBManager import PreciosWeb, TecnologiasWeb
    from omieinfosys import preciosmercadodiarioparser, tecnologiasmercadodiarioparser
    from utilities import cambiohoraverano, cambiohorainvierno
    from mongoengine import *
    from mongoengine import connection
    from urllib2 import urlopen


# Constantes:

# Funcciones Auxiliares:
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
        if datetime.now() < fecha:
            raise Exception('La fecha selecionada es posterior a hoy. No hay datos disponibles en la web.')
        fecha.replace(hour = 0)
    except:
        raise
    else:
        return

# main:
def main():
    unittest.main()

class testOMIEdbManagers(unittest.TestCase):
    """
    This test case should test the function and the class sepreatedly
    """

    def setUp(self):
        """
        Add Connection via mongoengine.
        testing against local mongod instance
        """
        try:
            # start connection
            connection.connect('unittests')
            self.fechatest = datetime.datetime(2013,1,1)
        except:
            raise
    
    def tearDown(self):
        """
        Close Connection via mongoengine
        """
        #print("tearing it down")
        # Delete each inicialized handler.
        try:
            # start connection
            # disconnect()
            connection.disconnect('unittests')
        except:
            raise

    def test00_ConnectionAndBasicOperations(self):
        """
        Just test connection and other stuff that check availability and configuation
        """
        # perform test on each collection!
        try:
            # the PreciosWeb Document generates the precios_web collection
            precios = PreciosWeb.objects(fecha=self.fechatest)
            self.assertEqual(precios.count(),0)
            del precios
            # Adding information
            precios1 = PreciosWeb(fecha=self.fechatest)
            precios1.PreciosES = [i for i in range(24)]
            precios1.PreciosPT = [100+i for i in range(24)]
            precios1.PreciosMI = [200+i for i in range(24)]
            precios1.save()
            del precios1
            # Querying Information
            for precios in PreciosWeb.objects(fecha=self.fechatest):
                precios2 = precios
            self.assertEqual(precios2.PreciosES,[i for i in range(24)])
            self.assertEqual(precios2.PreciosPT,[100+i for i in range(24)])
            self.assertEqual(precios2.PreciosMI,[200+i for i in range(24)])
            del precios2
            # Deleting Information
            for precios in PreciosWeb.objects(fecha=self.fechatest):
                precios3 = precios
            precios3.delete()
            # Check Precios collection for emptyness
            precios4 = PreciosWeb.objects(fecha=self.fechatest)
            self.assertEqual(precios4.count(),0)
            del precios4
        except:
            raise


    def test01_PreciosWebUsage(self):
        """
        This will test the class and the parser classes as this is intend to be used.
        Parse web data:: save data as it is.
        RecheckData:: should compare webdata and dbdata ok if Equal, else should raise the place were isn't equal.
        """
        resultsfromdb = PreciosWeb.objects(fecha=self.fechatest)
        preciosweb = preciosmercadodiarioparser(self.fechatest)
        if resultsfromdb.count() == 0:
            precios = PreciosWeb(self.fechatest)
            precios.PreciosPT = preciosweb['PreciosPT']
            precios.PreciosES = preciosweb['PreciosES']
            precios.PreciosMI = preciosweb['PreciosMibel']
            precios.save()
        resultsfromdb = PreciosWeb.objects(fecha=self.fechatest)
        # if resultsfromdb.count() == 1: No need to do this since result is unique by definition.
        for result in resultsfromdb:
            preciotest = result
            self.assertEqual(preciotest.PreciosES,preciosweb['PreciosES'])
            self.assertEqual(preciotest.PreciosMI,preciosweb['PreciosMibel'])
            self.assertEqual(preciotest.PreciosPT,preciosweb['PreciosPT'])
            # Deletes manage document
            preciotest.delete()


    def test02_TecnologiasWebUsage(self):
        """
        This will test the class and the parser classes as this is intend to be used.
        Parse web data:: save data as it is.
        RecheckData:: should compare webdata and dbdata ok if Equal, else should raise the place were isn't equal.
        """
        resultsfromdb = TecnologiasWeb.objects(fecha=self.fechatest)
        tecnologiasweb = tecnologiasmercadodiarioparser(self.fechatest)
        if resultsfromdb.count() == 0:
            tecnologias = TecnologiasWeb(self.fechatest)
            tecnologias.ProduccionyDemandaMIBEL = tecnologiasweb['ProduccionyDemandaMIBEL']
            tecnologias.ProduccionyDemandaES = tecnologiasweb['ProduccionyDemandaES']
            tecnologias.ProduccionyDemandaPT = tecnologiasweb['ProduccionyDemandaPT']
        resultsfromdb = TecnologiasWeb.objects(fecha=self.fechatest)
        # if resultsfromdb.count() ==1: No need to do this since result is unique by definition
        for result in resultsfromdb:
            tecnologiastest = result
            self.assertEqual(tecnologiastest.ProduccionyDemandaMIBEL,tecnologiasweb['ProduccionyDemandaMIBEL'])
            self.assertEqual(tecnologiastest.ProduccionyDemandaES,tecnologiasweb['ProduccionyDemandaES'])
            self.assertEqual(tecnologiastest.ProduccionyDemandaPT,tecnologiasweb['ProduccionyDemandaPT'])
            # Deletes manage document
            tecnologiastest.delete()

