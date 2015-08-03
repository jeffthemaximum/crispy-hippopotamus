<<<<<<< HEAD
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
=======
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail, Message
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
>>>>>>> more-temp
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
<<<<<<< HEAD
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
=======

login_manager = LoginManager()
#strong keeps track of client's ip address and will log user out if it detects change
login_manager.session_protection = 'strong'
#sets the endpoint for the login page
#because login route is inside a blueprint, it needs to be prefixed with blueprint name
login_manager.login_view = 'auth.login'

def create_app(config_name):
	app = Flask(__name__)
	#the configuration settings stored in one of the classes defined in 
	#config.py can be imported directly into the application using
	#the from_object method available to Flask's app.config object
	app.config.from_object(config[config_name])
	#the configuration object is selected from the config dictionary
	config[config_name].init_app(app)

	#once the app is created and configured,
	#the extensions can be initialized.
	#calling init_app() on the extentions that were created earlier
	#completes their intialization
	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	#applications created with the factory function are incomplete
	#because they are missing routes and custom error messages
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	
	return app
>>>>>>> more-temp
