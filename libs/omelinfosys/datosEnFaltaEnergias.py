# -*- coding: utf-8 -*-
'''
Created on 02/2013
@author: hmarrao & david
'''
from datetime import datetime, timedelta
from pymongo import Connection
from numpy.numarray import array, zeros
from utilities import cambiohoraverano, cambiohorainvierno
# from sys import exit

'''
es necesario que exista un script __init__.py para que se resuelvan los imports
'''

def getDummyPrecios(dt):
    '''
    '''
    if dt == datetime(1,1,1):
        pass
    else:
        PRECIOS = []
    return PRECIOS

def getDummyPrevisionEolica(dt):
    '''
    '''
    if dt == datetime(1,1,1):
        pass
    if dt == datetime(2011,4,23):
        ''' NO PERTENECE A LA LISTA DE DIAS EN FALTA '''
        previsionEOLICA = [4097, 4151, 4048, 3817, 3572, 3432, 3301, 3246, 3254, 3424, 3456, 3716, 3860, 4050, 4136, 4224, 4370, 4326, 4266, 4229, 4192, 4165, 4100, 4038]
    else:
        previsionEOLICA = []
    return previsionEOLICA

def getDummyPrevisionDemanda(dt):
    '''
    '''
    if dt == datetime(1,1,1):
        pass
    # PrevisionDemandaES (vector completo vacio)
    if dt == datetime(2011,4,23):
        DEMANDA = [22701.4, 21523.7, 19788.0, 18163.3, 17603.4, 17508.3, 18416.7, 18971.0, 18736.6, 20574.0, 22308.2, 23085.4, 24011.5, 24874.2, 24659.2, 24179.0, 23394.3, 23314.9, 22542.6, 22441.5, 24245.2, 26378.5, 26222.3, 25282.9]
    # PrevisionDemandaES (algunos elementos vacios)
    elif dt == datetime(2011, 3, 7):
        DEMANDA = [28039.1, 24660.2, 21151.0, 20878.1, 20811.0, 21602.0, 24044.1, 28670.6, 31404.2, 33605.7, 34517.0, 34796.9, 35436.4, 34596.5, 34071.5, 33158.2, 32476.9, 32724.9, 34067.5, 36191.0, 36210.3, 36489.8, 35676.5, 31935.7]
    elif dt == datetime(2011, 3, 8):
        DEMANDA = [28586.7, 25509.0, 23175.6, 22436.5, 22053.4, 22623.8, 24378.6, 29032.5, 32068.7, 34022.7, 34498.1, 34884.1, 35799.1, 34960.6, 34220.1, 33078.1, 32425.5, 32925.1, 34143.4, 36281.3, 36041.0, 35893.9, 34589.7, 30956.5]
    elif dt == datetime(2011,3,19):
        DEMANDA = [30211.3, 27407.5, 24766.1, 23705.0, 22863.0, 22006.3, 21994.1, 22858.6, 23397.5, 26016.0, 27880.2, 28749.4, 28812.1, 28735.4, 29048.8, 28187.0, 27392.8, 27623.3, 29450.9, 30477.4, 31095.4, 31759.3, 30928.5, 29747.8]
    elif dt == datetime(2011,4,21):
        DEMANDA = [26393.6, 24368.7, 22394.3, 21904.5, 21706.0, 21216.5, 20126.9, 19997.0, 20328.7, 21646.7, 24090.2, 24663.6, 25143.4, 25185.0, 24810.3, 23859.3, 22863.0, 22594.3, 22301.7, 22680.9, 24730.9, 26893.8, 26299.8, 24931.6]
    elif dt == datetime(2011,5,2):
        DEMANDA = [21833.4, 19719.8, 17872.3, 16964.2, 16887.9, 17308.6, 19668.7, 22094.7, 24055.5, 25566.4, 26530.3, 26867.7, 27235.8, 27574.7, 26770.7, 26592.0, 26646.1, 26373.4, 25976.2, 25666.8, 26940.3, 28190.0, 27487.6, 25610.5]
    elif dt == datetime(2011,8,19):
        DEMANDA = [27218.7, 24319.6, 22342.6, 20974.3, 20167.2, 20748.1, 22072.7, 24136.4, 26677.9, 28512.6, 31399.7, 32095.4, 33086.9, 33943.1, 32573.7, 32152.6, 31663.3, 31098.1, 30628.3, 30275.6, 29739.2, 29562.1, 29435.8, 27640.6]
    else:
        DEMANDA = []
    return DEMANDA

