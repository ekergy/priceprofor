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
