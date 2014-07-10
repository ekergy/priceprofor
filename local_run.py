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
from priceprofor import application
from dbpreciosesmanager import DBPreciosES

# importing models to setting the db URI

if __name__ == '__main__':
    
    #application.CONN_URI = None
    DBPreciosES.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
    ## application.CONN_URI = 'mongodb://sme:sme@ds035997.mongolab.com:35997/smehogar'
    
    run(application,host='0.0.0.0',port='8000',reloader=True)
    # run(application,host='0.0.0.0')
    
