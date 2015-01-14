# priceprofor
Priceprofor

## This repository contains the code running in openshif:
Connect to github:
```
git remote set-url origin https://github.com/ekergy/priceprofor
```
Connect to openshift:
```
git remote set-url origin ssh://54ae44054382ec0f69000247@price-profor.rhcloud.com/~/git/price.git/
```

## Setting up and Running the code:

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

#### Step 3 code requirements:
python local_run.py



### do a generic install install:
>   Case:
    You only have your machine and you want to install
    the minimum possible to get the server up and running without
    messing directly with your machine OS:

#### Step ZERO:
Activate your virtual env (check VIRTUALENV.md)

#### Step 1 python and other stuff:
You must use python-2.7

#### Step 2 code requirements:
pip install -r requirements.txt

#### Step 3 code requirements:
python local_run.py

### Using docker:
>   Case:
    You get the same developing and working functionalities as in a
    standard install but you only need to install the boot2docker thingie

#### Step 1 setup the boot2docker:
This step start a virtual Machine in your host OS then you have a linux
Kernel and you use it as a standar Linux Machine. (You Don't need full virtualbox).















## Setting up the database:

### Use local mongo instance:

### Use a mongolab instance (recommended):

### Use your Docker Container Image:

## Running the code:

### Use your standard Python Installation:

### Use the Python virtualenv (recommended):

### Use your Docker Container: