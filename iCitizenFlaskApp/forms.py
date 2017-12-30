from wtforms import Form, StringField, PasswordField, SelectField, SelectMultipleField, RadioField, validators
from iCitizenFlaskApp.data import STATES, SUBJECTS

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	email = StringField('Email', [
		validators.Length(min=6, max=50),
		validators.Email()
	])
	username = StringField('Username', [
		validators.InputRequired(),
		validators.Length(min=6, max=25)
	])
	password = PasswordField('Password', [
		validators.InputRequired(),
		validators.Length(min=6, max=25)
	])
	confirm = PasswordField('Confirm Password', 
		[validators.EqualTo('password', message='Passwords do not match!')])

class LoginForm(Form):
	username = StringField('Username', [validators.InputRequired()])
	password = PasswordField('Password', [validators.InputRequired()])

class PreferencesForm(Form):
	political_party = RadioField('Political Party', [validators.InputRequired()],
		choices=[('republican', 'Republican'), ('democrat', 'Democrat'), ('independent', 'Independent')])
	address = StringField('Address', [validators.InputRequired()])
	city = StringField('City', [validators.InputRequired()])
	state = SelectField('State', [validators.InputRequired()],
		choices=STATES)
	country = StringField('Country', [validators.InputRequired()])
	zipcode = StringField('Zip Code', [validators.InputRequired()])