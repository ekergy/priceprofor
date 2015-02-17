<<<<<<< HEAD
# priceprofor
Priceprofor

## Setting up and Running the code:

### if you are a developer config the repo as set in [GITWORKFLOW.md](GITWORKFLOW.md)


### do a standard install:
>   Case:
    You Have a OS with all the needed thinks
    and you only need to run the code and the database script
    to upload data.

#### Step ZERO:
python and pip and easy install should be added to your installed and working in your 
OS/virtualenv/Docker or what ever you use

#### Step 1 python and other stuff:
You must use python-2.7

#### Step 2 code requirements:
pip install -r requirements.txt

#### Step 3 run the server:
python local_run.py



### do a generic install install:
>   Case:
    You only have your machine and you want to install
    the minimum possible to get the server up and running without
    messing directly with your machine OS:

#### Step ZERO:
Activate your virtual env (check [VIRTUALENV.md](VIRTUALENV.md))

#### Step 1 python and other stuff:
You must use python-2.7

#### Step 2 code requirements:
pip install -r requirements.txt

#### Step 3 run the server:
python local_run.py

### Using docker:
>   Case:
    You get the same developing and working functionalities as in a
    standard install but you only need to install the boot2docker thingie

#### Step ZERO setup the docker:
This step depends on the your host OS.
boot2docker is the project to run Docker containers in Windows and in MAC/OSX.
Kernel and you use it as a standar Linux Machine. (You Don't need full virtualbox).
see the head of the Dockerfile to set your docker image and run it!
In the future a docker image will be available in the dockerhub and you only need to pull it from there!

#### Step 1 just run the image as suggested in the Dockerfile















## Setting up the database:

### Use local mongo instance:

### Use a mongolab instance (recommended):

### Use your Docker Container Image:

## Running the code:

### Use your standard Python Installation:

### Use the Python virtualenv (recommended):

### Use your Docker Container:
=======
# Mibel Site

Mible Site es una web que contiene informacion sobre el Mercado Iberico de la Electricidad y que recopila datos publicos disponibles en Internet sobre los balances energeticos en el Mercado Diario en España y Portugal. Estos datos se analizan para sacar estadisticas sobre el comportamiento del mercado y obtener conclusiones

https://sites.google.com/a/ekergy.es/mibelsite/home

# App Android de los precios del Mercado Diario Electrico

https://play.google.com/store/apps/details?id=com.latteandcode.ekergy

1. Visualizar los precios
2. Hora y precio maximo
3. Hora y precio minimo

# Publicacion de contenido en OpenShift


Primero debemos comprobar contra que repositorio estamos subiendo los cambios. Para ello usamos el siguiente comando
```
#!git
git remote -v
```

Si queremos fijar como repositorio OpenShift lo haremos con el comando
```
#!git
git remote set-url origin ssh://542bc3bb4382ec4e520010a0@priceprofor-ekergy.rhcloud.com/~/git/priceprofor.git/
```

Si preferimos fijar como repositorio BitBucket usaremos el comando
```
#!git
git remote set-url origin https://****usarioBitbucket***@bitbucket.org/ekergy/priceprofor.git
```

Ahora ya podemos hacer commit, pull y push para subir los cambios al servidor

# Cron en servidor OpenShift

Esta pagina contiene la documentacion para instalar en OpenShift un modulo Cron y tambien explica como crear con un ejemplo sencillo un script que cada minuto guarda en el log la fecha

https://www.openshift.com/blogs/getting-started-with-cron-jobs-on-openshift

Se resume del proceso de ejecucion Cron desde una url con el codigo en el servidor rhc. Hay que tener en cuenta que el servidor OpenShift tiene uso horario EDT y en local tenemos CEST

La aplicacion Cron tiene que estar instalada en la ruta 
```
#!
$OPENSHIFT_CRON_DIR
```

Los ficheros Log que recopilan el historico estan en la ruta 
```
#!
$OPENSHIFT_LOG_DIR
```

Los ejecutables se encuentran en esta ruta oculta ".openshift" accesible con "ls -la"
```
#!
SERVIDOR $OPENSHIFT_REPO_DIR/.openshift/cron

LOCAL /home/david/workspace/priceprofor/.openshift/cron
```

# Cron en maquina LocalHost

Este es un ejemplo sencillo de como ejecutar un proceso Cron en local. Hay que tener en cuenta que para que en el minuto 15 de cada hora se ejecute el script, debe estar MongoDB conectada

[david@bootes dcron]$ 
pwd
```
#!linux
/home/david/workspace/priceprofor/dcron
```

[david@bootes dcron]$ 
crontab -e
```
#!linux
15 * * * * /bin/sh /home/david/workspace/priceprofor/dcron/preciosMarginalesLocal.sh
```

[david@bootes dcron]$ 
more /home/david/workspace/priceprofor/dcron/preciosMarginalesLocal.sh
```
#!linux
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib/R/lib/
/usr/bin/python2.7 /home/david/workspace/priceprofor/dcron/populatePreciosLocal.py
```

[david@bootes dcron]$ 
more /home/david/workspace/priceprofor/dcron/populatePreciosLocal.py
```
#!linux
from sys import path

path.append('/home/david/workspace/priceprofor/libs')

from dbpreciosesmanager import populatePreciosLocal

populatePreciosLocal()
```
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
