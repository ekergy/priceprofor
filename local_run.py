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
from priceprofor import myapplication
from dbpreciosesmanager import DBPreciosES
from omelinfosys.dbstudydatamanager import DBStudyData
from utilities import connectiondetails as connectiondetailsutilities
from estadisticasgenericas import connectiondetails as connectiondetailsestadisticasgenericas

if __name__ == '__main__':
#     application.CONN_URI = None
#     application.CONN_URI = 'mongodb://sme:sme@ds035997.mongolab.com:35997/smehogar'

    ''' LOCAL '''
    DBPreciosES.connectiondetails['host'] = None
    DBStudyData.connectiondetails['host'] = None
    connectiondetailsutilities['host'] = None
    connectiondetailsestadisticasgenericas['host'] = None

    ''' SERVIDOR '''
#     DBPreciosES.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
#     DBStudyData.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
#     connectiondetailsutilities['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
#     connectiondetailsestadisticasgenericas['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'

    run(myapplication,host='0.0.0.0', port='8000', reloader=False)
#     run(application,host='0.0.0.0')