def getDummyProduccionyDemanda(dt):
    '''
    '''
    HORASENUNDIA = 24

    if dt == datetime(1,1,1):
        ''' plantilla para rellenar datos en falta '''

        BALxls = {
        'Hidráulica (UGH + Turb. Bomb.)': list(),
        'Nuclear': list(),
        'Carbón': list(),
        'Fuel + Gas': list(),
        'Ciclo combinado': list(),
        'Resto hidráulica': list(),
        'Eólica': list(),
        'Solar fotovoltaico': list(),
        'Solar térmico': list(),
        'Térmica renovable': list(),
        'Cogeneración y resto': list(),
        'Total generación': list(),
        'Consumos en bombeo': list(),
        'Enlace Península-Baleares': list(),
        'Saldo Francia': list(),
        'Saldo Portugal': list(),
        'Saldo Marruecos': list(),
        'Saldo Andorra': list(),
        'Saldo internacional': list(),
        'Ajuste de programas': list(),
        'Demanda peninsular': list() }

        CBFxls = {
        'Hidráulica (UGH + Turb. Bomb.)': list(),
        'Nuclear': list(),
        'Carbón': list(),
        'Fuel + Gas': list(),
        'Ciclo combinado': list(),
        'Resto hidráulica': list(),
        'Eólica': list(),
        'Solar fotovoltaico': list(),
        'Solar térmico': list(),
        'Térmica renovable': list(),
        'Cogeneración y resto': list(),
        'Total generación': list(),
        'Comercialización Mercado Libre': list(),
        'Unid. Prog. Genéricas Demanda': list(),
        'Prog. Imp. Francia': list(),
        'Prog. Imp. Portugal': list(),
        'Prog. Imp. Marruecos': list(),
        'Prog. Imp. Andorra': list(),
        'Total importaciones': list(),
        'Total ventas': list(),
        'Consumos en bombeo': list(),
        'Comercialización Mercado Libre': list(),
        'Comercialización Último Recurso': list(),
        'Consumo Directo en Mercado': list(),
        'Unid. Prog. Genéricas Produccion': list(),
        'Prog. Exp. Francia': list(),
        'Prog. Exp. Portugal': list(),
        'Prog. Exp. Marruecos': list(),
        'Prog. Exp. Andorra': list(),
        'Total exportaciones': list(),
        'Total compras': list() }

        EGxls = list()

    elif dt == datetime(2014,3,17):
        ''' NO PERTENECE A LA LISTA DE DIAS EN FALTA '''

        BALxls = {
        'Hidráulica (UGH + Turb. Bomb.)': [6248.3, 5339.4, 4279.5, 4995.5, 5024.5, 5703.3, 7685.3, 9960.6, 10506.7, 10323.6, 9973.4, 9904.8, 9960.9, 9577.0, 9517.0, 9243.6, 9230.0, 9650.1, 10670.4, 11211.7, 11605.2, 11452.5, 11076.3, 10023.5],
        'Nuclear': [7118.7, 7118.7, 7118.7, 7118.7, 7118.7, 7118.7, 7118.7, 7118.7, 7118.7, 7118.7, 7118.7, 7118.7, 7118.7, 7116.8, 7114.9, 7114.9, 7114.9, 7114.9, 7114.9, 7114.9, 7116.8, 7116.8, 7117.8, 7118.7],
        'Carbón': [0.0, 0.0, 0.0, 0.0, 60.0, 150.0, 386.0, 1622.0, 2526.0, 2646.0, 2410.2, 2136.0, 2691.0, 2602.5, 2028.4, 1741.0, 1741.0, 1741.0, 2746.0, 2801.0, 2801.0, 2801.0, 2801.0, 1741.0],
        'Fuel + Gas': [327.6, 327.9, 327.9, 327.1, 327.6, 326.5, 327.0, 332.3, 331.0, 329.7, 329.0, 328.7, 328.2, 328.5, 327.7, 328.3, 328.4, 329.2, 329.5, 329.9, 330.7, 332.3, 333.0, 333.4],
        'Ciclo combinado': [1284.4, 1024.4, 999.4, 199.4, 199.4, 199.4, 199.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4, 349.4],
        'Resto hidráulica': [1053.3, 1026.3, 961.4, 957.3, 954.5, 967.9, 969.0, 979.1, 1004.3, 1020.7, 1036.7, 1063.8, 1071.1, 1059.7, 1053.4, 1116.6, 1103.1, 1143.2, 1099.7, 1219.2, 1227.9, 1224.3, 1231.8, 1110.8],
        'Eólica': [3444.8, 2770.8, 2071.3, 1637.3, 1341.7, 1142.4, 1009.5, 1020.7, 987.3, 1012.9, 1040.4, 1085.3, 1291.3, 1252.5, 1319.7, 1311.6, 1321.8, 1450.9, 1378.4, 1443.6, 1372.4, 1635.3, 1656.2, 1527.8],
        'Solar fotovoltaico': [0, 0, 0, 0, 0, 0, 49.7, 238.2, 1108.8, 2217.9, 2961.6, 3386.8, 3603.6, 3600.1, 3419.5, 3027.1, 2451.3, 1594.9, 539.5, 55.5, 23.0, 22.9, 0, 0],
        'Solar térmico': [420.3, 363.4, 308.3, 140.6, 39.9, 39.9, 37.2, 11.7, 64.6, 670.4, 1527.1, 1829.4, 1867.3, 1872.6, 1879.3, 1898.8, 1894.7, 1829.3, 1333.6, 708.8, 576.2, 589.2, 552.9, 549.4],
        'Térmica renovable': [504.1, 505.7, 499.6, 500.4, 499.9, 500.1, 500.1, 548.7, 553.5, 555.3, 554.7, 564.6, 582.9, 578.1, 580.4, 549.7, 546.6, 582.5, 581.1, 580.7, 575.2, 582.8, 584.8, 548.1],
        'Cogeneración y resto': [1927.7, 1927.7, 1924.8, 1918.2, 1911.1, 1915.4, 1937.8, 2107.7, 2732.0, 2838.6, 2836.3, 2845.0, 2868.1, 2866.7, 2869.4, 2826.7, 2822.8, 2868.6, 2884.2, 2891.2, 2924.8, 2928.5, 2903.7, 2801.6],
        'Total generación': [22329.2, 20404.3, 18490.9, 17794.5, 17477.3, 18063.6, 20219.7, 24289.1, 27282.3, 29083.2, 30137.5, 30612.5, 31732.5, 31203.9, 30459.1, 29507.7, 28904.0, 28654.0, 29026.7, 28705.9, 28902.6, 29035.0, 28606.9, 261037.0],
        'Consumos en bombeo': list(),
        'Enlace Península-Baleares': list(),
        'Saldo Francia': [1200.0, 1300.0, 1180.0, 1179.0, 1300.0, 1300.0, 1056.0, 1150.0, 1150.0, 1160.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1080.0, 1005.0, 1030.0, 1200.0, 1200.0, 1200.0, 1200.0],
        'Saldo Portugal': [806.6, 288.8, -152.3, -173.6, 140.7, 232.4, 646.0, 624.4, 881.6, 521.5, -146.1, -345.4, -381.5, -180.8, -97.3, -207.3, -76.9, 88.0, 610.6, 1760.3, 1535.8, 1527.7, 1215.0, 452.1],
        'Saldo Marruecos': [-300.0, -200.0, -100.0, 0, 0, 0, 0, 0, -350.0, -450.0, -500.0, -550.0, -550.0, -550.0, -550.0, -550.0, -550.0, -500.0, -500.0, -700.0, -700.0, -700.0, -550.0, -550.0],
        'Saldo Andorra': [-43.0, -37.0, -35.0, -34.0, -33.0, -34.0, -39.0, -49.0, -15.0, -24.0, -28.0, -28.0, -27.0, -25.0, -22.0, -67.0, -67.0, -67.0, -69.0, -75.0, -73.0, -68.0, -58.0, -51.0],
        'Saldo internacional': list(),
        'Ajuste de programas': list(),
        'Demanda peninsular': list() }

        CBFxls = {
        'Hidráulica (UGH + Turb. Bomb.)': [3263.7, 2392.7, 1067.1, 920.3, 1191.1, 1338.3, 2148.3, 3500.2, 4201.0, 4457.6, 4343.8, 4442.1, 4726.4, 4800.7, 4675.9, 4370.7, 4201.7, 4433.5, 5230.0, 5790.4, 5929.3, 6088.3, 5906.1, 4860.5],
        'Nuclear': [5862.8, 5862.8, 5862.8, 5862.8, 5862.8, 5862.8, 5862.8, 5862.8, 5862.8, 5862.8, 5862.8, 5862.8, 5862.8, 5861.0, 5859.1, 5859.1, 5859.1, 5859.1, 5859.1, 5859.1, 5861.0, 5861.0, 5862.0, 5862.8],
        'Carbón': [0] * HORASENUNDIA,
        'Fuel + Gas': [0] * HORASENUNDIA,
        'Ciclo combinado': [0] * HORASENUNDIA,
        'Resto hidráulica': [0] * HORASENUNDIA,
        'Eólica': [0] * HORASENUNDIA,
        'Solar fotovoltaico': [0] * HORASENUNDIA,
        'Solar térmico': [0] * HORASENUNDIA,
        'Térmica renovable': [0] * HORASENUNDIA,
        'Cogeneración y resto': [0] * HORASENUNDIA,
        'Total generación': [9126.5, 8255.5, 6929.9, 6783.1, 7053.9, 7201.1, 8011.1, 9363.0, 10063.8, 10320.4, 10206.6, 10304.9, 10589.2, 10661.7, 10535.0, 10229.8, 10060.8, 10292.6, 11089.1, 11649.5, 11790.3, 11949.3, 11768.1, 10723.3],
        'Comercialización Mercado Libre': list(),
        'Unid. Prog. Genéricas Demanda': [2671.5, 2437.5, 2339.1, 2327.8, 2232.4, 2364.8, 2827.8, 3304.0, 3654.8, 4000.0, 4084.0, 4102.9, 4157.9, 3967.9, 3800.3, 3642.8, 3575.9, 3727.2, 3828.6, 3995.7, 3814.3, 3636.7, 3395.7, 3074.6],
        'Prog. Imp. Francia': [1200.0, 1300.0, 1300.0, 1300.0, 1300.0, 1300.0, 1216.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1175.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0],
        'Prog. Imp. Portugal': [0] * HORASENUNDIA,
        'Prog. Imp. Marruecos': [0] * HORASENUNDIA,
        'Prog. Imp. Andorra': [0] * HORASENUNDIA,
        'Total importaciones': [1200.0, 1300.0, 1300.0, 1300.0, 1300.0, 1300.0, 1216.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1175.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0],
        'Total ventas': list(),
        'Consumos en bombeo': [0] * HORASENUNDIA,
        'Comercialización Mercado Libre': list(),
        'Comercialización Último Recurso': list(),
        'Consumo Directo en Mercado': list(),
        'Unid. Prog. Genéricas Produccion': [1200.0, 1300.0, 1300.0, 1300.0, 1300.0, 1300.0, 1176.0, 1160.0, 1160.0, 1160.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1135.0, 1160.0, 1200.0, 1200.0, 1200.0, 1200.0],
        'Prog. Exp. Francia': [0, 0, 120.0, 121.0, 0, 0, 160.0, 50.0, 50.0, 40.0, 0, 0, 0, 0, 0, 0, 0, 120.0, 170.0, 170.0, 0, 0, 0, 0],
        'Prog. Exp. Portugal': [0] * HORASENUNDIA,
        'Prog. Exp. Marruecos': [0] * HORASENUNDIA,
        'Prog. Exp. Andorra': [3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 3.0, 4.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 4.0],
        'Total exportaciones': [3.0, 3.0, 122.0, 123.0, 2.0, 2.0, 163.0, 54.0, 55.0, 45.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 125.0, 175.0, 175.0, 5.0, 5.0, 4.0, 4.0],
        'Total compras': list() }

        EGxls = [15169.3, 13697.6, 12821.0, 12271.4, 11824.1, 12354.9, 14030.6, 16710.5, 19260.1, 20444.3, 21090.9, 21427.6, 22238.3, 21612.2, 20994.1, 20347.9,  19913.2, 19593.4, 19683.2, 19976.7, 19787.1, 19773.4, 19173.8, 17032.5]

    else:
        BALxls = {}
        CBFxls = {}
        EGxls = []

    return BALxls, CBFxls, EGxls

