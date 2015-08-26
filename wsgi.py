import os
from app import create_app, db
from app.models import User, Role, Game
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()
