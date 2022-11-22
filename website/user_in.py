from flask import Blueprint, Flask, redirect, url_for, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import pandas as pd

user_in = Blueprint('user_in', __name__, url_prefix="/user")

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

# my_funcs:

@user_in.route("/")
def home():
    return render_template("home.html")


@user_in.route("/create_lecture/name", methods=["POST", "GET"])
def create_lecture_name():
    if request.method == "POST":
        session["lec_name"] = request.form["lec_name"]
        return redirect(url_for("user_in.create_lecture_tasks"))
    else:
        return render_template("create_lecture_name.html")


@user_in.route("/create_lecture/tasks", methods=["POST", "GET"])
def create_lecture_tasks():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        session["tasks"] = pd.read_csv(file).to_json()
        return redirect(url_for("main.index"))
    return render_template('create_lecture_tasks.html', form=form)


# end funcs