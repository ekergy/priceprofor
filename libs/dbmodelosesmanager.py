# -*- coding: utf-8 -*-
'''
Created on 11/2014
@author: hmarrao & david
'''

from os import path
direc = path.abspath(__file__)
machine = direc[direc.find("e")+2:direc.find("w")-1]

from pymongo import Connection

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import DBModelosES
# ins = DBModelosES()
class DBModelosES(object):
    '''
    '''
    connectiondetails = dict(host=None)
#     connectiondetails = dict()

    def __init__(self,tipo=None):
        '''
        SET COLLECTION NAME IN MONGO
        No need for user uname or coopid
        '''

        # LOCAL
        # self.connectiondetails['host'] = None
        # SERVIDOR
        # self.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'

        self.connectiondetails['host'] = self.connectiondetails['host']
        self.connectiondetails['db_name'] = 'mercadodiario'
        if tipo == None:
            self.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
            self.connectiondetails['coll_name'] = 'modelosHWTES'
        elif tipo == 'NN':
            self.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
            self.connectiondetails['coll_name'] = 'modelosARNN'
            # self.connectiondetails['host'] = None
            # self.connectiondetails['coll_name'] = 'modelosARNN'
        self.setCollection()

    def getCollection(self):
        '''
        Get mongo collection cursor
        '''
        return self._collection

#     def setCollection(self, conndetails=None):
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
