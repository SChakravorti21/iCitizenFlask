from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from iCitizenFlaskApp.forms import RegisterForm, LoginForm

from iCitizenFlaskApp.dbconfig import db

mod = Blueprint('users', __name__)

@mod.route('/register/', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)

	if request.method == 'POST' and form.validate():
		# Add user to database
		name = form.name.data
		email = form.email.data
		username = form.username.data
		plain_password = str(form.password.data)

		password = sha256_crypt.encrypt(plain_password)

		users = db['users']
		insert_id = users.insert_one({
			'name': name,
			'email': email,
			'username': username,
			'password': password
		}).inserted_id

		print(str(insert_id))

		flash('You are now registered and can log in!', 'success')

		return redirect( url_for('users.login'))

	# Just render the template if it wasn't a POST request, or if the form failed to validate
	return render_template('register.html', form=form)

@mod.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)

	if request.method == 'POST' and form.validate():

		username = form.username.data
		entered_password = str(form.password.data)

		query = {'username': username}
		users = db['users']

		user = users.find_one(query)
		print(user)

		if user is None or not sha256_crypt.verify(entered_password, user['password']):
			flash('Invalid username or password', 'danger')
		else:
			session['logged_in'] = True
			session['username'] = username

			flash('You have successfully logged in!', 'success')
			return redirect( url_for('index'))

	# Just render the template if it wasn't a POST request, or if the form failed to validate
	return render_template('login.html', form=form)

@mod.route('/logout/', methods=['GET'])
def logout():
	session['logged_in'] = False
	session['username'] = None

	flash('You have successfully logged out!', 'success')
	return redirect( url_for('index'))

@mod.route('/dashboard/', methods=['GET'])
def load_dashboard():
	return render_template('dashboard.html')
