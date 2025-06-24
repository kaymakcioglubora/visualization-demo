import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import datetime

app = dash.Dash(__name__)
app.title = "Plotly Dash Demo"

df = pd.DataFrame(columns=["Time", "Value"])

app.layout = html.Div(
    style={'padding': '2rem'},
    children=[
        html.H1("Plotly Demo"),
        dcc.Graph(id='live-graph', style={'height': '60vh'}),
        dcc.Interval(
            id='interval',
            interval=1000,
            n_intervals=0
        )
    ]
)


@app.callback(
    Output('live-graph', 'figure'),
    Input('interval', 'n_intervals')
)
def update_graph(n):
    global df

    new_time = pd.Timestamp.now().strftime("%H:%M:%S")
    new_value = np.random.randn() * 10 + 50
    new_row = pd.DataFrame({"Time": [new_time], "Value": [new_value]})

    df = pd.concat([df, new_row], ignore_index=True).tail(100)

    fig = px.line(df, x='Time', y='Value', title='Live Random Time-Series')
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Value',
        template='plotly_dark'
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
