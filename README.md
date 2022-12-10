# lector_assistant

# Prepare
создать + активировать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt


# Flask settings
настройка фласка:
export FLASK_APP=app
export FLASK_DEBUG=1


# Database settings
создать бд:
в командной строке из папки website
flask shell
from app import db
import models
db.create_all()
exit()


# Launching
запустить:
python exe.py



# Have no idea whats this 
бд и миграции
flask db init
flask db migrate -m "message"
