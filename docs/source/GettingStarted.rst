=================
 Getting Started
=================

Use the Docker Image:
=====================

1. 

Get the code:
=============

1. 

Select your Install Environment:
++++++++++++++++++++++++++++++++

1. Install the package along with Sphinx.

   There are two ways to install the extension. Using pip::

     $ pip install sphinxcontrib-fulltoc

   or from the source tree::

     $ python setup.py install

2. Add the extension to the list in your ``conf.py`` settings file for
   each project where you want to use it::

      # conf.py
      ...
      extensions = ['sphinxcontrib.fulltoc']
      ...
      
3. Rebuild all of the HTML output for your project.