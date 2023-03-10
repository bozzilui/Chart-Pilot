from main import app, dashapp
from dash.dependencies import Input, Output, State
import Plot_ichimoku
from Predict_price import predict_stock_prices
from Bolinger_predict import predict
from Overbought_oversold import calc

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
    }

@dashapp.callback(
    Output('my-graph', 'figure'),
    [Input('input', 'value')])
def update_search_term(search_term):
    
    df = Plot_ichimoku.get_stock_df_from_csv(search_term)

    fig = Plot_ichimoku.get_Ichimoku(df)

    fig.update_layout(
    title=search_term,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color="white"
    )

    return fig


@dashapp.callback(
    Output('price', 'children'),
    [Input('date', 'start_date'), Input('date', 'end_date'), Input('input', 'value')] )
def get_price(start_date, end_date, ticker):
    price = predict_stock_prices(ticker, start_date, end_date)
    return price

@dashapp.callback(
    Output('status', 'children'),
    [Input('date', 'start_date'), Input('date', 'end_date'), Input('input', 'value')] )
def get_status(start_date, end_date, ticker):
    status = predict(ticker, start_date, end_date)
    return status

@dashapp.callback(
    Output('Over', 'children'),
    [Input('date', 'start_date'), Input('date', 'end_date'), Input('input', 'value')] )
def get_over(start_date, end_date, ticker):
    status = calc(ticker, start_date, end_date)
    return status


if __name__ == '__main__':
    dashapp.run_server(debug=True)
    #app.run(debug=True)