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
from omelinfosys.dbrawdatamanager import DBRawData

# names redefine connections
from utilities import connectiondetails as connectiondetailsutilities
from estadisticasgenericas import connectiondetails as connectiondetailsestadisticasgenericas

if __name__ == '__main__':
#     application.CONN_URI = None
#     application.CONN_URI = 'mongodb://sme:sme@ds035997.mongolab.com:35997/smehogar'

#     hostLocalHost = None
    hostOpenShift = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'

    ''' LOCAL '''
#     DBPreciosES.connectiondetails['host'] = hostLocalHost
#     DBStudyData.connectiondetails['host'] = hostLocalHost
#     DBRawData.connectiondetails['host'] = hostLocalHost
#     connectiondetailsutilities['host'] = hostLocalHost
#     connectiondetailsestadisticasgenericas['host'] = hostLocalHost

    ''' SERVIDOR '''
    DBPreciosES.connectiondetails['host'] = hostOpenShift
    DBStudyData.connectiondetails['host'] = hostOpenShift
    DBRawData.connectiondetails['host'] = hostOpenShift
    connectiondetailsutilities['host'] = hostOpenShift
    connectiondetailsestadisticasgenericas['host'] = hostOpenShift

    run(myapplication,host='0.0.0.0', port='8000', reloader=False)
#     run(application,host='0.0.0.0')
