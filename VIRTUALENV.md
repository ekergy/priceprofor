# Setting up a Virtual environment for python-2.7 to run priceprofor:

install virtual env:
```
sudo easy_install virtualenv
```

create a clean virtualenv for your python:
```
virtualenv env/virt1 --no-site-packages --verbose
```

start your virtualenv:
```
source env/virt1/bin/activate
```

stop/exit your virtualenv:
```
deactivate
```