# from sys import path
# path.append('libs')
# from datetime import datetime
# fecha = datetime(2014,1,1)
# from omelinfosys.datosEnFaltaEnergias import centralEuropeanTime
# centralEuropeanTime(fecha)
def centralEuropeanTime(anyo):
    '''
    Central European Time
    01:00:00 CET
    Central European Summer Time
    02:00:00 CEST
    '''
    fechaCHV = cambiohoraverano(anyo)
    fechaCHI = cambiohorainvierno(anyo)
    return fechaCHV, fechaCHI

# from sys import path
# path.append('libs')
# from datetime import datetime
# dt = datetime(2011,3,19)
# DEMANDA = 
# from omelinfosys.datosEnFaltaEnergias import zeroPrevisionDemanda
# zeroPrevisionDemanda(dt, DEMANDA)
def zeroPrevisionDemanda(dt, DEMANDA):
    '''
    '''
    from dbrawdatamanager import DBRawData
    ins = DBRawData(dt)
    ins.getPrevisionDemandaESfromWeb()
    previsionDEMANDA = ins.PrevisionDemandaES
    for indi in range(len(previsionDEMANDA)):
        if previsionDEMANDA[indi] == 0:
            previsionDEMANDA[indi] = DEMANDA[indi]
    return previsionDEMANDA

