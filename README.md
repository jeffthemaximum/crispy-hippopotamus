Crispy Hippopotamus
======

## Who is responsible for this disaster: 
Jeff Maxim

## Readme last edited: 
March 8, 2016

## Project Overview
Crispy Hippo is now hosted on AWS for anyone to use! It's here: http://ec2-52-20-212-59.compute-1.amazonaws.com/

This is my attempt to create a browser based graphical user interface for xboard compatible chess chess engines, such as gnuchess. Basically, it's a browser-based version of xboard. It lets you play against some of the best winboard/UCI chess engines right in your browser.

Ever since September, 2015, Crispy Hippo gives users the option of choosing to play against one of many possible AI's, such as GNUchess, Crafty, and Simontacchi. Because it's fairly complicated to download, compile, and run these AI's on everyone's local machine, it may be difficult for you to clone my repo and use it yourself. Getting an open-source AI written in the 70's to run on everyone's machine is hard, so I can't guarentee crispy hippo will run in your environment. If you still want to try, you can follow my directions below:

## What's most interesting:
1. Written with Python, Flask, JavaScript, Postgres, HTML, CSS, jQuery, AJAX and hosted on Amazon AWS EC2.
2. Users have the choice of playing against several different open-source Chess AI engines.
3. Websockets show users real-time thinking output from the AI.
4. Other users can view a game in progress and chat with the game-player via jQuery and AJAX.
5. JavaScript provides board GUI, checks user moves for legality, and tracks game state.

## How to use the production site:
1. Go to http://ec2-52-20-212-59.compute-1.amazonaws.com/
2. Register and login.
3. Click "Start playing chess!" button.
4. Choose an AI.
5. Play chess, but you'll likely lose :)


## Directions to run Crispy Hippopotamus locally:
* Pull the repository to your local machine.
* Install virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/install.html
* Install GNU Chess on your local machine: http://www.gnu.org/software/chess/
* Install Craft on your local machine: http://www.craftychess.com/
* Install Simontacchi on your local machine: http://simontacchi.sourceforge.net/
* setup a new virtual environment where you want to run crispy hippopotamus on your local machine.
* on commade line, run:
```
pip install -r requirements.txt
```
* Make sure you have postgres setup on your local machine: http://www.postgresql.org/
* on command line, to setup your database, run:
```
python manage.py db upgrade
```
* Startup the localhost server by running on command line:
```
python manage.py db runserver
```
* Point your browser to localhost:5000
* enjoy playing some beautiful chess.

## Current limitations / Known bugs:
* Most move handling is handled via AJAX. I'd like to clean this up and use socketio for this.
* Production site gets buggy, and AI's sometimes crash.
