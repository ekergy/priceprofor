# -*- coding: utf-8 -*-
<<<<<<< HEAD
"""Running the application on a local machine:

just type:
    $ python wsgi/priceprofor.py

Remmenber to have the mongodb up and running:
Also (it could be a on the same server or in a different one:)

"""
=======
'''
Created on 13/05/2014
@author: david, hector, hmarrao, mundi
'''
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
# set up sys path for local run development
import sys

try:
<<<<<<< HEAD
    # add libs and wsgi to python 
    #path to emulate openshift behavior and settings.
=======
    # add libs and wsgi to python
    # path to emulate openshift behavior and settings
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
    sys.path.append('libs/')
    sys.path.append('wsgi/')
except:
    raise

<<<<<<< HEAD
# importing models to setting the db URI

if __name__ == '__main__':
    import priceprofor
    priceprofor.app.run(debug=True)
=======
# fix change of hour
from utilities import diasconcambiodehora
from dbpreciosesmanager import populatePrecios, findLastPriceDocument, findFirstPriceDocument
from omelinfosys.dbstudydatamanager import populateStudyData, findLastStudyDocument, findFirstStudyDocument

# importing models to setting the db URI
from bottle import run
from priceprofor import myapplication
from dbpreciosesmanager import DBPreciosES
from dbmodelosesmanager import DBModelosES
from omelinfosys.dbstudydatamanager import DBStudyData
from omelinfosys.dbrawdatamanager import DBRawData

# names redefine connections
from utilities import connectiondetails as connectiondetailsutilities
from estadisticasgenericas import connectiondetails as connectiondetailsestadisticasgenericas

# from sys import path
# path.append('libs')
# from local_run import fixChangeOfHourInPrices
# fixChangeOfHourInPrices()
def fixChangeOfHourInPrices():
    """
    get all days different from 24 hours using as date the smalest in db collection and the biggest in db collection
    delete those days from collection PRECIOS (no need populate overwrite db info)
    execute a populate for each day
    """

    startDate = findFirstPriceDocument()['fecha']
    endDate = findLastPriceDocument()['fecha']

    dictio = diasconcambiodehora(startDate,endDate)

    print 'tecnologias verano'
    dictio['DiasCambioDeHoraAverano']
    for element in dictio['DiasCambioDeHoraAverano']:
        populatePrecios(element,element)

    print ''

    print 'tecnologias invierno'
    dictio['DiasCambioDeHoraAinvierno']
    for element in dictio['DiasCambioDeHoraAinvierno']:
        populatePrecios(element,element)

# from sys import path
# path.append('libs')
# from local_run import fixChangeOfHourInTechnologies
# fixChangeOfHourInTechnologies()
def fixChangeOfHourInTechnologies():
    """
    get all days different from 24 hours using as date the smalest in db collection and the biggest in db collection
    delete those days from collection TECNOLOGIAS (no need populate overwrite db info)
    execute a populate for each day
    """

    startDate = findFirstStudyDocument()['fecha']
    endDate = findLastStudyDocument()['fecha']

    dictio = diasconcambiodehora(startDate,endDate)

    print 'precios verano'
    dictio['DiasCambioDeHoraAverano']
    for element in dictio['DiasCambioDeHoraAverano']:
        populateStudyData(element,element)

    print ''

    print 'precios invierno'
    dictio['DiasCambioDeHoraAinvierno']
    for element in dictio['DiasCambioDeHoraAinvierno']:
        populateStudyData(element,element)

if __name__ == '__main__':
#     application.CONN_URI = None
#     application.CONN_URI = 'mongodb://sme:sme@ds035997.mongolab.com:35997/smehogar'

    hostLocalHost = None
    hostOpenShift = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'

    ''' LOCAL '''
#     DBPreciosES.connectiondetails['host'] = hostLocalHost
#     DBModelosES.connectiondetails['host'] = hostLocalHost
#     DBStudyData.connectiondetails['host'] = hostLocalHost
#     DBRawData.connectiondetails['host'] = hostLocalHost
#     connectiondetailsutilities['host'] = hostLocalHost
#     connectiondetailsestadisticasgenericas['host'] = hostLocalHost

    ''' SERVIDOR '''
    DBPreciosES.connectiondetails['host'] = hostOpenShift
    DBModelosES.connectiondetails['host'] = hostOpenShift
    DBStudyData.connectiondetails['host'] = hostOpenShift
    DBRawData.connectiondetails['host'] = hostOpenShift
    connectiondetailsutilities['host'] = hostOpenShift
    connectiondetailsestadisticasgenericas['host'] = hostOpenShift

    run(myapplication,host='0.0.0.0', port='8000', reloader=False)
#     run(application,host='0.0.0.0')
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