# from sys import path
# path.append('libs')
# from omelinfosys.dbrawdatamanager import diasEnFalta
# diasEnFalta()
def diasEnFalta():
    '''
    Lista de dias sin datos sobre subtotales energias en la web "http://www.omie.es/inicio"
    que obtenemos haciendo calculos a partir de la web http://www.esios.ree.es/web-publica/
    '''

    ''' Las fechas datetime(x,y,z) no funcionan bien si ponemos por ej el mes "01" en vez de "1" '''
    # PrevisionDemandaES (vector completo vacio)
    emptyPD = [ datetime(2011,4,23) ]
    # PrevisionDemandaES (algunos elementos vacios)
    zeroPD = [ datetime(2011,3,7), datetime(2011,3,8),
               datetime(2011,3,19), datetime(2011,4,21),
               datetime(2011,5,2), datetime(2011,8,19) ]

    # listDT = emptyPD + zeroPD
    # listDT = []
    # return listDT
    return emptyPD, zeroPD

# from datetime import datetime
# fecha = datetime(2014,3,17)
# from sys import path
# path.append('libs')
# from omelinfosys.dbrawdatamanager import datosEnFalta
# dic = datosEnFalta(fecha)
# dic['ProduccionyDemandaES']['HIDRAULICA_CONVENCIONAL']
def datosEnFalta(dt):
    '''
    No olvidar que al llamar a esta funcion, el valor de "dt" debe ser por ejemplo "2014-3-17"
    '''
    dic = dict()
    HORASENUNDIA = 24
    emptyPD, zeroPD = diasEnFalta()
    listDT = emptyPD + zeroPD

    '''
    PreciosES
    '''
    # print 'PreciosES'

    if dt in listDT:
        PRECIOS = getDummyPrecios(dt)
        if PRECIOS:
            dic['PreciosES'] = PRECIOS
        else:
            dic['PreciosES'] = []

    '''
    PrevisionEolicaES
    '''
    # print 'PrevisionEolicaES'

    if dt in listDT:
        previsionEOLICA = getDummyPrevisionEolica(dt)
        if previsionEOLICA:
            dic['PrevisionEolicaES'] = previsionEOLICA
        else:
            dic['PrevisionEolicaES'] = []

    '''
    PrevisionDemandaES
    '''
    # print 'PrevisionDemandaES'

    if dt in listDT:
        DEMANDA = getDummyPrevisionDemanda(dt)
        if dt in emptyPD:
            previsionDEMANDA = DEMANDA
        elif dt in zeroPD:
            previsionDEMANDA = zeroPrevisionDemanda(dt, DEMANDA)
        if previsionDEMANDA:
            dic['PrevisionDemandaES'] = previsionDEMANDA
        else:
            dic['PrevisionDemandaES'] = []

    '''
    ProduccionyDemandaES
    '''
    # print 'ProduccionyDemandaES'

    if dt in listDT:
        BALxls, CBFxls, EGxls = getDummyProduccionyDemanda(dt)
    else:
        BALxls, CBFxls, EGxls = {}, {}, []

    '''
    SUBTOTALES_ENERGIAS
    Debemos de restar a las tecnologias del fichero BAL las mismas tecnologias del fichero CBF
    '''

    pyd = {
    'EXPORTACION_A_FRANCIA': list(),
    'UNIDADES_GENERICAS_DEMANDA': list(),
    'TOTAL_GENERICAS_(30+31)': list(),
    'UNIDADES_GENERICAS_PRODUCCION': list(),
    'TOTAL_GENERICAS_(16+17)': list(),
    'NUCLEAR': list(),
    'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA': list(),
    'TOTAL_DEMANDA': list(),
    'FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)': list(),
    'EXPORTACION_CONTRATO_A_LARGO_PLAZO': list(),
    'REGIMEN_ESPECIAL_A_DISTRIBUCION': list(),
    'TOTAL_PRODUCCION': list(),
    'IMPORTACION_CONTRATO_LARGO_PLAZO': list(),
    'IMPORTACION_MARRUECOS': list(),
    'TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO': list(),
    'HIDRAULICA_CONVENCIONAL': list(),
    'CONSUMO_DE_BOMBEO': list(),
    'FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)': list(),
    'UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION': list(),
    'CICLO_COMBINADO': list(),
    'HIDRAULICA_BOMBEO_PURO': list(),
    'TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)': list(),
    'COMERCIALIZACION_NACIONAL': list(),
    'TOTAL_POTENCIA_INDISPONIBLE': list(),
    'CARBON_IMPORTACION': list(),
    'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO': list(),
    'TOTAL_REGIMEN_ESPECIAL_(9+10)': list(),
    'COMERCIALIZACION_ULTIMO_RECURSO': list(),
    'TOTAL_EXPORTACIONES_(25+26+27+28+29)': list(),
    'EXPORTACION_A_PORTUGAL': list(),
    'CARBON_NACIONAL': list(),
    'TOTAL_CONSUMO_BOMBEO_(24)': list(),
    'IMPORTACION_PORTUGAL': list(),
    'TOTAL_TERMICA_(3+4+5+6+7+8)': list(),
    'TOTAL_IMPORTACION_(11+12+13+14+15)': list(),
    'UNIDADES_AJUSTE_DE_DISTRIBUIDORAS_A_PREVISION_DEMANDA': list(),
    'EXPORTACION_A_MARRUECOS': list(),
    'IMPORTACION_FRANCIA': list(),
    'TOTAL_HIDRAULICA_(1+2)': list(),
    'REGIMEN_ESPECIAL_A_MERCADO': list(),
    'CONSUMIDOR_DIRECTO': list(),
    'IMPORTACION_ANDORRA': list(),
    'EXPORTACION_A_ANDORRA': list() }

    if EGxls:
        pyd['TOTAL_DEMANDA'] = EGxls

    if BALxls and CBFxls:

        names = [ 'HIDRAULICA_CONVENCIONAL',
                  'NUCLEAR',
                  'CARBON_IMPORTACION',
                  'CICLO_COMBINADO',
                  'FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)',
                  'TOTAL_PRODUCCION' ]

        BAL = { names[0]: BALxls['Hidráulica (UGH + Turb. Bomb.)'],
                names[1]: BALxls['Nuclear'],
                names[2]: BALxls['Carbón'],
                names[3]: BALxls['Fuel + Gas'],
                names[4]: BALxls['Ciclo combinado'],
                names[5]: BALxls['Total generación'] }

        CBF = { names[0]: CBFxls['Hidráulica (UGH + Turb. Bomb.)'],
                names[1]: CBFxls['Nuclear'],
                names[2]: CBFxls['Carbón'],
                names[3]: CBFxls['Fuel + Gas'],
                names[4]: CBFxls['Ciclo combinado'],
                names[5]: CBFxls['Total generación'] }

        if len(BAL) == len(CBF):
            for indi1 in range(len(BAL)):
                if len(BAL[names[indi1]]) == 24 and len(CBF[names[indi1]]) == 24:
                    N = len(BAL[names[indi1]])
                lis = list()
                for indi2 in range(N):
                    lis.append( BAL[names[indi1]][indi2] - CBF[names[indi1]][indi2] )
                pyd[names[indi1]] = lis
            dic['ProduccionyDemandaES'] = pyd

        '''
        TOTAL_TERMICA_(3+4+5+6+7+8)
        Total termica es el resultado de sumar las 6 tecnologias incluidas en la variable tt
        '''

        names2 = [ 'NUCLEAR',
                   'CARBON_IMPORTACION',
                   'CARBON_NACIONAL',
                   'CICLO_COMBINADO',
                   'FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)',
                   'FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)' ]

        tt = { names2[0]: pyd[names[1]],
               names2[1]: pyd[names[2]],
               names2[2]: [0] * HORASENUNDIA,
               names2[3]: pyd[names[3]],
               names2[4]: pyd[names[4]],
               names2[5]: [0] * HORASENUNDIA }

        lis = list()
        arr = zeros(N)
        for value in tt.values():
            arr = array(value) + array(arr)
        lis = list(arr)
        dic['ProduccionyDemandaES']['TOTAL_TERMICA_(3+4+5+6+7+8)'] = lis

        '''
        REGIMEN_ESPECIAL_A_MERCADO
        El regimen especial es el resultado de sumar las 6 tecnologias incluidas en la variable names
        '''

        names = [ 'RESTO_HIDRAULICA',
                  'EOLICA',
                  'SOLAR_FOTOVOLTAICO',
                  'SOLAR_TERMICO',
                  'TERMICA_RENOVABLE',
                  'CONGENERACION_Y_RESTO' ]

        BAL = { names[0]: BALxls['Resto hidráulica'],
                names[1]: BALxls['Eólica'],
                names[2]: BALxls['Solar fotovoltaico'],
                names[3]: BALxls['Solar térmico'],
                names[4]: BALxls['Térmica renovable'],
                names[5]: BALxls['Cogeneración y resto'] }

        CBF = { names[0]: CBFxls['Resto hidráulica'],
                names[1]: CBFxls['Eólica'],
                names[2]: CBFxls['Solar fotovoltaico'],
                names[3]: CBFxls['Solar térmico'],
                names[4]: CBFxls['Térmica renovable'],
                names[5]: CBFxls['Cogeneración y resto'] }

        rem = dict()
        if len(BAL) == len(CBF):
            for indi1 in range(len(BAL)):
                if len(BAL[names[indi1]]) == 24 and len(CBF[names[indi1]]) == 24:
                    N = len(BAL[names[indi1]])
                lis = list()
                for indi2 in range(N):
                    lis.append( BAL[names[indi1]][indi2] - CBF[names[indi1]][indi2] )
                rem[names[indi1]] = lis
        lis = list()
        arr = zeros(N)
        for value in rem.values():
            arr = array(value) + array(arr)
        lis = list(arr)
        dic['ProduccionyDemandaES']['REGIMEN_ESPECIAL_A_MERCADO'] = lis

        '''
        'TOTAL_REGIMEN_ESPECIAL_(9+10)'
        Total regimen especial es el resultado de sumar las 2 tecnologias incluidas en la variable tre
        '''

        names3 = [ 'REGIMEN_ESPECIAL_A_MERCADO',
                   'REGIMEN_ESPECIAL_A_DISTRIBUCION' ]

        tre = { names3[0]: lis,
                names2[1]: [0] * HORASENUNDIA }

        lis = list()
        arr = zeros(N)
        for value in tre.values():
            arr = array(value) + array(arr)
        lis = list(arr)
        dic['ProduccionyDemandaES']['TOTAL_REGIMEN_ESPECIAL_(9+10)'] = lis

        '''
        ENERGIAS CONTRATOS BILATERALES
        Existen tecnologias que solo aparecen en el fichero CBF y se añaden directamente al diccionario
        '''

        # TOTAL_CONSUMO_BOMBEO_(24) es igual a CONSUMO_DE_BOMBEO
        # TOTAL_REGIMEN_ORDINARIO_CON_PRIMA es igual a FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)
        names = [ 'UNIDADES_GENERICAS_DEMANDA',
                  'UNIDADES_GENERICAS_PRODUCCION',
                  'TOTAL_IMPORTACION_(11+12+13+14+15)',
                  'TOTAL_EXPORTACIONES_(25+26+27+28+29)',
                  'CONSUMO_DE_BOMBEO',
                  'TOTAL_CONSUMO_BOMBEO_(24)',
                  'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',
                  'TOTAL_GENERICAS_(30+31)',
                  'TOTAL_GENERICAS_(16+17)' ]

        BAL = dict()

        CBF = { names[0]: CBFxls['Unid. Prog. Genéricas Demanda'],
                names[1]: CBFxls['Unid. Prog. Genéricas Produccion'],
                names[2]: CBFxls['Total importaciones'],
                names[3]: CBFxls['Total exportaciones'],
                names[4]: CBFxls['Consumos en bombeo'],
                names[5]: list(),
                names[6]: BALxls['Fuel + Gas'],
                names[7]: list(),
                names[8]: list() }

        CBF[names[5]] = CBF[names[4]]
        CBF[names[7]] = CBF[names[0]]
        CBF[names[8]] = CBF[names[1]]

        for indi in range(len(names)):
            dic['ProduccionyDemandaES'][names[indi]] = CBF[names[indi]]

        '''
        SALDOS IMPORTACIONES EXPORTACIONES
        A partir de los SALDOS del fichero BAL, segun su signo, tenemos dos operaciones diferentes:
        SALDO POSITIVO -> Se le resta el campo IMPORTACIONES del fichero CBF para dar importaciones
        SALDO NEGATIVO -> Se le resta el campo EXPORTACIONES del fichero CBF para dar exportaciones
        '''

        iye = {
        'IMPORTACION_FRANCIA': [0] * HORASENUNDIA,
        'IMPORTACION_PORTUGAL': [0] * HORASENUNDIA,
        'IMPORTACION_MARRUECOS': [0] * HORASENUNDIA,
        'IMPORTACION_ANDORRA': [0] * HORASENUNDIA,
        'EXPORTACION_A_FRANCIA': [0] * HORASENUNDIA,
        'EXPORTACION_A_PORTUGAL': [0] * HORASENUNDIA,
        'EXPORTACION_A_MARRUECOS': [0] * HORASENUNDIA,
        'EXPORTACION_A_ANDORRA': [0] * HORASENUNDIA }

        namesSD = [ 'SALDO_FRANCIA',
                    'SALDO_PORTUGAL',
                    'SALDO_MARRUECOS',
                    'SALDO_ANDORRA' ]

        names = [ 'IMPORTACION_FRANCIA',
                  'IMPORTACION_PORTUGAL',
                  'IMPORTACION_MARRUECOS',
                  'IMPORTACION_ANDORRA',
                  'EXPORTACION_A_FRANCIA',
                  'EXPORTACION_A_PORTUGAL',
                  'EXPORTACION_A_MARRUECOS',
                  'EXPORTACION_A_ANDORRA' ]

        BAL = { namesSD[0]: BALxls['Saldo Francia'],
                namesSD[1]: BALxls['Saldo Portugal'],
                namesSD[2]: BALxls['Saldo Marruecos'],
                namesSD[3]: BALxls['Saldo Andorra'] }

        CBF = { names[0]: CBFxls['Prog. Imp. Francia'],
                names[1]: CBFxls['Prog. Imp. Portugal'],
                names[2]: CBFxls['Prog. Imp. Marruecos'],
                names[3]: CBFxls['Prog. Imp. Andorra'],
                names[4]: CBFxls['Prog. Exp. Francia'],
                names[5]: CBFxls['Prog. Exp. Portugal'],
                names[6]: CBFxls['Prog. Exp. Marruecos'],
                names[7]: CBFxls['Prog. Exp. Andorra'] }

        for indi1 in range(len(namesSD)):
            for indi2 in range(24):
                valor = BAL[namesSD[indi1]][indi2]
                if valor >= 0:
                    ''' importacion '''
                    iye[names[indi1]][indi2] = abs(valor - CBF[names[indi1]][indi2])
                    # iye[names[indi1 + 4]][indi2] = 0.0
                elif valor < 0:
                    ''' exportacion '''
                    iye[names[indi1 + 4]][indi2] = abs(- valor - CBF[names[indi1 + 4]][indi2])
                    # iye[names[indi1]][indi2] = 0.0

        for indi in range(len(names)):
            dic['ProduccionyDemandaES'][names[indi]] = iye[names[indi]]

    else:
        dic['ProduccionyDemandaES'] = {}

    ''' return PreciosES, PreciosPT, PrevisionDemandaES, PrevisionEolicaES, ProduccionyDemandaES '''
    return dic

