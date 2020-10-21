# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import metals_api

from dash.dependencies import Input, Output

df_xau_usd = metals_api.redis_to_dataframe('XAU-USD')
df_xag_usd = metals_api.redis_to_dataframe('XAG-USD')

# convert usd pricing
df_xau_usd['DateValue'] = df_xau_usd.DateValue.apply(lambda x: 1/x)
df_xag_usd['DateValue'] = df_xag_usd.DateValue.apply(lambda x: 1/x)

df_xau_usd.insert(1, 'Stock', 'Gold', allow_duplicates=True)
df_xau_usd.insert(2, 'Currency', 'USD', allow_duplicates=True)

df_xag_usd.insert(1, 'Stock', 'Silver', allow_duplicates=True)
df_xag_usd.insert(2, 'Currency', 'USD', allow_duplicates=True)


# Add daily change column. As easy as.
df_xau_usd['Change'] = df_xau_usd['DateValue'].diff()

# Add daily change column. As easy as.
df_xag_usd['Change'] = df_xag_usd['DateValue'].diff()


df = pd.concat([df_xau_usd, df_xag_usd], ignore_index=True)
# Make Date column a datetime series
df['Date'] = pd.to_datetime(df['Date'])

df.set_index('Date', inplace=True)

# initialize app
app = dash.Dash(__name__)


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})
    return dict_list


@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['Stock'] == stock].index,
                                y=df_sub[df_sub['Stock'] == stock]['DateValue'],
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
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={
                      'range': [df_sub.index.min(), df_sub.index.max()],
                      'type': 'date'
                  },
                ),
              }

    return figure



@app.callback(Output('change', 'figure'),
              [Input('stockselector', 'value')])
def update_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    trace = []
    df_sub = df
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['Stock'] == stock].index,
                                y=df_sub[df_sub['Stock'] == stock]['Change'],
                                mode='lines',
                                opacity=0.7,
                                name=stock,
                                textposition='bottom center'))
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
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




# define app
app.layout = html.Div(
    children = [
        html.Div(
            className = 'row',
            children = [
                # Define the left element
                html.Div(
                    className = 'four columns div-user-controls',
                    children = [
                        html.H2('STOCKS'),
                        html.P('Pick a stock'),
                        html.Div(className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='stockselector',
                                             options=get_options(df['Stock'].unique()),
                                             multi=True,
                                             value=[df['Stock'].sort_values()[0]],
                                             style={'backgroundColor': '#1E1E1E'},
                                             className='stockselector')
                            ],
                            style={'color': '1E1E1E'}
                        )
                    ]
                ),
                # Define the right element
                html.Div(
                    className = 'eight columns div-for-charts bg-grey',
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
    app.run_server(debug = True)
