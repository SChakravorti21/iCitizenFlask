from flask import Flask, render_template, url_for, session

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('home.html')

from iCitizenFlaskApp.views import user_routes

app.register_blueprint(user_routes.mod)