# from sys import path
# path.append('libs')
# from datetime import datetime
# startDT = datetime(2011,1,1)
# endDT = datetime(2014,5,1)
# from omelinfosys.datosEnFaltaEnergias import findEnFalta
# findEnFalta(startDT,endDT)
def findEnFalta(startDT, endDT):
    '''
    '''

    ONEDAY = timedelta(1)
    collection = Connection().OMIEData.OMIEWebData

    dic = { 'fecha': {},
            'PreciosES': {},
            'PrevisionEolicaES': {},
            'PrevisionDemandaES': {},
            'ProduccionyDemandaES': {} }

    # cursor = collection.find({ "fecha": {"$in": [datetime(2011,1,1)]} })
    # for element in cursor:
    #     print element['fecha']

    # collection.remove({"fecha" : {"$in" : [datetime(2014,1,1)]}})

    iterDT = startDT
    listDT = list()

    vvPreciosES = list()
    chfecha = list()
    vvPrevisionDemandaES = list()
    ecPrevisionDemandaES = list()
    vvPrevisionEolicaES = list()
    ecPrevisionEolicaES = list()

    while (endDT >= iterDT):
        cursor = collection.find({ 'fecha': {'$in': [iterDT]} })
        for element in cursor:
            print iterDT.date()

            ''' fecha '''
            if len(element['PreciosES']) != 24:
                chfecha.append(element['fecha'])

            ''' PreciosES '''
            if element['PreciosES'] == []:
                vvPreciosES.append(element['fecha'])

            ''' PrevisionDemandaES '''
            if element['PrevisionDemandaES'] == []:
                vvPrevisionDemandaES.append(element['fecha'])
            boo = 0
            for pd in element['PrevisionDemandaES']:
                if pd == 0:
                    boo = 1
            if boo == 1:
                ecPrevisionDemandaES.append(element['fecha'])

            ''' PrevisionEolicaES '''
            if element['PrevisionEolicaES'] == []:
                vvPrevisionEolicaES.append(element['fecha'])
            boo = 0
            for pd in element['PrevisionEolicaES']:
                if pd == 0:
                    boo = 1
            if boo == 1:
                ecPrevisionEolicaES.append(element['fecha'])

            ''' ProduccionyDemandaES '''
            listDT.append(element['fecha'])

        iterDT += ONEDAY

    listIT = list()
    # la tupla son intervalos de fechas sin datos (no incluyendo los extremos)
    for indi in range(1,len(listDT)):
        if (listDT[indi] - listDT[indi-1]) != timedelta(days=1):
            listIT.append( (listDT[indi-1], listDT[indi]) )

    # listDT.pop(4) # listDT.pop(24) # listDT.pop(24) # listDT.pop(58) # listDT.pop(58) # listDT.pop(58)

    fvfecha = list()
    # la lista son las fechas en falta
    for tu in listIT:
        dtINI = tu[0]
        dtFIN = tu[1]
        while dtINI < dtFIN - ONEDAY:
            dtINI += ONEDAY
            fvfecha.append(dtINI)

    dic['PreciosES']['vector_vacio'] = vvPreciosES
    dic['fecha']['cambio_hora'] = chfecha
    dic['PrevisionDemandaES']['vector_vacio'] = vvPrevisionDemandaES
    dic['PrevisionDemandaES']['elemento_cero'] = ecPrevisionDemandaES
    dic['PrevisionEolicaES']['vector_vacio'] = vvPrevisionEolicaES
    dic['PrevisionEolicaES']['elemento_cero'] = ecPrevisionEolicaES
    dic['ProduccionyDemandaES']['fecha_vacia'] = fvfecha

    '''
    PreciosES
    '''

    # cursor = collection.find({ "PreciosES": {'$in': [[]]} })
    # for element in cursor:
    #     print element['fecha']
    #     print element['PreciosES']

