# -*- coding: utf-8 -*-

"""
Running this unittests:
$ python -m unittest -v test_modul
"""

# importing 
import sys
import os
import unittest
import datetime
try:
    # to import the module needed.
    sys.path.append('..')
    sys.path.append('../..')
except:
    pass
finally:
    # from reeProgramaBaseFuncParser import programabasefuncparser, ProgramaBaseFuncHandler
    from reeinfosys import esiosreeurl, reecontratacionbilateralparser, reeprogramabasefuncparser, reepreveolparser, reeprevdemandaparser, reeenergiagestionadaparser, reepreciosparser
    from reeMercadoDiarioWebParsers import ContratacionBilateralHandler, ProgramaBaseFuncHandler, PrevEolHandler, PrevDemandaHandler, EnergiaGestionadaHandler, PreciosHandler, ProgramaBaseFuncOLDERHandler, ContratacionBilateralOLDERHandler
    # from utilities import validafecha
    from xml.sax import handler, make_parser
    from urllib2 import urlopen
    from pprint import pprint
    

# Constantes:
# funcciones auxiliares:
def validafecha(fecha):
    '''
    valida la fecha que se introduce.
    doctest

    >>> validafecha(datetime.datetime(2012,12,1))
    >>>
    
    >>> validafecha(datetime.datetime.now() + datetime.timedelta(days=2))
    Traceback (most recent call last):
        File "/usr/lib/python2.7/doctest.py", line 1254, in __run
            compileflags, 1) in test.globs
        File "<doctest webdatascraping._validafecha[0]>", line 1, in <module>
            _validafecha(datetime.datetime(2013,12,1))
        File "webdatascraping.py", line 34, in _validafecha
            raise Exception('La fecha selecionada es postrior de la de hoy. No tiene datos disponibles en la web.')
    Exception: La fecha selecionada es postrior de la de hoy. No tiene datos disponibles en la web.
    
    '''
    try:
        if not isinstance(fecha, datetime.datetime):
            raise Exception('El formato fecha no es del tipo correcto.')
        fecha.replace(hour = 11)
        if datetime.datetime.now() < fecha:
            raise Exception('La fecha selecionada es posterior a hoy. No hay datos disponibles en la web.')
        fecha.replace(hour = 0)
    except:
        raise
    else:
        return
# main:
def main():
    unittest.main()

