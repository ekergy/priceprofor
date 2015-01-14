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
