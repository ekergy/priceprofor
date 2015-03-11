# First time configuration:

## for standard contribuitors

* clone the repo:
  ``` 
  git clone https://github.com/ekergy/priceprofor 
  ```

* Now change the name of the remote host
  ```
  git remote rename origin github
  ```
Remember to check the remote github workflow.

## for developers and openshift administrators

* clone the repo:
  ``` 
  git clone https://github.com/ekergy/priceprofor 
  ```

* Now change the name of the remote host
  ```
  git remote rename origin github
  ```

* Now create the remote for openshift (needs to configure your id_rsa.pub to the openshift account):
  ```
  git remote add openshift ssh://53a812b8e0b8cd8a67000159@priceprofor-ekergydavid.rhcloud.com/~/git/priceprofor.git/
  ```

To kept github and openshift repos sync we will use the remote push-only strategy:

* Add a new remote (with name all) using github as base:
  ```
  git remote add all https://github.com/ekergy/priceprofor
  ```
* Configure a push url for all:
  ```
  git remote set-url --add --push all https://github.com/ekergy/priceprofor
  ```
* Configure the other push only url for all:
  ```
  git remote set-url --add --push all ssh://53a812b8e0b8cd8a67000159@priceprofor-ekergydavid.rhcloud.com/~/git/priceprofor.git/
  ```
And you are set to go. To check our config run ``` git remote -v ``` and you should get:
```
all     https://github.com/ekergy/priceprofor (fetch)
all     https://github.com/ekergy/priceprofor (push)
all     ssh://53a812b8e0b8cd8a67000159@priceprofor-ekergydavid.rhcloud.com/~/git/priceprofor.git/ (push)
github  https://github.com/ekergy/priceprofor (fetch)
github  https://github.com/ekergy/priceprofor (push)
openshift       ssh://53a812b8e0b8cd8a67000159@priceprofor-ekergydavid.rhcloud.com/~/git/priceprofor.git/ (fetch)
openshift       ssh://53a812b8e0b8cd8a67000159@priceprofor-ekergydavid.rhcloud.com/~/git/priceprofor.git/ (push)
```
Remember to check the remote all/openshift workflow.

# The git remote github workflow

* Soy un desarrollador standard y quiero contribuir para el proyecto:
  ```
  git fetch github
  ```
  quiero partir del ultimo que haya en el repositorio:
  ```
  git reset github/master
  ```
  y tambien ignorar todas las modificaciones que tenga en mi repositorio y fichero en local:
  ```
  git reset --hard github/master
  ```
* Vale pues he terminado mi desarrollos y hago commit a mis modificaciones:
  ```
  git commit -a -m"mi mensage"
  ```
  y ahora actualizo openshift y github con mis cambios:
  ```
  git push openshift -f
  ```
  y me voy a casa a descansar.

# The git remote all workflow

* Voy iniciar trabajo con el proyecto:
  ```
  git fetch all
  ```
  y ademas quiero partir del ultimo que haya en el repositorio:
  ```
  git reset all/master
  ```
  y tambien ignorar todas las modificaciones que tenga en mi repositorio y fichero en local:
  ```
  git reset --hard all/master
  ```
* Vale pues he terminado mi desarrollos y hago commit a mis modificaciones:
  ```
  git commit -a -m"mi mensage"
  ```
  y ahora actualizo openshift y github con mis cambios:
  ```
  git push all -f
  ```
  y me voy a casa a descansar.

# The git remote openshift workflow

* Hay un problem con el repo y el código solamente en openshift:
  ```
  git fetch openshift
  ```
  quiero partir del ultimo que haya en el repositorio:
  ```
  git reset openshift/master
  ```
  y tambien ignorar todas las modificaciones que tenga en mi repositorio y fichero en local:
  ```
  git reset --hard openshift/master
  ```
* Vale pues he terminado mi desarrollos y hago commit a mis modificaciones:
  ```
  git commit -a -m"mi mensage"
  ```
  y ahora actualizo openshift y github con mis cambios:
  ```
  git push openshift -f
  ```
  y me voy a casa a descansar.