#     iterDT = startDT
#     listDT = list()
# 
#     while (endDT >= iterDT):
#         cursor = collection.find({ 'fecha': {'$in': [iterDT]} })
#         for element in cursor:
#             if element['PreciosES'] == []:
#                 listDT.append(element['fecha'])
#         iterDT += ONEDAY
#     listDT
#     dic['PreciosES']['vector_vacio'] = listDT
# 
#     iterCH = startDT
#     listCH = list()
# 
#     while (endDT >= iterCH):
#         cursor = collection.find({ 'fecha': {'$in': [iterCH]} })
#         print iterCH.date()
#         for element in cursor:
#             if len(element['PreciosES']) == 23 or len(element['PreciosES']) == 25:
#                 listCH.append(element['fecha'])
#         iterCH += ONEDAY
#     listCH
#     dic['PreciosES']['cambio_hora'] = listCH

    '''
    PrevisionEolicaES
    PrevisionDemandaES
    '''

    # "PrevisionEolicaES" y "PrevisionDemandaES" se tratan ambas de igual modo

    # cursor = collection.find({ "PrevisionDemandaES": {'$in': [[]]} })
    # for element in cursor:
    #     print element['fecha']
    #     print element['PrevisionDemandaES']

#     iterDT = startDT
#     listDT = list()
# 
#     while (endDT >= iterDT):
#         cursor = collection.find({ 'fecha': {'$in': [iterDT]} })
#         print iterDT.date()
#         for element in cursor:
#             if element['PrevisionDemandaES'] == []:
#                 listDT.append(element['fecha'])
#         iterDT += ONEDAY
#     listDT
#     dic['PrevisionDemandaES']['vector_vacio'] = listDT
# 
#     iterDT = startDT
#     listDT = list()
#     listPD = list()
# 
#     while (endDT >= iterDT):
#         cursor = collection.find({ 'fecha': {'$in': [iterDT]} })
#         print iterDT.date()
#         for element in cursor:
#             boo = 0
#             for pd in element['PrevisionDemandaES']:
#                 if pd == 0:
#                     boo = 1
#             if boo == 1:
#                 listDT.append(element['fecha'])
#                 listPD.append(element['PrevisionDemandaES'])
#         iterDT += ONEDAY
#         listDT
#         listPD
#     dic['PrevisionDemandaES']['elemento_cero'] = listDT

    # se comprueba que actualmente NO hay listas vacias en "PrevisionEolicaES"

    # cursor = collection.find({ "PrevisionEolicaES": {'$in': [[]]} })
    # for element in cursor:
    #     print element['fecha']
    #     print element['PrevisionEolicaES']

