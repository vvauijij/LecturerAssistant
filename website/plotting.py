import plotly.express as px
import plotly.subplots as sp
import plotly
import pandas as pd
import numpy as np
import json
from app import db
from ast import literal_eval
from models import PollSample


def render_plot(polls_results_db):
    figures = []
    titles = []

    for poll_res in polls_results_db:

        answers = json.loads(poll_res.answers)
        # print(answers)

        df = pd.DataFrame(answers, index=["key"])
        df = pd.DataFrame(np.vstack([df.columns, df])).T
        # df.rename_columns = {0: "answer", 1: "count"}
        # print(df)

        sample = PollSample.query.filter_by(id=poll_res.poll_sample_id).first()
        titles.append(sample.question)
        # if sample.poll_type == "quiz":
        #     correct = sample.correct_answer
        #     answer_variants = json.loads(sample.answer_variants)
        #     print(df)
        #     df['correct'] = df['answer'].apply(lambda x: x == answer_variants[correct])
        #     df.set_index('answer', inplace=True)
        #     print(df)
        #
        #     fig = px.bar(df, y='count', color='correct')
        # else:
        #     df.set_index('answer', inplace=True)
        #     fig = px.bar(df, y='count')
        fig = px.bar(df, x=0, y=1)
        fig.update_layout(xaxis_title="Options", yaxis_title="Votes Amount")
        figures.append(fig)
    if len(figures) == 0:
        return None
    plot = sp.make_subplots(rows=len(figures)//3 + (len(figures) % 3 != 0), cols=3, subplot_titles=titles)

    for i, figure in enumerate(figures):
        for trace in range(len(figure["data"])):
            plot.add_trace(figure["data"][trace], row=i//3 + 1, col=i % 3 + 1)
    plot.update_layout(height=400 * (len(figures)//3 + (len(figures) % 3 != 0)), showlegend=False)

    graphJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON





