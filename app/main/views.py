from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from . import main
from .. import db
from ..models import User
from ..email import send_email
from .forms import NameForm

@main.route('/', methods=['POST', 'GET'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		user = User.query.filter_by(username=form.name.data).first()
		if old_name is not None and old_name != form.name.data:
			flash('Lookz likez youz changd ur namez!')
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
			if current_app.config['FLASKY_ADMIN']:
				send_email(current_app.config['FLASKY_ADMIN'], 'New User',
							'mail/new_user', user=user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		db.session.commit()
		return redirect(url_for('.index'))
	return render_template('index.html',
							current_time=datetime.utcnow(),
							form=form, 
							name=session.get('name'),
							known=session.get('known', False)) #session.get() returns a value of none in name is not a key in the session dict