#     iterDT = startDT
#     listDT = list()
# 
#     while (endDT >= iterDT):
#         cursor = collection.find({ 'fecha': {'$in': [iterDT]} })
#         print iterDT.date()
#         for element in cursor:
#             if element['PrevisionEolicaES'] == []:
#                 listDT.append(element['fecha'])
#         iterDT += ONEDAY
#     listDT
#     dic['PrevisionEolicaES']['vector_vacio'] = listDT
# 
#     iterDT = startDT
#     listDT = list()
#     listPD = list()
# 
#     while (endDT >= iterDT):
#         cursor = collection.find({ 'fecha': {'$in': [iterDT]} })
#         print iterDT.date()
#         for element in cursor:
#             boo = 0
#             for pd in element['PrevisionEolicaES']:
#                 if pd == 0:
#                     boo = 1
#             if boo == 1:
#                 listDT.append(element['fecha'])
#                 listPD.append(element['PrevisionEolicaES'])
#         iterDT += ONEDAY
#         listDT
#         listPD
#     dic['PrevisionEolicaES']['elemento_cero'] = listDT

    '''
    ProduccionyDemandaES
    '''

#     listDT = list()
#     iterDT = startDT
# 
#     while (endDT >= iterDT):
#         cursor = collection.find({ 'fecha': {'$in': [iterDT]} })
#         print iterDT.date()
#         for element in cursor:
#             listDT.append(element['fecha'])
#         iterDT += ONEDAY
#     listDT
# 
#     listT = list()
#     # la tupla son intervalos de fechas sin datos (no incluyendo los extremos)
# 
#     for indi in range(1,len(listDT)):
#         if (listDT[indi] - listDT[indi-1]) != timedelta(days=1):
#             listT.append( (listDT[indi-1], listDT[indi]) )
#     listT
# 
#     # listDT.pop(4) # listDT.pop(24) # listDT.pop(24) # listDT.pop(58) # listDT.pop(58) # listDT.pop(58)
# 
#     listD = list()
#     # la lista son las fechas en falta
# 
#     for tu in listT:
#         dtINI = tu[0]
#         dtFIN = tu[1]
#         while dtINI < dtFIN - ONEDAY:
#             dtINI += ONEDAY
#             listD.append(dtINI)
#     listD
#     dic['ProduccionyDemandaES']['fecha_vacia'] = listD

    return dic

if __name__ == '__main__':
    '''
    '''

    print ''
