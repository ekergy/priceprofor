# -*- coding: utf-8 -*-
'''
Created on 13/05/2014
@author: david, hector, hmarrao, mundi
'''
# set up sys path for local run development
import sys

try:
    # add libs and wsgi to python
    # path to emulate openshift behavior and settings
    sys.path.append('libs/')
    sys.path.append('wsgi/')
except:
    raise

# importing models to setting the db URI
from bottle import run
from priceprofor import aplicacion
from dbpreciosesmanager import DBPreciosES
from omelinfosys.dbstudydatamanager import DBStudyData
# from controllers.priceprofor_graficas import connectiondetails
from utilities import connectiondetails



if __name__ == '__main__':
#     application.CONN_URI = None
#     application.CONN_URI = 'mongodb://sme:sme@ds035997.mongolab.com:35997/smehogar'

#     DBPreciosES.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
#     DBStudyData.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
#     connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'

    DBPreciosES.connectiondetails['host'] = None
    DBStudyData.connectiondetails['host'] = None
    connectiondetails['host'] = None

    run(aplicacion,host='0.0.0.0',port='8000',reloader=True)
#     run(application,host='0.0.0.0')
