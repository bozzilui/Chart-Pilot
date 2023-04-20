import dash_core_components as dcc
from dash import dash_table
import os
import dash_bootstrap_components as dbc
import dash_html_components as html
import Plot_ichimoku
import pandas as pd
from datetime import date
import base64

def get_column_from_csv(file, col_name):
    # Try to get the file and if it doesn't exist issue a warning
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print("File Doesn't Exist")
    else:
        return df[col_name]

def dashboard(ticker):
    tickers = get_column_from_csv(f"{os.getcwd()}/Wilshire-5000-Stocks.csv", "Ticker")

    colors = {
    'background': '#111111',
    'text': '#7FDBFF'
    }

    df = Plot_ichimoku.get_stock_df_from_csv(ticker)

    fig = Plot_ichimoku.get_Ichimoku(df)

    fig.update_layout(
    title=ticker,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color='white'
    )
    """
    navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Login", href="/login", external_link=True)),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Logout", href="/logout", external_link=True),
                dbc.DropdownMenuItem("Sign up", href="/sign-up", external_link=True),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Chart Pilot",
    brand_href="/",
    brand_external_link=True,
    color="#272b34",
    dark=True,
    links_left=True
    )      
    """

    drop = dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Logout", href="/logout", external_link=True),
                
            ],
            nav=True,
            in_navbar=True,
            label="More",
        )

    search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
    )
    
    test_png = 'website/dashapp/chartpilotlogo.png'
    test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

    navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(test_base64), height="70px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                drop,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="#11171a",
    dark=True,
    )




    select_chart = dbc.DropdownMenu(
    label="Chart Type",
    children=[
        dbc.DropdownMenuItem("Ichimoku"),
        dbc.DropdownMenuItem("Fibonacci"),
        dbc.DropdownMenuItem("RSI"),
    ],
    )

    num_chart = dbc.DropdownMenu(
    label="Number of Charts",
    children=[
        dbc.DropdownMenuItem("1"),
        dbc.DropdownMenuItem("2"),
        dbc.DropdownMenuItem("3"),
        dbc.DropdownMenuItem("4"),
    ],
    )

    stock_crypto = dbc.DropdownMenu(
    label="Trading",
    children=[
        dbc.DropdownMenuItem("Stocks"),
        dbc.DropdownMenuItem("Crypto"),
    ],
    )

    date_picker = dcc.DatePickerRange(id="date",
    month_format='MMMM Y',
    start_date_placeholder_text="Start Period",
    end_date_placeholder_text='End Period',
    end_date=date.today(),
    style={'background-color': 'black'}
    )
    
    first_card = dbc.Card(
        dbc.CardBody(
            dbc.Row(
            [   

                dbc.Col([date_picker], width={'size':2}),

                dbc.Col([
                dbc.Row([dbc.Col(html.H5("Predicted Price")),dbc.Col(html.H5("Status")),dbc.Col(html.H5("Overbought/Oversold"))]),
                
                dbc.Row([dbc.Col(html.H5(id="price")),dbc.Col(html.H5(id="status")),dbc.Col(html.H5(id="Over"))]),

                html.P("Data based off selected date range"),])
            ], style={'padding-right': '0', 'padding-left':'0'}
            )
            )
        )


    portfolio = dash_table.DataTable


    second_card = dbc.Card(
        dbc.CardBody(
            dbc.Row(
            [   

                dbc.Row([html.H5("Your Portfolio")])

            ], style={'padding-right': '0', 'padding-left':'0'}
            )
            )
        )


    ticker_drop = dcc.Dropdown(id='input', options=[{'label': i, 'value': i} for i in tickers], 
            placeholder="Select a Stock Ticker",
            style=dict(display='incline-block',backgroundColor=colors["background"]))

    # Layout for the entire page
    layout = html.Div(id='main', children=[
        navbar,
        html.Div(children=[dbc.Card(dbc.CardBody([
            
            dbc.Row([dbc.Col(ticker_drop,width={'size':9}), dbc.Col(select_chart, width={'offset': 1,})], style={"margin-bottom":'10px'}),

            dcc.Graph(id='my-graph', figure=fig, responsive=True)]),style={'width':'w-50', 'height': '500px'}),

            html.Div([dbc.Row([first_card]),
            ], style={'backgroundColor':colors['background']}),

            html.Div([dbc.Row([second_card]),
            ], style={'backgroundColor':colors['background']}) 
            
        ]),
        
        
        dcc.Store(id='user-store'),
    ], style={'width': '250', 'backgroundColor': colors['background']})

    return layout


