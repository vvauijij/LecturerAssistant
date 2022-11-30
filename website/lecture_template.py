import datetime
import json


class PollResult:
    __slots__ = ['question',
                 'votes',  # dict: option - voter_count
                 'poll_type',
                 'correct_option_id']

    def __init__(self,
                 question='question?',
                 votes=None,
                 poll_type='regular',
                 correct_option_id=0):
        # create poll results
        self.question = question

        if self.votes is None:
            self.votes = dict()

        self.votes = votes
        self.poll_type = poll_type
        self.correct_option_id = correct_option_id


class Poll:
    __slots__ = ['question',
                 'options',
                 'poll_type',
                 'correct_option_id',
                 'explanation',
                 'is_closed',
                 'is_anonymous']

    def __init__(self,
                 question='question?',
                 options=None,
                 poll_type='regular',
                 correct_option_id=0,
                 explanation='explanation',
                 is_closed=False,
                 is_anonymous=False):
        # create poll
        self.question = question
        self.options = options
        if options is None:
            self.options = []
        elif type(options) == str:
            self.options = json.loads(options)

        self.poll_type = poll_type
        self.correct_option_id = correct_option_id
        self.explanation = explanation
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous

    def __dict__(self):
        return {
            'question': self.question,
            'options': self.options,
            'poll_type': self.poll_type,
            'correct_option_id': self.correct_option_id,
            'explanation': self.explanation,
            'is_closed': self.is_closed,
            'is_anonymous': self.is_anonymous
        }


class LectureResults:
    __slots__ = ['title',
                 'id',
                 'timecodes',  # dict: theme - timecode
                 'polls_results']  # list: poll_result

    def __init__(self, title='title', lecture_id=None, timecodes=None, polls_results=None):
        self.title = title
        self.id = lecture_id

        if timecodes is None:
            self.timecodes = dict()
        if polls_results is None:
            self.polls_results = list()


class Lecture:
    __slots__ = ['title',
                 'themes',
                 'polls',
                 'poll_ids',
                 'id',
                 'polls_results',  # list: poll_result
                 'timecodes',  # dict: theme - timecode
                 'current_theme']

    def __init__(self, title='title', themes=None, polls=None, poll_ids=None):
        # create lecture

        self.title = title
        self.themes = themes
        self.polls = polls
        self.poll_ids = poll_ids
        if themes is None:
            self.themes = list()
        if polls is None:
            self.polls = dict()
            self.poll_ids = list()
        self.timecodes = None
        self.id = None
        self.polls_results = None
        self.current_theme = None

    def start_lecture(self, lec_id):
        self.id = lec_id
        self.timecodes = dict()
        self.polls_results = list()
        self.timecodes['Start'] = datetime.datetime.now()

    def end_lecture(self) -> LectureResults:
        return LectureResults(title=self.title,
                              timecodes=self.timecodes,
                              polls_results=self.polls_results)  # todo: check if mutable

    def __dict__(self):
        return {
            'title': self.title,
            'themes': self.themes,
            'polls': [poll.__dict__() for poll in self.polls],
            'id': self.id,
            'polls_results': self.polls_results,
            'timecodes': self.timecodes,
            'current_theme': self.current_theme,
            'poll_ids': self.poll_ids
        }


def lecture_from_dict(lecture_dict) -> Lecture:
    lecture = Lecture(title=lecture_dict['title'],
                      themes=lecture_dict['themes'],
                      polls=[Poll(**poll) for poll in lecture_dict['polls']])
    lecture.id = lecture_dict['id']
    lecture.polls_results = lecture_dict['polls_results']
    lecture.timecodes = lecture_dict['timecodes']
    lecture.current_theme = lecture_dict['current_theme']
    lecture.poll_ids = lecture_dict['poll_ids']
    return lecture
