from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
	name = StringField('Whats yur namez?', validators=[Required()])
	submit = SubmitField('Submit')