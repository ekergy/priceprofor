# -*- coding: utf-8 -*-
"""Running the application on a local machine:

just type:
    $ python wsgi/priceprofor.py

Remmenber to have the mongodb up and running:
Also (it could be a on the same server or in a different one:)

"""
# set up sys path for local run development
import sys

try:
    # add libs and wsgi to python 
    #path to emulate openshift behavior and settings.
    sys.path.append('libs/')
    sys.path.append('wsgi/')
except:
    raise

# importing models to setting the db URI

if __name__ == '__main__':
    import priceprofor
    priceprofor.app.run(debug=True)