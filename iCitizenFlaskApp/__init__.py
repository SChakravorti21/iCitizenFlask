from flask import Flask, render_template, url_for, session
import datetime

app = Flask(__name__)

@app.before_request
def before_request():
	session.permanent = True
	app.permanent_session_lifetime = datetime.timedelta(minutes=20)
	session.modified = True


@app.route('/', methods=['GET'])
def index():
	return render_template('home.html')

from iCitizenFlaskApp.views import user_routes, user_functions

app.register_blueprint(user_routes.mod)
app.register_blueprint(user_functions.mod)