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

df_xau_usd = metals_api.redis_to_dataframe('XAU-USD')
df_xag_usd = metals_api.redis_to_dataframe('XAG-USD')

# convert usd pricing
df_xau_usd['DateValue'] = df_xau_usd.DateValue.apply(lambda x: 1/x)
df_xag_usd['DateValue'] = df_xag_usd.DateValue.apply(lambda x: 1/x)

df_xau_usd.insert(1, 'Stock', 'Gold', allow_duplicates=True)
df_xau_usd.insert(2, 'Currency', 'USD', allow_duplicates=True)

df_xag_usd.insert(1, 'Stock', 'Silver', allow_duplicates=True)
df_xag_usd.insert(2, 'Currency', 'USD', allow_duplicates=True)


df = pd.concat([df_xau_usd, df_xag_usd], ignore_index=True)

fig_xau_usd = go.Figure(data=[go.Scatter(x=df_xau_usd['Date'], y=df_xau_usd['DateValue'])])
fig_xag_usd = go.Figure(data=[go.Scatter(x=df_xag_usd['Date'], y=df_xag_usd['DateValue'])])

# initialize app
app = dash.Dash(__name__)


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})
    return dict_list


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
                            dcc.Graph(
                                id = 'timeseries',
                                config = {
                                    'displayModeBar': False
                                },
                                animate = True,
                                figure = px.line(
                                    df,
                                    x = 'Date',
                                    y = 'DateValue',
                                    color = 'Stock',
                                    template = 'plotly_dark'
                                ).update_layout(
                                    {
                                      'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                      'paper_bgcolor': 'rgba(0, 0, 0, 0)'
                                    }
                                )
                            )
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
