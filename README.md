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

# MicroApp para visualizar los precios del Mercado Diario de la electricidad

https://play.google.com/store/apps/details?id=com.latteandcode.ekergy

1. Visualizar los precios
2. Hora y precio maximo
3. Hora y precio minimo
