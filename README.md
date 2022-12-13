# Lecturer Assistant

Утилита (сайт и телеграм бот) для продуктивного взаимодействия преподавателя с аудиторией во время занятия. 

Итоговый проект для курса "Углубленный Python" ПМИ ФКН НИУ ВШЭ, 2022. [Пеньков Алексей](https://github.com/vvauijij), [Сечкарь Константин](https://github.com/kssechkar), [Оникова Даша](https://github.com/myramystin). 

[Презентация](https://github.com/vvauijij/LecturerAssistant/blob/develop/Lecturer%20Assistant.pdf)

[Шаблоны опросов](https://github.com/vvauijij/LecturerAssistant/tree/develop/csv_templates)

## Global setup
## Local setup

### Prepare virlual env

```
pipenv shell 
```

### Install packages

```
pipenv install -r requirements.txt 
```


### Flask settings

``` 
export FLASK_APP=app

export FLASK_DEBUG=1
```

### Database settings

```
flask shell

from app import db

import models

db.create_all()

exit()
```

### Launching

```
pipenv run python exe.py
```
