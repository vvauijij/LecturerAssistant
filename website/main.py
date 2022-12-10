from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")
    return redirect(url_for("auth.login"))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',  name=current_user.name)