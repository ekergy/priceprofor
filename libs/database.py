# -*- coding: utf-8 -*-
'''
adding any database:
testing mongo with unique email as primary field.
Allowing for a email to login how ever he likes.

PENDING: like to try out firebase and redis as a alternative database.
'''
import pymongo

class DatabaseUsers(object):
    ''' 
    '''

    # Class attribute with the connection string to the mongo database.
    connectiondetails = dict(host = None)
    connectiondetails['coll_name'] = 'registedusers'

    #property: la db y las respectiva collection del usuario

    #property: numero de registros del usuario

    #property: numero de registros del usuario

    #property: collection de la base de datos:
    def getCollection(self):
        '''
        get mongo collection cursor.
        '''

        return self._collection

    def setCollection(self,conndetails=None):
        '''
        sets collection to be used.
        '''
        self._connection = pymongo.Connection(host = self.connectiondetails['host'])
        self._db = self._connection.smehogar
        self._collection = self._db[self.connectiondetails['coll_name']]

    def delCollection(self):
        '''
        Remove cursors from mongo database and collections.
        '''
        self._connection.close()
        del self._db,self._collection

    Collection = property(getCollection, 
                          setCollection, 
                          delCollection, 
                          "La collection para hacer las queries")

    def __init__(self):
        '''
        returns db connection or collection
        '''
        pass

    def find_user(self, email, password=None ):
        '''
        el nombre lo dice todo
        '''
        self.setCollection()
        collection = self.getCollection()
        results = collection.find({"uemail": email })
        self.delCollection()
        # make query to mongo and check the email is unique.
        if results.count() == 0:
            return False
        elif results.count() > 1:
            # send a email to app admin if this occur.
            return False
        #check user password:
        for result in results:
            if result['upassword'] == password:
                return result
            else:
                return False

    def add_user(self, **kwargs):
        '''
        el nombre lo dice todo.

        '''
        add_user_options = {'ufname':None, 'ulname':None, 'uname':None,
                          'uemail':None , 'upassword':None , 
                          'ulastauthused':None, 'ulastlogintime':None,
                          'ufirstauth':None,'ufirstlogindatetime':None}
        add_user_options.update(kwargs)

        #uinfo = {'ufname':ufname, 'ulname':ulname, 'uname':uname, 'uemail': uemail, 'upassword':upassword,
        #'ulastauth':ulastauth,'ulastlogintime':ulastlogintime,'ufirstauth':ulastauth,'ufirstlogindatetime':ulastlogindatetime}
        #oid = None
        self.setCollection()
        collection = self.getCollection()
        results = collection.find({"uemail": add_user_options['uemail'] })
        if results.count() > 1:
            return None
        collection.insert(add_user_options)
        
        self.delCollection()
        return add_user_options

    def update_user(self, **kwargs ):
        '''
        el nombre lo dice todo
        '''
        uinfo = {'ufname':None, 'ulname':None, 'uname':None,
                          'uemail':None , 'upassword':None , 
                          'ulastauthused':None, 'ulastlogindatetime':None}
        uinfo.update(kwargs)
        # TODO update user record.

        pass

    def return_user_by_objectid(self, uid ):
        '''
        el oid generado para el usuario es la clave de busqueda.
        '''
        if uid:
            pass
        else:
            return None

    def recover_user_password(self, email):
        '''
        yet another password recovery mode.
        '''
        pass


