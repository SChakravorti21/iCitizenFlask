from wtforms import Form, StringField, PasswordField, validators

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	email = StringField('Email', [
		validators.Length(min=6, max=50),
		validators.Email()
	])
	username = StringField('Username', [
		validators.DataRequired(),
		validators.Length(min=6, max=25)
	])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.Length(min=6, max=25)
	])
	confirm = PasswordField('Confirm Password', 
		[validators.EqualTo('password', message='Passwords do not match!')])