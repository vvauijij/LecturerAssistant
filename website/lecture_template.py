import datetime
from json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

    def decode(self, o):
        # TODO
        pass


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
        if options is None:
            self.options = ['option1', 'option2']
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

    def __init__(self, title='title', themes=None, polls=None):
        # create lecture

        self.title = title
        if themes is None:
            self.themes = list()
        if polls is None:
            self.polls = dict()

        self.themes = themes
        self.polls = polls

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
            'polls': self.polls,
            'id': self.id,
            'polls_results': self.polls_results,
            'timecodes': self.timecodes,
            'current_theme': self.current_theme
        }



