import os
from app import create_app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()
