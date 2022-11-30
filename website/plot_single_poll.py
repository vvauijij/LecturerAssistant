import plotly.express as px
import pandas as pd
import numpy as np
from lecture_template import Poll


def render_plot(answers: dict, poll: Poll):
    default_color = "blue"
    df = pd.DataFrame(answers, index=["key"])
    df = pd.DataFrame(np.vstack([df.columns, df])).T
    if poll.poll_type == 'quiz':
        colors_map = {poll.options[poll.correct_option_id]: "red"}
        print(answers)
        print(poll.options, poll.correct_option_id, type(poll.options))
        for opt in answers.keys():
            if opt not in colors_map.keys():
                colors_map[opt] = default_color
            print(colors_map)
        fig = px.bar(df, x=0, y=1, color=0, color_discrete_map=colors_map)
    else:
        fig = px.bar(df, x=0, y=1)
    fig.update_layout(
        title=poll.question,
        xaxis_title="Options",
        yaxis_title="Votes Amount")
    fig.show()




