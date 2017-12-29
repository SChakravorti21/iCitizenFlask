from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from iCitizenFlaskApp.forms import RegisterForm

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


	return render_template('register.html', form=form)

@mod.route('/login/', methods=['GET', 'POST'])
def login():
	return render_template('login.html')
