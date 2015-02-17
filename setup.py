<<<<<<< HEAD
import os
from setuptools import setup

setup(name='PriceProfor',
      version='0.0',
      description='PriceProfor Zero Alpha',
      author='Hugo Marrao',
      author_email='hmarrao@ekergy.es',
      url='',
      # install_requires=[''],
      # install_requires=open('%s/requirements.txt' % os.environ.get('OPENSHIFT_REPO_DIR', PROJECT_ROOT)).readlines(),
      install_requires=open('requirements.txt').readlines()
,     )
=======
# -*- coding: utf-8 -*

from setuptools import setup

setup(name='priceprofor',
      version='1.0',
      description='Proyecto de Observacion del Mercado Electrico Diario Español',
      author='david, hector, marrao, mundi ',
      author_email='hmarrao@ekergy.es',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['awesome-slugify','bottle','rauth','beaker','pymongo','setuptools',
                        'Jinja2>=2.7.2'],
     )
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
