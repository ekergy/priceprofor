# -*- coding: utf-8 -*-
#!/usr/bin/env python

__author__ = ("Hugo M. Marrao Rodrigues","David deJuan")
__version__ = "0.0.1"
__revision__ = "dev"

# from mongoengine import MongoEngine

CONN_DETAILS = {'db':'priceprofor'}

# db = MongoEngine()
import os
try:
    # mongodb://$OPENSHIFT_MONGODB_DB_HOST:$OPENSHIFT_MONGODB_DB_PORT/
    # host = os.environ['OPENSHIFT_MONGODB_IP']
    host = os.environ['OPENSHIFT_MONGODB_DB_HOST']
    port = os.environ['OPENSHIFT_MONGODB_DB_PORT']
    # host = 'mongodb://'+host+':'+port+'/'
    host = os.environ['OPENSHIFT_MONGODB_DB_URL']
except:
    host = 'localhost'
    port = 27017

from mongoengine.connection import get_db, connect

try:
    get_db(CONN_DETAILS['db'],reconnect=True)
except:
    print "modellingsys ->",host
    connect(CONN_DETAILS['db'],host=host)