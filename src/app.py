import dash
import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

import polar

app = Dash(__name__)
server = app.server
app.title = 'Radio Canada Data Visualization Project | INF8808'

dataframe = pd.read_csv('./RC1000-1.csv')

polar_fig = polar.generate_polar(dataframe)

app.layout = html.Div(
    children=[
        html.H1("Radio Canada Data Visualization"),
        dcc.Graph(
            id='polar-chart',
            figure=polar_fig
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
