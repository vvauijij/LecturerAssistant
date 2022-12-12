import plotly.graph_objects as go
import plotly.subplots as sp
import plotly
import pandas as pd
import numpy as np
import json
from models import PollSample


def render_plot(polls_results_db):
    """
    :param polls_results_db: list of PollResult objects (db query)
    :return: plotly json object
    """
    titles = []
    sz = 0
    for poll_res in polls_results_db:
        sample = PollSample.query.filter_by(id=poll_res.poll_sample_id).first()
        titles.append(sample.question)
        sz += 1
    if sz == 0:
        return None
    rows_amount = sz // 3 + (sz % 3 != 0)
    cols_amount = 3

    plot = sp.make_subplots(rows=rows_amount, cols=cols_amount, subplot_titles=titles,
                            specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}] for _ in range(rows_amount)])
    for i, poll_res in enumerate(polls_results_db):

        answers = json.loads(poll_res.answers)
        df = pd.DataFrame(answers, index=["key"])
        df = pd.DataFrame(np.vstack([df.columns, df])).T
        df = df.rename({0: 'answer', 1: 'count'}, axis=1)

        labels = list(df['answer'])
        values = list(df['count'])
        zeros = [True if values[i] == 0 else False for i in range(len(values))]
        if len(labels) - zeros.count(True) == 0 or len(values) - zeros.count(True) == 0:
            continue
        pull = [0 for _ in range(len(labels))]
        sample = PollSample.query.filter_by(id=poll_res.poll_sample_id).first()
        if sample.poll_type == "quiz":
            correct = sample.correct_answer
            answer_variants = json.loads(sample.answer_variants)
            correct_index = labels.index(answer_variants[correct])
            if not (zeros.count(False) == 1 and not zeros[correct_index]):
                pull[correct_index] = 0.1
        final_labels = [labels[i] for i in range(len(labels)) if not zeros[i]]
        final_values = [values[i] for i in range(len(values)) if not zeros[i]]
        final_pull = [pull[i] for i in range(len(pull)) if not zeros[i]]
        plot.add_trace(go.Pie(labels=final_labels, values=final_values, pull=final_pull), row=i // 3 + 1, col=i % 3 + 1)
    plot.update_layout(height=400 * rows_amount, showlegend=False)
    graphJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
