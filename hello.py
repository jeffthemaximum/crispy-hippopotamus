from datetime import datetime
#from flask import Flask, render_template, session, redirect, url_for, flash
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask.ext.script import Manager
#from flask.ext.bootstrap import Bootstrap
#from flask.ext.moment import Moment
from flask.ext.wtf import Form
#from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Shell
#from flask.ext.mail import Mail, Message

import pudb
import os

app = Flask(__name__)
#should be stored in config.py file
app.config['SECRET_KEY'] = 't@afvhq+$l^f*u*$a!!uo$d6g@v)h(u2uh$^jid(#i7n*zavp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jeff:airjeff@localhost/flasky'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <frey.maxim@gmail.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
	#manager.run() #doesn't use debug mode or auto restart
    app.run(debug=True)