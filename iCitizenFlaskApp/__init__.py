from flask import Flask, render_template, url_for, session
from iCitizenFlaskApp.celery_worker import make_celery
import datetime

app = Flask(__name__)
app.secret_key = 'secret123'

@app.before_request
def before_request():
	session.permanent = True
	app.permanent_session_lifetime = datetime.timedelta(minutes=20)
	session.modified = True


@app.route('/', methods=['GET'])
def index():
	return render_template('home.html')

celery_worker_bills = make_celery(app)
celery_worker_events = make_celery(app)
celery_worker_polls = make_celery(app)

from iCitizenFlaskApp.views import user_routes, user_functions, user_data, get_saved_data

app.register_blueprint(user_routes.mod)
app.register_blueprint(user_functions.mod)
app.register_blueprint(user_data.mod)
app.register_blueprint(get_saved_data.mod)