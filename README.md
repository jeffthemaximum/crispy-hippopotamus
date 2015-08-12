Crispy Hippopotamus
======

Readme last edited: August 12, 2015
Who is responsible for this disaster: Jeff Maxim

This is my attempt to create a browser based graphical user interface for xboard compatible chess chess engines, such as gnuchess. Basically, it's a browser-based version of xboard. Hopefully, it'll let you play against some of the best winboard/UCI chess engines right in your browser.

## What you need to run or use Crispy Hippopotamus:
* Pull the repository to your local machine.
* Install virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/install.html
* setup a new virtual environment where you want to run crispy hippopotamus on your local machine.
* on commade line, run:
```
pip install -r requirements.txt
```
* on command line, run:
```
python manage.py runserver
```
* Make sure you have postgres setup on your local machine: http://www.postgresql.org/
* on command line, to setup your database, run:
```
python manage.py db upgrade
```
* enjoy playing some beautiful chess.
