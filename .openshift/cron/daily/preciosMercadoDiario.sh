#/!bin/bash
date >> $OPENSHIFT_LOG_DIR/fechaDiaria.log
wget http://profor-ekergy.rhcloud.com/populatePrecios
