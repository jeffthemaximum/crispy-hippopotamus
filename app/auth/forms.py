from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email_validators = [Required(), Length(1, 64), Email()]
    email = StringField('Email', validators=email_validators)
    password = PasswordField('Password', validators=[Required()])
    # boolean field represents a checkbox
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email_validators = [Required(), Length(1, 64), Email()]
    password_validators = [
        Required(),
        EqualTo('password2', message="Passwords much match.")]
    email = StringField('Email', validators=email_validators)
    username = StringField(
        'Username', validators=[
            Required(), Length(1, 64),
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$', 0,
                'Usernames must have only letters, '
                'numbers, dots or underscores')])
    password = PasswordField('Password', validators=password_validators)
    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")
