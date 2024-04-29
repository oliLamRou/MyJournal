import os
import pandas as pd
import numpy as np
import dash
from dash import Dash, dash_table, html, dcc, Input, Output, callback, ctx
import dash_bootstrap_components as dbc
from app_style import SIDEBAR_STYLE, CONTENT_STYLE

import data
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


CATEGORIES = ['run', 'yoga', 'crying']

def form():
    dcc.Markdown('## something')

path = f'../data/myLog.csv'
df = pd.read_csv(path).set_index('date')

def card_body(date):
    #Get Note
    note = df.loc[date, 'note']
    #NOTE: should be a better way right ?
    if str(note) == 'nan':
        note = '---'

    #Add first elem in markdown list
    body = [dcc.Markdown(f'### {note}')]


    metrics = []
    for col in df.columns:
        if col == 'note':
            continue

        metric = df.loc[date, col]
        body.append(dcc.Markdown(f'- {metric}'))

    #Add metadata at the end
    metadata = 'metadata'
    body.append(dcc.Markdown(f'###### *{metadata}*'))

    return dbc.CardBody(
        body
    )

def card(date):
    return dbc.Card(
        [
            dbc.CardHeader(date),
            card_body(date)
        ]
    )

def cards():
    _cards = [dcc.Markdown('## Hello')]
    for date in df.index:
        _cards.append(card(date))

    return _cards

def get_dropdownmenu():
    dropdownmenu = [dbc.DropdownMenuItem(category.capitalize(), id=category) for category in CATEGORIES]
    dropdownmenu.append(dbc.DropdownMenuItem(divider=True))
    dropdownmenu.append(dbc.DropdownMenuItem('New Categeory', id='new categeory'))
    return dropdownmenu

def get_inputs():
    inputs = [Input(category, 'n_clicks') for category in CATEGORIES]
    inputs.append(Input('new categeory', 'n_clicks'))
    return inputs

def form():
    input_group = html.Div(
    [
        #Title
        dbc.InputGroup(
            [dbc.Input(placeholder="Title")],
            className="mb-3",
        ),
        #Notes
        dbc.InputGroup(
            [dbc.Textarea(placeholder="Note")],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.DropdownMenu(
                    get_dropdownmenu(),
                    label="Generate", id='dropdownmenu-label'
                ),
                dbc.Input(placeholder="new categeory", id='new-category'),
                dbc.Input(placeholder="Value", id='value-disable')
            ]
        ),
        dbc.InputGroup(
            [
                dbc.Button("+", color="success", className="me-1"),
            ]
        ),
        dbc.InputGroup(
            [
                dbc.Button("Enter", color="primary", className="me-1"),
                dbc.Button("Cancel", color="secondary", className="me-1"),
            ]
        )
    ])
    return [input_group]

@app.callback(
    [
        Output('new-category', 'style'),
        Output('dropdownmenu-label', 'label'),
        Output('value-disable', 'disabled'),
    ],
    get_inputs())
def category_button(*args,**kwargs):
    if not ctx.triggered:
        return {'display': 'none'}, 'Categeory', True
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == 'new categeory':
        return {'display': 'block'}, button_id.capitalize(), False
    else:
        return {'display': 'none'}, button_id.capitalize(), False

if __name__ == '__main__':
    app.layout = html.Div([
        dbc.Container(form(), style=SIDEBAR_STYLE),
        dbc.Container(cards(), style=CONTENT_STYLE)
    ])
    app.run(debug=True)