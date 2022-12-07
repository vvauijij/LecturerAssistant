import pandas as pd
from models import PollSample, ThemeSample
import json
from poll_template import Poll


def CreatePolls(file, cur_id):
    polls = []
    data = pd.read_json(file)
    for line in data.values:
        question = line[0]
        options = json.dumps(line[1].split("|"), ensure_ascii=False).encode('utf-8')
        poll_type = line[2]
        correct = 0
        explanation = ""
        if poll_type == "quiz":
            correct = int(line[3])
            explanation = line[4]
        polls.append(PollSample(question=question, poll_type=poll_type, correct_answer=correct, hint=explanation,
                                answer_variants=options, lecture_sample_id=cur_id))
    return polls


def CreateThemes(file, cur_id):
    themes_list = []
    data = pd.read_json(file)
    for line in data.values:
        themes_list.append(line[0])
    themes_list = json.dumps(themes_list, ensure_ascii=False).encode('utf-8')  # чтобы брать нужен .decode()
    return ThemeSample(themes=themes_list, lecture_sample_id=cur_id)


def dbPollsToTg(polls):
    polls_lec = []
    poll_samples_ids = []
    for poll in polls:
        poll_samples_ids.append(poll.id)
        question = poll.question
        poll_type = poll.poll_type
        correct_answer = poll.correct_answer
        explanation = poll.hint
        options = poll.answer_variants.decode()
        polls_lec.append(Poll(question=question, options=options, poll_type=poll_type, correct_option_id=correct_answer,
                              explanation=explanation))
    return polls_lec, poll_samples_ids
