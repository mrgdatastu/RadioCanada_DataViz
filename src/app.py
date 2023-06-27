import dash
import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

import polar
import bar_chart
import sunburst

app = Dash(__name__)
server = app.server
app.title = 'Radio Canada Data Visualization Project | INF8808'

dataframe = pd.read_csv('f:/RC1000-1.csv')

polar_fig = polar.generate_polar(dataframe)
bar_fig = bar_chart.generate_bar_chart(dataframe)
sunburst_fig = sunburst.generate_sunburst(dataframe)

app.layout = html.Div(
    children=[
        html.H1("Radio Canada Data Visualization"),
        html.H2("Polar Chart"),
        dcc.Graph(
            id='polar-chart',
            figure=polar_fig
        ),
        html.H2("BarChart"),
        dcc.Graph(
            id='bar-chart',
            figure=bar_fig
        ),
        html.H2("SunburstChart"),
        dcc.Graph(
            id='sunburst-chart',
            figure=sunburst_fig
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
