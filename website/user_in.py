from flask import Blueprint, Flask, redirect, url_for, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import pandas as pd
from models import LectureSample, PollSample, ThemeSample, LectureResult, PollResult
from LecParser import CreatePolls, CreateThemes, dbPollsToTg
from app import db
from flask_login import login_required, current_user
import json
import os
import base64

from lecture_template import Lecture, Poll, lecture_from_dict

from plotting import render_plot, convert_to_binary_data

import bot_main

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
    polls_db = PollSample.query.filter_by(lecture_sample_id=lec_id)
    polls_lec, polls_ids = dbPollsToTg(polls_db)
    session["lec_sample_id"] = lec_id
    if request.method == "POST":
        # тут создается инстанс lecture_result, пишем его в lec_result_id
        new_lec_res = LectureResult(lecture_sample_id=lec_id, user_id=current_user.id)
        db.session.add(new_lec_res)
        db.session.commit()

        session["lec_result_id"] = new_lec_res.id
        session["room_code"] = str(session["lec_result_id"])

        bot_main.lector_assistant_bot.create_room(session["room_code"])

        lec_db = LectureSample.query.filter_by(id=lec_id).first()
        lec = Lecture(title=lec_db.name, polls=polls_lec, poll_ids=polls_ids)
        lec.start_lecture(new_lec_res.id)
        session["lec"] = lec.__dict__()
    lec = lecture_from_dict(session["lec"])
    polls_available = lec.polls_available
    polls = [(i, polls_lec[i].question, polls_available[i]) for i in range(len(polls_lec))]
    return render_template("running_lecture.html", polls=polls, code=session["room_code"],
                           polls_available=lec.polls_available)


# end funcs

@user_in.route("/sendpoll/<id>", methods=["POST", "GET"])
@login_required
def send_poll(id):
    if request.method == "POST":
        lec = lecture_from_dict(session["lec"])
        poll_sample = lec.polls[int(id)]
        lec.sent_polls_ids.append(int(id))
        lec.polls_available[int(id)] = False
        session["lec"] = lec.__dict__()
        bot_main.lector_assistant_bot.send_poll(session["room_code"], len(lec.sent_polls_ids)-1, poll_sample)
    return redirect(url_for("user_in.run_lecture", lec_id=session["lec_sample_id"]))


@user_in.route("/endpoll/<id>", methods=["POST", "GET"])
@login_required
def close_poll(id):
    if request.method == "POST":
        lec = lecture_from_dict(session["lec"])
        bot_id = len(lec.sent_polls_ids) - 1 - lec.sent_polls_ids[::-1].index(int(id))
        poll_sample = lec.polls[int(id)]

        poll_data = bot_main.lector_assistant_bot.get_poll_result(session["room_code"], bot_id)

        link = render_plot(poll_data, poll_sample, id)
        bin_data = convert_to_binary_data(link)
        new_poll_res = PollResult(lecture_result_id=session["lec_result_id"],
                                  poll_sample_id=int(lec.poll_ids[int(id)]),
                                  answers=json.dumps(poll_data),
                                  plot=bin_data)
        db.session.add(new_poll_res)
        db.session.commit()
        os.remove(link)

        lec.polls_available[int(id)] = True
        session["lec"] = lec.__dict__()

    return redirect(url_for("user_in.run_lecture", lec_id=session["lec_sample_id"]))


@user_in.route("/my_lectures_results")
@login_required
def my_lectures_results():
    user_lecs = LectureResult.query.filter_by(user_id=current_user.id)
    user_lecs_with_names = [(lec.lecture_sample.name, lec.id) for lec in user_lecs]
    # TODO добавить время (чтобы как-то отличать лекции одного сэмпла)
    return render_template('my_lectures_results.html', lecs=user_lecs_with_names)


@user_in.route("/show/<lec_id>", methods=["GET", "POST"])
@login_required
def show_lecture(lec_id):
    polls_results_db = PollResult.query.filter_by(lecture_result_id=lec_id)
    images = []
    for poll in polls_results_db:
        images.append(base64.b64encode(poll.plot).decode('utf-8'))
    return render_template('show_lecture_result.html', images=images)
