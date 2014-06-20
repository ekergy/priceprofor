# -*- coding: utf-8 -*-
'''
Created on 13/05/2014
@author: david, hector, marrao, mundi y alguien más
'''
# set up sys path for local run development
import sys

try:
    # add libs and wsgi to python 
    #path to emulate openshift behavior and settings.
    sys.path.append('libs/')
    sys.path.append('wsgi/')
except:
    raise

from bottle import run
from sme_hogar import application
from database import DatabaseUsers

# importing models to setting the db URI

if __name__ == '__main__':
    # for cloud Run set this at the application file
    # try to use the config parser:
    # application.CONN_URI = 'mongodb://hmarrao:hmarrao@ds027479.mongolab.com:27479/profor'
    # User database URI:
    application.CONN_URI = 'mongodb://sme:sme@ds035997.mongolab.com:35997/smehogar'
    # 
    # application.CONN_URI = None
    DatabaseUsers.connectiondetails['host'] = application.CONN_URI
    #MedidorPotencias.connectiondetails['host'] = application.CONN_URI
    #LecturasContador.connectiondetails['host'] = application.CONN_URI
    #run(application,host='0.0.0.0',port='8000',reloader=True)
    # run(application,host='0.0.0.0')
    run(application,host='0.0.0.0',port='8000',reloader=False)
    
