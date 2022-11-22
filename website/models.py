from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

#
# import datetime
# from time import sleep
#
#
# class Task:
#     def __init__(self, text="", answers=None, right_answer=1):
#         if answers is None:
#             answers = []
#         self.text = text
#         self.answers = answers
#         self.right_answer = right_answer
#
#
# class Poll:
#     def __init__(self, variants=None, tasks=None):
#         if variants is None:
#             variants = []
#         if tasks is None:
#             tasks = []
#         self.variants = variants
#         self.tasks = tasks
#
#     def plot_smth(self):
#         pass
#
#
# class Lection:
#     def __init__(self, list_of_themes=None, test_tasks=None):
#         #self.begin_time = datetime.datetime.now()
#         if list_of_themes is None:
#             list_of_themes = []
#         if test_tasks is None:
#             test_tasks = []
#         self.list_of_themes = list_of_themes
#         self.list_of_themes = ['Начало'] + self.list_of_themes
#         self.test_tasks = test_tasks
#         #self.timecodes = [self.begin_time]
#         self.current_theme = -1
#         self.current_task = -1
#         self.current_poll = -1
#
#     def next_theme(self):
#         self.timecodes.append(datetime.datetime.now())
#         self.current_theme += 1
#         return self.list_of_themes[self.current_theme]
#
#     def next_task(self):
#         self.current_task += 1
#         return self.test_tasks[self.current_task]
#
#     def send_poll(self, poll):
#         self.current_poll = poll
#         return poll.variants
#
#     def form_timecodes(self):
#         timecodes = []
#         for i in range(len(self.timecodes)):
#             delta = self.timecodes[i] - self.begin_time
#             sec = delta.seconds
#             hours = sec // 3600
#             minutes = (sec // 60) - (hours * 60)
#             sec -= hours * 3600 + minutes * 60
#             timecodes.append(f"{hours}:{minutes}:{sec}")
#         return timecodes
#
#
# l = Lection(list_of_themes=["Тема 1", "Тема 2", "Тема 3", "Тема 4"])
# sleep(10)
# for i in range(1, len(l.list_of_themes)):
#     l.next_theme()
#     sleep(5)
# a = l.form_timecodes()
# for i in range(len(a)):
#     print(l.list_of_themes[i], a[i])
# b = 10
