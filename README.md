# Lecturer Assistant - local setup

# Prepare virlual env

pipenv shell


# Install packages
pipenv install -r requirements.txt


# Flask settings

export FLASK_APP=app

export FLASK_DEBUG=1


# Database settings

flask shell

from app import db

import models

db.create_all()

exit()


# Launching
pipenv run python exe.py

