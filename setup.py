from setuptools import setup

setup(name='priceprofor',
      version='1.0',
      description='Proyecto de Observacion del Mercado Electrico Diario Español',
      author='david, hector, marrao, mundi ',
      author_email='hmarrao@ekergy.es',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['bottle','rauth','beaker','pymongo','setuptools',
                        'awesome-slugify',
                        'Jinja2>=2.7.2'],
     )
