from flask import (
    Blueprint, render_template
)

from .db import get_db

bp = Blueprint('application', __name__)

@bp.route("/")
def index():
    return render_template('index.html')

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if valid_login(request.form['username'], request.form['password']):
#         print(request.form['username'])
#     return  redirect(url_for('dashboard'))
#
# @app.route("/dashboard")
# def dashboard():
#     return render_template('dashboard.html')
#
#
# def valid_login(login, password):
#     session['login'] = login
#     return True
#
#
#
#
# if __name__ == "__main__":
#     print(__name__)
#     app.run(debug=True)
#
