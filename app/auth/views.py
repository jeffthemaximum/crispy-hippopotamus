from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm
from .forms import RegistrationForm
from ..models import User
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # auth/login.html must be stored inside of the app/templates folder
    # flask expects templates to me relative to the application's templates f
    login_form = LoginForm()
    # if form is valid
    if login_form.validate_on_submit():
        # query db by email for user
        user = User.query.filter_by(email=login_form.email.data).first()
        # if user exists and password is valid
        if user is not None and user.verify_password(login_form.password.data):
            # login user
            # remember_me.data sets a long term cookie in user browser
            login_user(user, login_form.remember_me.data)
            # if login was presented to user to prevent unauthorized login
            # flask-login will save the original url in the 'next' string
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', login_form=login_form)


@auth.route('/logout')
@login_required
def logout():
    # removes and reset user session
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', registration_form=form)
