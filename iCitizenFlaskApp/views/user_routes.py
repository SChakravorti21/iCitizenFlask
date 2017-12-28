from flask import Blueprint, render_template, url_for

mod = Blueprint('general', __name__)

@mod.route('/register/', methods=['GET'])
def register():
	return render_template('register.html')
