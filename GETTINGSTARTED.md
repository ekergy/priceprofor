# Getting Started with priceprofor server:

1. First clone the repository into a folder of your choice:
	git clone git://github.com/ekergy/priceproforzeroalpha

2. Install a mongodb in your local:
Go to mongodb web site
	http://www.mongodb.org/downloads
Download the installer Mongo (v2.6 is recommend):
	mongodb-linux-x86_64-2.6.7.tgz

3. Start your mongo 2.6 instance:
or example to run on linux
	./mongod

4. It is the priceprofor software requires a python-2.7 installation:
Install python 2.7 and the corresponding pip to your environment

5. We recommend to Set up a virtual env for priceprofor (optional):
You must install virtualenv in your machine
	Check the [VIRTUALENV.md](VIRTUALENV.md)

6. Installing project requirements:
You can check project requirements in the file requirements.txt using pip just type, to install then:
	pip install -r requirements.txt

7. Base de datos mongodb:
We update the database with three collections , prices, technologies and total
The collection totals may take a while to fully charge
	python -m omieinfosys updatedb
