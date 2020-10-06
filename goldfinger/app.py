# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import metals_api

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


df_xau = metals_api.redis_to_dataframe('XAU')
df_xag = metals_api.redis_to_dataframe('XAG')

fig_xau = go.Figure([go.Scatter(x=df_xau['Date'], y=df_xau['DateValue'])])
fig_xag = go.Figure([go.Scatter(x=df_xag['Date'], y=df_xag['DateValue'])])

app.layout = html.Div(children=[
    html.H1(children='Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig_xau
    ),
    dcc.Graph(
        id='example-graph2',
        figure=fig_xag
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
