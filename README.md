# microApp para observar los precios del Mercado diario de electricidad.

1. Visualizar precio
2. Hora de Precio Maximo
3. Hora del Precio Minimo



# Publicación de contenido en OpenShift
* Primero debemos comprobar contra que repositorio estamos subiendo los cambios. Para eso tenemos el comando:  
```
#!git

git remote -v
```
* Ahora tenemos que fijar el repositorio de OpenShift con el comando:
```
#!git

git remote set-url origin ssh://53a812b8e0b8cd8a67000159@priceprofor-ekergydavid.rhcloud.com/~/git/priceprofor.git/
```
* Ahora ya podemos hacer commit y push para publicar los cambios en el servidor
* Si queremos volver a fijar el repositorio de bitbucket usamos el comando:
```
#!git

git remote set-url origin https://djuan26@bitbucket.org/ekergy/priceprofor.git
```


## La Maquina principal para los calculos del kernelMarketPredictions es cygnus(192.168.1.154).

TBD or TODO ... Añadir aqui como gestionar esta maquina:

ssh 
ruta proyecto
otras configuraciontes especiales
y software (y paquetes python) que hay que instalar para que el kernel funcione.



