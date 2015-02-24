# -*- coding: utf-8 -*-
"""Running the application on a local machine:

just type:
    $ python local_run.py

Remmenber to have the mongodb up and running:
Also (it could be a on the same server or in a different one:)

Test the server:

curl http://localhost:5000/omieinfosys/status
curl -X POST -H "Content-Type: application/json" -d '{"day":"2014-1-1","market":"ES"}' http://localhost:5000/omieinfosys/ReportDay
curl -X POST -H "Content-Type: application/json" -d '{"day":"2014-01-01","market":"ES"}' http://localhost:5000/omieinfosys/ReportDay


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