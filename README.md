# blockchain

A simple Blockchain in Python. Using Django REST framework.

### Description ###

This is a Django REST implementation of the Daniel van Flymen's [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)

## Installation 

Clone this repository 

	$ git clone https://github.com/kanguarrovi/blockchain.git

Create a virtualenv (on Debian based Linux)

    $ cd blockchain
	$ python3 -m venv env
	$ source env/bin/activate

Upgrade pip if it is needed 

	$ pip install --upgrade pip

Install requirements 

	$ pip install -r requirements.txt

## Run in development

	$ python manage.py runserver

    Go to the browser at 127.0.0.1:8000/chain and begin to use it.