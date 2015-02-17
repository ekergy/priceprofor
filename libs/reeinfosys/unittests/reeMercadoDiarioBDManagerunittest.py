# -*- coding: utf-8 -*-
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
    from reeMercadoDiarioDBManager import TecnologiasCBLWeb, TecnologiasPBFWeb, PrevisionesWeb, PreciosWeb
    from mongoengine import *
    from mongoengine import connection

# Constantes:

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
            self.fechatest = datetime.datetime(2014,1,1)
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
        Testing all classes defined at reeMercadoDiarioDBManager
        """
        pass