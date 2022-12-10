# Lecturer Assistant - setup

# Prepare venv

python3 -m venv venv

source venv/bin/activate

# Install packages
pip install -r requirements.txt


# Flask settings
настройка фласка:

export FLASK_APP=app

export FLASK_DEBUG=1


# Database settings (from terminal)

flask shell

from app import db

import models

db.create_all()

exit()


# Launching
python exe.py



# Have no idea whats this 
бд и миграции

flask db init

flask db migrate -m "message"
