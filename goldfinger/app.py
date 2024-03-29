# -*- coding: utf-8 -*-
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import flask
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pandas_helpers
from dash.dependencies import Input, Output


_colorway = ['#D4AF37', '#C0C0C0', '#375CB1', '#FF7400', '#FFF400', '#FF0056', "#5E0DAC", '#FF4F00']
colourmap = {
    'GoldUSD': '#D4AF37',
    'SilverUSD': '#C0C0C0'
}


# initialize app
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)


@app.callback(Input('interval-component', 'n_intervals'))
def make_data_frame():
    gold_usd = pandas_helpers.get_mangled_dataframe('XAU-USD')
    silver_usd = pandas_helpers.get_mangled_dataframe('XAG-USD')
    gold_zar = pandas_helpers.get_mangled_dataframe('XAU-ZAR')
    silver_zar = pandas_helpers.get_mangled_dataframe('XAG-ZAR')
    return pandas_helpers.concatenate_dataframes([gold_usd, silver_usd, gold_zar, silver_zar])


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})
    return dict_list


@app.callback(Output('timeseries', 'figure'), [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []
    df_sub = df

    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['Stock-Currency'] == stock].index,
                                y=df_sub[df_sub['Stock-Currency'] == stock]['DateValue'],
                                mode='lines',
                                opacity=0.7,
                                name=stock,
                                textposition='bottom center')
                    )

    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  #colorway=colorway.insert(0, colourmap[data[0]['name']]),
                  colorway=_colorway,
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={
                      'text': 'Stock Prices',
                      'font': {'color': 'white'},
                      'x': 0.5
                  },
                  xaxis={
                      'range': [df_sub.index.min(), df_sub.index.max()],
                      'type': 'date'
                  },
                ),
              }

    return figure


@app.callback(Output('change', 'figure'), [Input('stockselector', 'value')])
def update_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    trace = []
    df_sub = df
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['Stock-Currency'] == stock].index,
                                y=df_sub[df_sub['Stock-Currency'] == stock]['Change'],
                                mode='lines',
                                opacity=0.7,
                                name=stock,
                                textposition='bottom center'))
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=_colorway,
                  #colorway=_colorway.insert(0, colourmap[data[0]['name']]),
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=250,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Daily Change', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
                ),
              }

    return figure


df = make_data_frame()




# define app
app.layout = html.Div(

    dcc.Interval(
        id='interval-component',
        interval=15000,
        n_intervals=0
    )


    children = [
        html.Div(
            className = 'row',
            children = [
                # Define the left element
                html.Div(
                    className = 'three columns div-user-controls',
                    children = [
                        html.H2('STOCKS'),
                        html.P('Pick a stock'),
                        html.Div(className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='stockselector',
                                             options=get_options(df['Stock-Currency'].unique()),
                                             multi=True,
                                             value=[df['Stock-Currency'].sort_values()[0]],
                                             style={'backgroundColor': '#1E1E1E'},
                                             className='stockselector')
                            ],
                            style={'color': '1E1E1E'}
                        )
                    ]
                ),
                # Define the right element
                html.Div(
                    className = 'nine columns div-for-charts bg-grey',
                    children = [
                        html.Div(
                            dcc.Graph(id = 'timeseries', config = {'displayModeBar': False}, animate=True),
                        ),
                        html.Div(
                            dcc.Graph(id = 'change', config = {'displayModeBar': False})
                        )
                    ]
                )
            ]
        )
    ]
)


# run app
if __name__ == '__main__':

    import os

    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
    app.run_server(host='0.0.0.0', port=8050, debug=debug)
