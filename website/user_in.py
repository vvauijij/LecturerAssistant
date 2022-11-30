from flask import Blueprint, Flask, redirect, url_for, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import pandas as pd
from models import LectureSample, PollSample, ThemeSample, LectureResult, PollResult
from LecParser import CreatePolls, CreateThemes, dbPollsToTg
from app import db
from flask_login import login_required, current_user

from lecture_template import Lecture, Poll, lecture_from_dict

from plot_single_poll import render_plot

user_in = Blueprint('user_in', __name__, url_prefix="/user")


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")


# my_funcs:


@user_in.route("/")
@login_required
def home():
    return render_template("home.html")


@user_in.route("/create_lecture/name", methods=["POST", "GET"])
@login_required
def create_lecture_name():
    if request.method == "POST":
        session["lec_name"] = request.form["lec_name"]
        new_lec = LectureSample(name=session["lec_name"], user_id=current_user.id)
        db.session.add(new_lec)
        db.session.commit()
        session["lec_id"] = new_lec.id
        return redirect(url_for("user_in.create_lecture_themes"))
    else:
        return render_template("create_lecture_name.html")


@user_in.route("/create_lecture/themes", methods=["POST", "GET"])
@login_required
def create_lecture_themes():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        session["themes"] = pd.read_csv(file).to_json()
        themes = CreateThemes(session["themes"], session["lec_id"])
        db.session.add(themes)
        db.session.commit()
        return redirect(url_for("user_in.create_lecture_tasks"))
    return render_template('create_lecture_themes.html', form=form)


@user_in.route("/create_lecture/tasks", methods=["POST", "GET"])
@login_required
def create_lecture_tasks():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        session["tasks"] = pd.read_csv(file).to_json()
        polls = CreatePolls(session["tasks"], session["lec_id"])
        for poll in polls:
            db.session.add(poll)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template('create_lecture_tasks.html', form=form)


@user_in.route("/my_lectures")
@login_required
def my_lectures():
    user_lecs = LectureSample.query.filter_by(user_id=current_user.id)
    return render_template('my_lectures.html', lecs=user_lecs)


@user_in.route("/running/<lec_id>", methods=["POST", "GET"])
@login_required
def run_lecture(lec_id):
    # TODO отправка в бота
    # lector_assistant_bot.create_room(str(lec_id))
    # тут создается инстанс lecture_result, пишем его в lec_result_id
    new_lec_res = LectureResult(lecture_sample_id=lec_id, user_id=current_user.id)
    session["lec_result_id"] = new_lec_res.id
    db.session.add(new_lec_res)
    db.session.commit()
    polls_db = PollSample.query.filter_by(lecture_sample_id=lec_id)
    polls_lec = dbPollsToTg(polls_db)

    lec_db = LectureSample.query.filter_by(id=lec_id).first()
    lec = Lecture(title=lec_db.name, polls=polls_lec)
    lec.start_lecture(new_lec_res.id)
    session["lec"] = lec.__dict__()
    print(session["lec"])
    poll_ids_questions = [(i, poll.question) for i, poll in enumerate(polls_lec)]
    return render_template("running_lecture.html", polls=poll_ids_questions)


# end funcs

@user_in.route("/endpoll/<id>", methods=["POST", "GET"])
@login_required
def close_poll(id):
    if request.method == "POST":
        # TODO забирать данные из бота
        reg_poll_data = {"ничего": 10, "что-то": 17}
        quiz_poll_data = {"никого": 30, "кого-то": 45}

        lec = lecture_from_dict(session["lec"])
        poll_sample = lec.polls[int(id)]

        render_plot(quiz_poll_data, poll_sample)

        # TODO закрыть опрос

        return render_template("single_poll.html")
    else:
        return render_template("running_lecture.html")


def close_lecture():
    pass
