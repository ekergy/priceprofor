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

git remote set-url origin ssh://542bc3bb4382ec4e520010a0@priceprofor-ekergy.rhcloud.com/~/git/priceprofor.git/
```
* Ahora ya podemos hacer commit y push para publicar los cambios en el servidor
* Si queremos volver a fijar el repositorio de bitbucket usamos el comando:
```
#!git

git remote set-url origin https://****usarioBitbucket***@bitbucket.org/ekergy/priceprofor.git
```