class testREEHandlersLocal(unittest.TestCase):
    """
    This test case should test the function and the class sepreatedly
    """

    def setUp(self):
        # setting up handler in test.
        # print("setting up")
        # import handlers method:
        # inicialize handlers:
        self.fechatest = datetime.datetime(2014,1,1)
        self.assertIsNone(validafecha(self.fechatest))
        self.get_files()
    
    def tearDown(self):
        #print("tearing it down")
        # Delete each inicialized handler.
        pass
        
    def get_files(self):
        try:
            # check if all files exists:
            def esiosreeTestData(xmlid):
                '''
                Check if the proper files exists.
                If not it will try to get data from the website.
                '''
                url = esiosreeurl(self.fechatest, xmlid=xmlid)
                if not os.path.isfile(url[34:]):
                    # if not it will try to get data from the web
                    webFile = urlopen(url)
                    #self.assertIsInstance(webFile,instance)
                    localFile = open(url[34:], 'w')
                    localFile.write(webFile.read())
                    webFile.close()
                    localFile.close()
                self.assertTrue(os.path.isfile(url[34:]))
            # Mapping the needed files and test it existence.
            map(esiosreeTestData,["preveol_DD","demanda_aux","BAL_PBF_DD","CBF_PBF_DD","MD_EGEST_DD","MD_PREC_DD"])
        except:
            raise
        else:
                # must downloadfile using it url.
            # if not it should download the file
            # if yes use the file in disk
            pass

    def test01_ProgramaBaseFuncHandler(self):
        """
        Testing the PrevEolParser class
        """
        
        url = esiosreeurl(self.fechatest, xmlid="BAL_PBF_DD")
        #infile = urlopen(url)
        infile = open(url[34:], 'r')
        parser = make_parser()
        tomatoma = ProgramaBaseFuncHandler()
        parser.setContentHandler(tomatoma)
        parser.parse(infile)
        programabasefunc = tomatoma.parsingresults
        self.assertEqual(programabasefunc,{'FUEL_GAS': {'valores': [448.9, 447.6, 431.9, 421.5, 346.1, 346.1, 346.9, 349.8, 347.0, 346.9, 419.3, 417.5, 429.9, 416.2, 344.1, 343.3, 339.0, 345.3, 431.3, 432.4, 446.8, 447.0, 447.8, 448.3], 'inConceptoAs': False, 'TAGS': [u'Fuel + Gas', u'Fuel + Gas']}, 'TERMICA_RENOVABLE': {'valores': [543.9, 545.0, 545.3, 531.8, 530.9, 531.1, 532.5, 531.9, 527.6, 529.3, 532.8, 533.5, 541.9, 542.4, 541.1, 537.0, 530.2, 537.5, 543.6, 549.4, 549.1, 549.2, 550.8, 551.5], 'inConceptoAs': False, 'TAGS': [u'T\xe9rmica renovable', u'Therm renewable']}, 'SALDO_ANDORRA': {'valores': [-35.0, -34.0, -31.0, -28.0, -27.0, -26.0, -27.0, -27.0, -28.0, -30.0, -33.0, -35.0, -37.0, -39.0, -39.0, -37.0, -36.0, -38.0, -42.0, -45.0, -45.0, -44.0, -40.0, -36.0], 'inConceptoAs': False, 'TAGS': ['Saldo Andorra']}, 'NUCLEAR': {'valores': [6098.9, 6096.9, 6096.9, 6096.9, 6096.9, 6096.9, 6096.9, 6096.9, 6056.6, 6080.6, 6098.9, 6098.9, 6097.9, 6097.9, 6096.9, 6096.9, 6040.6, 6100.9, 6102.9, 6103.9, 6103.9, 6103.9, 6101.9, 6098.9], 'inConceptoAs': False, 'TAGS': [u'Nuclear']}, 'SALDO_FRANCIA': {'valores': [-677.0, -845.0, -1038.0, -894.0, -1094.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1000.0, -950.0, -187.0, 100.0, -250.0, -712.0], 'inConceptoAs': False, 'TAGS': ['Saldo Francia']}, 'EOLICA': {'valores': [9578.4, 9660.4, 9583.0, 9250.3, 9263.4, 9253.8, 9254.4, 9310.3, 9363.7, 9555.7, 9848.6, 10124.7, 10544.8, 10776.7, 11044.3, 11217.8, 11350.9, 11704.0, 11996.0, 12276.0, 12233.9, 12189.3, 12210.2, 12313.8], 'inConceptoAs': False, 'TAGS': [u'E\xf3lica', u'Wind']}, 'HIDRAULICA': {'valores': [3823.5, 2881.0, 2043.6, 1927.7, 1872.3, 1877.3, 1877.3, 2125.8, 2125.9, 2226.6, 2319.5, 2426.3, 2555.6, 2752.8, 2784.3, 2766.2, 2881.3, 3129.7, 3489.9, 4254.3, 4757.8, 4806.5, 4635.9, 3630.1], 'inConceptoAs': False, 'TAGS': [u'Hidr\xe1ulica (UGH + Turb. Bomb.)', u'Hydro (UGH + Pump. Gen.)']}, 'CONSUMO_DE_BOMBEO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Consumo Bombeo']}, 'SOLAR_TERMICO': {'valores': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 12.8, 16.5, 56.8, 135.2, 148.5, 146.9, 147.5, 121.3, 121.3, 72.2, 31.0, 24.4, 11.8, 10.0, 10.0, 10.0], 'inConceptoAs': False, 'TAGS': [u'Solar t\xe9rmico', u'Solar thermal']}, 'CICLO_COMBINADO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Combined cycle GT', u'Ciclo Combinado']}, 'COGENERACION_Y_RESTO': {'valores': [2133.1, 2104.9, 2104.6, 2104.1, 2104.7, 2104.7, 2120.5, 2116.9, 2150.9, 2182.2, 2192.5, 2194.6, 2193.8, 2195.4, 2195.2, 2205.0, 2183.9, 2202.0, 2208.6, 2222.8, 2226.1, 2231.9, 2251.0, 2256.6], 'inConceptoAs': False, 'TAGS': [u'Cogeneraci\xf3n y resto', u'Cogeneration and rest']}, 'SALDO_MARRUECOS': {'valores': [-400.0, -300.0, -200.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -300.0, -450.0, -650.0, -650.0, -650.0, -600.0, -300.0], 'inConceptoAs': False, 'TAGS': ['Saldo Marruecos']}, 'CARBON': {'valores': [837.0, 803.5, 770.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 166.8, 85.7, 0], 'inConceptoAs': False, 'TAGS': [u'Coal', u'Carb\xf3n']}, 'SALDO_PORTUGAL': {'valores': [203.8, -184.7, -476.5, -300.9, -369.1, -99.7, 145.8, 437.2, 674.3, 1146.2, 962.3, 800.3, 980.2, 546.5, 654.6, 1072.9, 1181.5, 1196.0, 1129.2, 883.6, 873.0, 1020.0, 1145.9, 954.9], 'inConceptoAs': False, 'TAGS': ['Saldo Portugal']}, 'SOLAR_FOTOVOLTAICO': {'valores': [13.7, 13.4, 13.4, 12.3, 12.0, 11.8, 11.8, 58.0, 158.5, 575.8, 1179.6, 1564.5, 1748.5, 1766.0, 1587.8, 1309.9, 837.3, 392.2, 193.4, 124.9, 69.8, 14.4, 12.1, 12.3], 'inConceptoAs': False, 'TAGS': [u'Solar fotovoltaico', u'Solar PV']}, 'HIDRAULICA_OTROS': {'valores': [866.9, 848.5, 841.6, 820.8, 822.5, 819.0, 820.7, 811.0, 810.0, 824.9, 829.1, 847.0, 860.1, 866.9, 865.3, 848.8, 836.9, 848.0, 856.6, 878.5, 887.2, 899.8, 890.5, 875.4], 'inConceptoAs': False, 'TAGS': [u'Resto hidr\xe1ulica', u'Rest hydro']}})

    def test02_programabasefuncparser(self):
        """
        Testing the preveolparser function
        """
        
        programabasefunc = reeprogramabasefuncparser(self.fechatest)

        self.assertEqual(programabasefunc,{'FUEL_GAS': {'valores': [448.9, 447.6, 431.9, 421.5, 346.1, 346.1, 346.9, 349.8, 347.0, 346.9, 419.3, 417.5, 429.9, 416.2, 344.1, 343.3, 339.0, 345.3, 431.3, 432.4, 446.8, 447.0, 447.8, 448.3], 'inConceptoAs': False, 'TAGS': [u'Fuel + Gas', u'Fuel + Gas']}, 'TERMICA_RENOVABLE': {'valores': [543.9, 545.0, 545.3, 531.8, 530.9, 531.1, 532.5, 531.9, 527.6, 529.3, 532.8, 533.5, 541.9, 542.4, 541.1, 537.0, 530.2, 537.5, 543.6, 549.4, 549.1, 549.2, 550.8, 551.5], 'inConceptoAs': False, 'TAGS': [u'T\xe9rmica renovable', u'Therm renewable']}, 'SALDO_ANDORRA': {'valores': [-35.0, -34.0, -31.0, -28.0, -27.0, -26.0, -27.0, -27.0, -28.0, -30.0, -33.0, -35.0, -37.0, -39.0, -39.0, -37.0, -36.0, -38.0, -42.0, -45.0, -45.0, -44.0, -40.0, -36.0], 'inConceptoAs': False, 'TAGS': ['Saldo Andorra']}, 'NUCLEAR': {'valores': [6098.9, 6096.9, 6096.9, 6096.9, 6096.9, 6096.9, 6096.9, 6096.9, 6056.6, 6080.6, 6098.9, 6098.9, 6097.9, 6097.9, 6096.9, 6096.9, 6040.6, 6100.9, 6102.9, 6103.9, 6103.9, 6103.9, 6101.9, 6098.9], 'inConceptoAs': False, 'TAGS': [u'Nuclear']}, 'SALDO_FRANCIA': {'valores': [-677.0, -845.0, -1038.0, -894.0, -1094.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1100.0, -1000.0, -950.0, -187.0, 100.0, -250.0, -712.0], 'inConceptoAs': False, 'TAGS': ['Saldo Francia']}, 'EOLICA': {'valores': [9578.4, 9660.4, 9583.0, 9250.3, 9263.4, 9253.8, 9254.4, 9310.3, 9363.7, 9555.7, 9848.6, 10124.7, 10544.8, 10776.7, 11044.3, 11217.8, 11350.9, 11704.0, 11996.0, 12276.0, 12233.9, 12189.3, 12210.2, 12313.8], 'inConceptoAs': False, 'TAGS': [u'E\xf3lica', u'Wind']}, 'HIDRAULICA': {'valores': [3823.5, 2881.0, 2043.6, 1927.7, 1872.3, 1877.3, 1877.3, 2125.8, 2125.9, 2226.6, 2319.5, 2426.3, 2555.6, 2752.8, 2784.3, 2766.2, 2881.3, 3129.7, 3489.9, 4254.3, 4757.8, 4806.5, 4635.9, 3630.1], 'inConceptoAs': False, 'TAGS': [u'Hidr\xe1ulica (UGH + Turb. Bomb.)', u'Hydro (UGH + Pump. Gen.)']}, 'CONSUMO_DE_BOMBEO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Consumo Bombeo']}, 'SOLAR_TERMICO': {'valores': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 12.8, 16.5, 56.8, 135.2, 148.5, 146.9, 147.5, 121.3, 121.3, 72.2, 31.0, 24.4, 11.8, 10.0, 10.0, 10.0], 'inConceptoAs': False, 'TAGS': [u'Solar t\xe9rmico', u'Solar thermal']}, 'CICLO_COMBINADO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Combined cycle GT', u'Ciclo Combinado']}, 'COGENERACION_Y_RESTO': {'valores': [2133.1, 2104.9, 2104.6, 2104.1, 2104.7, 2104.7, 2120.5, 2116.9, 2150.9, 2182.2, 2192.5, 2194.6, 2193.8, 2195.4, 2195.2, 2205.0, 2183.9, 2202.0, 2208.6, 2222.8, 2226.1, 2231.9, 2251.0, 2256.6], 'inConceptoAs': False, 'TAGS': [u'Cogeneraci\xf3n y resto', u'Cogeneration and rest']}, 'SALDO_MARRUECOS': {'valores': [-400.0, -300.0, -200.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -300.0, -450.0, -650.0, -650.0, -650.0, -600.0, -300.0], 'inConceptoAs': False, 'TAGS': ['Saldo Marruecos']}, 'CARBON': {'valores': [837.0, 803.5, 770.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 166.8, 85.7, 0], 'inConceptoAs': False, 'TAGS': [u'Coal', u'Carb\xf3n']}, 'SALDO_PORTUGAL': {'valores': [203.8, -184.7, -476.5, -300.9, -369.1, -99.7, 145.8, 437.2, 674.3, 1146.2, 962.3, 800.3, 980.2, 546.5, 654.6, 1072.9, 1181.5, 1196.0, 1129.2, 883.6, 873.0, 1020.0, 1145.9, 954.9], 'inConceptoAs': False, 'TAGS': ['Saldo Portugal']}, 'SOLAR_FOTOVOLTAICO': {'valores': [13.7, 13.4, 13.4, 12.3, 12.0, 11.8, 11.8, 58.0, 158.5, 575.8, 1179.6, 1564.5, 1748.5, 1766.0, 1587.8, 1309.9, 837.3, 392.2, 193.4, 124.9, 69.8, 14.4, 12.1, 12.3], 'inConceptoAs': False, 'TAGS': [u'Solar fotovoltaico', u'Solar PV']}, 'HIDRAULICA_OTROS': {'valores': [866.9, 848.5, 841.6, 820.8, 822.5, 819.0, 820.7, 811.0, 810.0, 824.9, 829.1, 847.0, 860.1, 866.9, 865.3, 848.8, 836.9, 848.0, 856.6, 878.5, 887.2, 899.8, 890.5, 875.4], 'inConceptoAs': False, 'TAGS': [u'Resto hidr\xe1ulica', u'Rest hydro']}})

    def test03_PrevEolHandler(self):
        """
        Testing the PrevEolParser class
        """
        url = esiosreeurl(self.fechatest, xmlid="preveol_DD")
        #infile = urlopen(url)
        infile = open(url[34:], 'r')
        parser = make_parser()
        tomatoma = PrevEolHandler()
        parser.setContentHandler(tomatoma)
        parser.parse(infile)
        previsioneolica = tomatoma.listavalores
        self.assertEqual(previsioneolica,[10790, 10885, 10984, 10680, 10605, 10531, 10257, 9895, 9759, 9841, 8889, 9312, 9979, 10704, 10758, 10938, 11051, 11489, 11769, 11661, 11791, 11960, 12126, 12387])

    def test04_reepreveolparser(self):
        """
        Testing the preveolparser function
        """
        previsioneolica = reepreveolparser(self.fechatest)
        self.assertEqual(previsioneolica,[10790, 10885, 10984, 10680, 10605, 10531, 10257, 9895, 9759, 9841, 8889, 9312, 9979, 10704, 10758, 10938, 11051, 11489, 11769, 11661, 11791, 11960, 12126, 12387])

    def test05_PrevDemandaHandler(self):
        """
        Testing the PrevEolParser class
        """
        url = esiosreeurl(self.fechatest, xmlid="demanda_aux")
        #infile = urlopen(url)
        infile = open(url[34:], 'r')
        parser = make_parser()
        tomatoma = PrevDemandaHandler()
        parser.setContentHandler(tomatoma)
        parser.parse(infile)
        previsiondemanda = tomatoma.listavalores
        self.assertEqual(previsiondemanda,[23793, 22670, 21164, 19628, 18695, 18355, 18386, 18695, 18695, 19190, 21476, 23052, 24164, 24627, 24195, 22658, 22320, 22871, 25112, 26818, 27678, 29524, 28805, 26803])

    def test06_reeprevdemandaparser(self):
        """
        Testing the preveolparser function
        """
        previsiondemanda = reeprevdemandaparser(self.fechatest)
        self.assertEqual(previsiondemanda,[23793, 22670, 21164, 19628, 18695, 18355, 18386, 18695, 18695, 19190, 21476, 23052, 24164, 24627, 24195, 22658, 22320, 22871, 25112, 26818, 27678, 29524, 28805, 26803])

    def test07_EnergiaGestionadaHandler(self):
        """
        Testing the PrevEolParser class
        """
        """
        Testing the PrevEolParser class
        """
        url = esiosreeurl(self.fechatest, xmlid="MD_EGEST_DD")
        #infile = urlopen(url)
        infile = open(url[34:], 'r')
        parser = make_parser()
        tomatoma = EnergiaGestionadaHandler()
        parser.setContentHandler(tomatoma)
        parser.parse(infile)
        energiagestionada = tomatoma.listavalores
        self.assertEqual(energiagestionada,[21334.9, 20298.0, 22597.7, 20590.9, 20434.2, 20426.1, 20592.2, 21223.2, 21602.7, 22860.1, 23814.8, 24517.9, 25626.6, 25483.1, 25636.5, 25894.5, 25678.3, 25903.2, 26507.9, 23383.0, 20007.9, 20546.3, 24119.3, 23114.1])

    def test08_reeenergiagestionadaparser(self):
        """
        Testing the preveolparser function
        """
        energiagestionada = reeenergiagestionadaparser(self.fechatest)
        self.assertEqual(energiagestionada,[21334.9, 20298.0, 22597.7, 20590.9, 20434.2, 20426.1, 20592.2, 21223.2, 21602.7, 22860.1, 23814.8, 24517.9, 25626.6, 25483.1, 25636.5, 25894.5, 25678.3, 25903.2, 26507.9, 23383.0, 20007.9, 20546.3, 24119.3, 23114.1])

    def test09_ContratacionBilateralHandler(self):
        """
        Testing the PrevEolParser class
        """
        url = esiosreeurl(self.fechatest, xmlid="CBF_PBF_DD")
        #infile = urlopen(url)
        infile = open(url[34:], 'r')
        parser = make_parser()
        tomatoma = ContratacionBilateralHandler()
        parser.setContentHandler(tomatoma)
        parser.parse(infile)
        contratacionbilateral = tomatoma.parsingresults
        self.assertEqual(contratacionbilateral,{'FUEL_GAS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Fuel + Gas', u'Fuel + Gas']}, 'TERMICA_RENOVABLE': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'T\xe9rmica renovable', u'Therm renewable']}, 'NUCLEAR': {'valores': [2736.8, 2736.8, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 2736.8, 5332.8, 5332.8, 2736.8, 2736.8], 'inConceptoAs': False, 'TAGS': [u'Nuclear']}, 'IMPORTACION_MARRUECOS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Marruecos']}, 'EOLICA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'E\xf3lica', u'Wind']}, 'EXPORTACION_A_FRANCIA': {'valores': [0, 0, 0, 29.0, 29.0, 29.0, 29.0, 0, 180.0, 0, 0, 0, 0, 0, 0, 0, 0, 180.0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Francia']}, 'HIDRAULICA': {'valores': [1767.8, 1277.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1919.8, 3209.1, 3212.9, 1947.3, 1550.3], 'inConceptoAs': False, 'TAGS': [u'Hidr\xe1ulica (UGH + Turb. Bomb.)', u'Hydro (UGH + Pump. Gen.)']}, 'IMPORTACION_FRANCIA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40.0, 40.0, 40.0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Francia']}, 'CONSUMO_DE_BOMBEO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Consumo Bombeo']}, 'EXPORTACION_A_MARRUECOS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Marruecos']}, 'SOLAR_TERMICO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Solar t\xe9rmico', u'Solar thermal']}, 'IMPORTACION_ANDORRA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Andorra']}, 'CICLO_COMBINADO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Combined cycle GT', u'Ciclo Combinado']}, 'COGENERACION_Y_RESTO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Cogeneraci\xf3n y resto', u'Cogeneration and rest']}, 'IMPORTACION_PORTUGAL': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Portugal']}, 'CARBON': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Coal', u'Carb\xf3n']}, 'EXPORTACION_A_ANDORRA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7.0, 16.0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Andorra']}, 'SOLAR_FOTOVOLTAICO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Solar fotovoltaico', u'Solar PV']}, 'HIDRAULICA_OTROS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Resto hidr\xe1ulica', u'Rest hydro']}, 'EXPORTACION_A_PORTUGAL': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Portugal']}})

    def test10_reecontratacionbilateralparser(self):
        """
        Testing the preveolparser function
        """
        contratacionbilateral = reecontratacionbilateralparser(self.fechatest)
        self.assertEqual(contratacionbilateral,{'FUEL_GAS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Fuel + Gas', u'Fuel + Gas']}, 'TERMICA_RENOVABLE': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'T\xe9rmica renovable', u'Therm renewable']}, 'NUCLEAR': {'valores': [2736.8, 2736.8, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 674.0, 2736.8, 5332.8, 5332.8, 2736.8, 2736.8], 'inConceptoAs': False, 'TAGS': [u'Nuclear']}, 'IMPORTACION_MARRUECOS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Marruecos']}, 'EOLICA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'E\xf3lica', u'Wind']}, 'EXPORTACION_A_FRANCIA': {'valores': [0, 0, 0, 29.0, 29.0, 29.0, 29.0, 0, 180.0, 0, 0, 0, 0, 0, 0, 0, 0, 180.0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Francia']}, 'HIDRAULICA': {'valores': [1767.8, 1277.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1919.8, 3209.1, 3212.9, 1947.3, 1550.3], 'inConceptoAs': False, 'TAGS': [u'Hidr\xe1ulica (UGH + Turb. Bomb.)', u'Hydro (UGH + Pump. Gen.)']}, 'IMPORTACION_FRANCIA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40.0, 40.0, 40.0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Francia']}, 'CONSUMO_DE_BOMBEO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Consumo Bombeo']}, 'EXPORTACION_A_MARRUECOS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Marruecos']}, 'SOLAR_TERMICO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Solar t\xe9rmico', u'Solar thermal']}, 'IMPORTACION_ANDORRA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Andorra']}, 'CICLO_COMBINADO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Combined cycle GT', u'Ciclo Combinado']}, 'COGENERACION_Y_RESTO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Cogeneraci\xf3n y resto', u'Cogeneration and rest']}, 'IMPORTACION_PORTUGAL': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Portugal']}, 'CARBON': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Coal', u'Carb\xf3n']}, 'EXPORTACION_A_ANDORRA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7.0, 16.0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Andorra']}, 'SOLAR_FOTOVOLTAICO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Solar fotovoltaico', u'Solar PV']}, 'HIDRAULICA_OTROS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Resto hidr\xe1ulica', u'Rest hydro']}, 'EXPORTACION_A_PORTUGAL': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Portugal']}})

    def test11_PreciosHandler(self):
        """
        Testing the PreciosHandler class function
        """
        url = esiosreeurl(self.fechatest, xmlid="MD_PREC_DD")
        #infile = urlopen(url)
        infile = open(url[34:], 'r')
        parser = make_parser()
        tomatoma = PreciosHandler()
        parser.setContentHandler(tomatoma)
        parser.parse(infile)
        preciosespanha = tomatoma.listavalores
        self.assertEqual(preciosespanha,[20.02, 10.34, 5.35, 5.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.75, 5.35, 4.9, 0.9, 0.0, 0.0, 0.0, 5.0, 7.8, 18.9, 20.0, 20.0, 8.6])

    def test12_reepreciosparser(self):
        """
        Testing the reepreciosparser function
        """
        preciosespanha = reepreciosparser(self.fechatest)
        self.assertEqual(preciosespanha,[20.02, 10.34, 5.35, 5.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.75, 5.35, 4.9, 0.9, 0.0, 0.0, 0.0, 5.0, 7.8, 18.9, 20.0, 20.0, 8.6])

    def test13_ProgramaBaseFuncOLDERHandler(self):
        """
        Testing the PreciosHandler class function
        ProgramaBaseFuncOLDERHandler
        """
        url = esiosreeurl(datetime.datetime(2012,1,1), xmlid="BAL_PBF_DD")
        infile = urlopen(url)
        parser = make_parser()
        tomatoma = ProgramaBaseFuncOLDERHandler()
        parser.setContentHandler(tomatoma)
        parser.parse(infile)
        programabasefuncOLDER = tomatoma.parsingresults
        self.assertEqual(programabasefuncOLDER,{'CONSUMO_DE_BOMBEO': {'valores': [0.0, 0.0, -49.3, -842.2, -1320.7, -1250.8, -1261.3, -830.0, -1140.0, -1351.0, -648.0, -380.0, -600.8, -714.6, -780.7, -1006.0, -1157.0, -934.0, -660.1, -700.0, -546.5, 0.0, -314.6, -772.0], 'inConceptoAs': False, 'TAGS': [u'Consumo Bombeo']}, 'FUEL_GAS': {'valores': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8, 15.8], 'inConceptoAs': False, 'TAGS': [u'Fuel-Gas']}, 'TERMICA_RENOVABLE': {'valores': [552.8, 557.4, 517.4, 509.5, 509.3, 505.1, 504.0, 504.9, 505.1, 539.7, 540.3, 541.3, 550.8, 550.3, 550.7, 550.5, 550.7, 551.0, 587.8, 588.3, 587.8, 588.3, 589.4, 589.2], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. T\xe9rmico Renovable']}, 'CICLO_COMBINADO': {'valores': [746.0, 460.0, 0.0, 0.0, 0.0, 0.0, 0.0, 300.0, 367.3, 500.4, 830.4, 938.4, 938.4, 830.4, 730.4, 718.7, 500.4, 730.4, 830.4, 830.4, 938.4, 1074.4, 1038.4, 570.9], 'inConceptoAs': False, 'TAGS': [u'Combined cycle GT', u'Ciclo Combinado']}, 'SALDO_ANDORRA': {'valores': [], 'inConceptoAs': False, 'TAGS': ['Saldo Andorra']}, 'NUCLEAR': {'valores': [6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8, 6488.8], 'inConceptoAs': False, 'TAGS': [u'Nuclear']}, 'SALDO_FRANCIA': {'valores': [], 'inConceptoAs': False, 'TAGS': ['Saldo Francia']}, 'EOLICA': {'valores': [7102.1, 6924.7, 6340.6, 6162.8, 5983.7, 5842.2, 5712.2, 5624.4, 5529.1, 5517.8, 5499.0, 5563.5, 5846.2, 5968.2, 6152.4, 6430.8, 6715.6, 7140.9, 8007.0, 8502.3, 8978.0, 9325.3, 9630.5, 9806.1], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. E\xf3lico']}, 'HIDRAULICA': {'valores': [2191.1, 1558.7, 1320.6, 1232.5, 1208.4, 1204.0, 1200.9, 1200.8, 1200.8, 1250.6, 944.0, 1005.3, 1121.9, 1131.9, 1238.5, 1138.4, 1221.0, 1286.4, 2721.6, 3711.3, 4123.9, 4191.7, 3988.3, 3565.9], 'inConceptoAs': False, 'TAGS': [u'Hidr\xe1ulica Convencional']}, 'REGIMEN_ORDINARIO_CON_PRIMA': {'valores': [469.2, 484.9, 486.2, 471.5, 469.9, 470.6, 470.2, 470.0, 469.1, 468.8, 465.4, 476.4, 474.2, 457.9, 456.3, 464.2, 480.4, 483.5, 485.0, 487.5, 503.6, 506.4, 508.0, 493.4], 'inConceptoAs': False, 'TAGS': [u'R\xe9gimen ordinario con prima']}, 'COGENERACION_Y_RESTO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Cogeneraci\xf3n y resto', u'Cogeneration and rest']}, 'SOLAR_TERMICO': {'valores': [1.3, 0.9, 0.9, 0.9, 0.7, 0.8, 0.8, 3.5, 12.4, 45.5, 149.6, 385.8, 499.1, 482.1, 499.7, 561.9, 588.3, 405.9, 123.4, 82.5, 33.7, 21.9, 1.2, 1.3], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. Solar T\xe9rmico']}, 'HIDRAULICA_BOMBEO': {'valores': [809.7, 340.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 230.0, 65.0, 580.0, 325.0, 0.0, 78.0, 78.0, 78.0, 658.0, 600.2, 658.0, 738.0, 738.0, 209.6], 'inConceptoAs': False, 'TAGS': [u'Turbinaci\xf3n bombeo']}, 'TERMICA_NORENOVABLE': {'valores': [2366.0, 2365.7, 2299.4, 2307.1, 2306.4, 2306.3, 2312.2, 2309.7, 2306.2, 2343.2, 2341.0, 2336.2, 2336.6, 2333.5, 2330.9, 2330.0, 2346.8, 2353.1, 2410.9, 2419.6, 2420.9, 2423.6, 2428.9, 2437.5], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. T\xe9rmico no Renov.']}, 'OTRAS_RENOVABLE': {'valores': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. Otras Renovables']}, 'SALDO_MARRUECOS': {'valores': [], 'inConceptoAs': False, 'TAGS': ['Saldo Marruecos']}, 'CARBON': {'valores': [2835.0, 2806.5, 2685.5, 1826.5, 1451.5, 1451.5, 1706.5, 1706.5, 1541.0, 1551.7, 1852.5, 2094.0, 2094.0, 2094.0, 2094.0, 1201.0, 1201.0, 1419.0, 2094.0, 2094.0, 2094.0, 2094.0, 2094.0, 2094.0], 'inConceptoAs': False, 'TAGS': [u'Coal', u'Carb\xf3n']}, 'SALDO_PORTUGAL': {'valores': [], 'inConceptoAs': False, 'TAGS': ['Saldo Portugal']}, 'SOLAR_FOTOVOLTAICO': {'valores': [12.9, 12.9, 13.1, 13.1, 13.1, 12.9, 13.3, 46.3, 252.5, 1035.2, 1595.1, 1862.3, 2025.0, 2064.7, 1887.3, 1590.8, 1047.4, 332.4, 35.7, 32.5, 12.3, 12.7, 12.9, 13.0], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. Solar Fotovoltaico']}, 'HIDRAULICA_OTROS': {'valores': [559.2, 523.4, 413.6, 403.0, 401.4, 400.8, 400.1, 393.8, 398.2, 406.0, 409.4, 424.6, 439.5, 443.3, 437.3, 420.9, 437.2, 472.8, 566.4, 571.5, 584.4, 587.4, 578.5, 549.2], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. Hidr\xe1ulico']}})
        
    def test14_ContratacionBilateralOLDERHandler(self):
        """
        Testing the PreciosHandler class function
        ProgramaBaseFuncOLDERHandler
        """
        url = esiosreeurl(datetime.datetime(2012,1,1), xmlid="CBF_PBF_DD")
        infile = urlopen(url)
        parser = make_parser()
        tomatoma = ContratacionBilateralOLDERHandler()
        parser.setContentHandler(tomatoma)
        parser.parse(infile)
        contratacionbilateralOLDER = tomatoma.parsingresults
        self.assertEqual(contratacionbilateralOLDER,{'EXPORTACION_A_FRANCIA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Francia']}, 'NUCLEAR': {'valores': [5182.0, 5182.0, 5182.0, 5160.1, 5035.5, 5037.2, 5102.6, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0, 5182.0], 'inConceptoAs': False, 'TAGS': [u'Nuclear']}, 'EOLICA': {'valores': [354.2, 354.3, 347.4, 336.4, 323.9, 311.9, 298.5, 299.4, 304.9, 310.4, 316.4, 314.9, 298.1, 304.9, 315.0, 327.6, 330.7, 337.7, 350.3, 361.6, 366.4, 369.6, 383.3, 396.6], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. E\xf3lico']}, 'CARBON': {'valores': [864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0, 864.0], 'inConceptoAs': False, 'TAGS': [u'Coal', u'Carb\xf3n']}, 'COGENERACION_Y_RESTO': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'Cogeneraci\xf3n y resto', u'Cogeneration and rest']}, 'IMPORTACION_MARRUECOS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Marruecos']}, 'TERMICA_RENOVABLE': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. T\xe9rmico Renovable']}, 'HIDRAULICA': {'valores': [1406.6, 771.6, 555.9, 320.2, 318.2, 316.2, 317.2, 432.1, 437.3, 499.6, 478.9, 499.9, 565.4, 576.2, 597.1, 553.1, 580.1, 632.6, 1882.2, 2680.4, 3051.8, 3120.8, 2970.7, 2625.1], 'inConceptoAs': False, 'TAGS': [u'Hidr\xe1ulica Convencional']}, 'REGIMEN_ORDINARIO_CON_PRIMA': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'R\xe9gimen ordinario con prima']}, 'CONSUMO_DE_BOMBEO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Consumo Bombeo']}, 'CICLO_COMBINADO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 0], 'inConceptoAs': False, 'TAGS': [u'Combined cycle GT', u'Ciclo Combinado']}, 'EXPORTACION_A_PORTUGAL': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Portugal']}, 'SOLAR_TERMICO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. Solar T\xe9rmico']}, 'IMPORTACION_PORTUGAL': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Portugal']}, 'FUEL_GAS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Fuel-Gas']}, 'EXPORTACION_A_MARRUECOS': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Marruecos']}, 'HIDRAULICA_BOMBEO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'Turbinaci\xf3n bombeo']}, 'IMPORTACION_FRANCIA': {'valores': [430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0, 430.0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Francia']}, 'HIDRAULICA_OTROS': {'valores': [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. Hidr\xe1ulico']}, 'TERMICA_NORENOVABLE': {'valores': [], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. T\xe9rmico no Renov.']}, 'OTRAS_RENOVABLE': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. Otras Renovables']}, 'SOLAR_FOTOVOLTAICO': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': [u'R\xe9g. Esp. Solar Fotovoltaico']}, 'IMPORTACION_ANDORRA': {'valores': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'inConceptoAs': False, 'TAGS': ['Prog. Imp. Andorra']}, 'EXPORTACION_A_ANDORRA': {'valores': [51.0, 48.0, 44.0, 41.0, 39.0, 37.0, 38.0, 39.0, 40.0, 44.0, 49.0, 52.0, 55.0, 60.0, 59.0, 55.0, 53.0, 55.0, 63.0, 64.0, 66.0, 65.0, 61.0, 53.0], 'inConceptoAs': False, 'TAGS': ['Prog. Exp. Andorra']}})
        