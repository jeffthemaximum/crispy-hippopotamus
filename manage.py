from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from hello import app, db
app.config['SECRET_KEY'] = 't@afvhq+$l^f*u*$a!!uo$d6g@v)h(u2uh$^jid(#i7n*zavp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jeff:airjeff@localhost/flasky'

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()