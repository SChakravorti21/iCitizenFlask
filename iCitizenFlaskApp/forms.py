from wtforms import Form, StringField, PasswordField, SelectField, SelectMultipleField, RadioField, validators
from iCitizenFlaskApp.data import STATES, SUBJECTS

class RegisterForm(Form):
	"""This class defines the WTForm for user registration.

	Attributes:
		name (:obj:`StringField`): Allows for input of the user's actual name (although it
			is not actually used anywhere). The name must be between 1 and 50 characters
			long (inclusive).
		email (:obj:`StringField`): Allows for input of the user's email address (although it
			is not used anywhere for the time being). The email address must be between 
			6 and 50 characters (inclusive). Email address's existence is not checked
			robustly with the current implementation.
		username (:obj:`StringField`): Allows for input of the user's intended username.
			Username must be between 6 and 25 characters (inclusive). This username
			is used during login.
		password (:obj:`PasswordField`): Allows for input of the user's intended password.
			Password must be between 6 and 25 characters (inclusive).
		confirm (:obj:`PasswordField`): Allows for secodn input of the user's password.
			Checks whether this field matches the ``password`` field to ensure that
			user did not make a typo.
	"""

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
	"""This class defines WTForm for logging in.

	Attributes:
		username (:obj:`StringField`): Allows for input of the user's username.
		password (:obj:`PasswordField`): Allows for input of the user's password.
	"""
	
	username = StringField('Username', [validators.InputRequired()])
	password = PasswordField('Password', [validators.InputRequired()])

class PreferencesForm(Form):
	"""This class defines the WTForm for user to input their preferences.

	The multi-select field for entering topics of interest is not included
	in this form because the Select2 front-end library was used for a more
	user-friendly multi-select field.

	Attributes:
		political_party (:obj:`RadioField`): Allows user to enter their political
			affiliation. Options include Republican/Democrat/Independent.
		address (:obj:`StringField`): Allows user to input street address.
		city (:obj:`StringField`): Allows user to input city of address.
		state (:obj:`SelectField`): Allows user to select the state of their address.
		country (:obj:`StringField`): Allows user to input country of address.
		zipcode (:obj:`StringField`): Allows user to input zipcode of address.
	"""

	political_party = RadioField('Political Party', [validators.InputRequired()],
		choices=[('republican', 'Republican'), ('democrat', 'Democrat'), ('independent', 'Independent')])
	address = StringField('Address', [validators.InputRequired()])
	city = StringField('City', [validators.InputRequired()])
	state = SelectField('State', [validators.InputRequired()],
		choices=STATES)
	country = StringField('Country', [validators.InputRequired()])
	zipcode = StringField('Zip Code', [validators.InputRequired()])