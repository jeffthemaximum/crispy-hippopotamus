import os
from app import create_app, db
from app.models import User, Role, Game
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.socketio import SocketIO
from flask import current_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Game=Game)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def run():
    socketio.run(
        current_app,
        host='127.0.0.1',
        port=5000,
        use_reloader=False)


if __name__ == '__main__':
    manager.run()
