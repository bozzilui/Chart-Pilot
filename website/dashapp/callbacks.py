from datetime import datetime as dt
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from flask_login import current_user
import pandas_datareader as pdr


def register_callbacks(dashapp):
    @dashapp.callback(
    Output('search-output', 'children'),
    [Input('search-button', 'n_clicks')],
    [State('search-input', 'value')])
    def update_output(n_clicks, search_term):
        if n_clicks is not None:
            return f'Search term entered: {search_term}'

    @dashapp.callback(
        Output('search-term', 'children'),
        [Input('search-button', 'n_clicks')],
        [State('search-input', 'value')])
    def update_search_term(n_clicks, search_term):
        if n_clicks is not None:
            return search_term