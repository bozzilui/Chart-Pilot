from flask import Blueprint, render_template, Flask
import dash_html_components as html
from dash import Dash, dcc
from flask_login import login_required,  current_user
import pandas as pd
import json
import plotly
import plotly.express as px
import Plot_ichimoku

views = Blueprint('views', __name__)


@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/')
def front():
    # Students data available in a list of list
    students = [['Akash', 34, 'Sydney', 'Australia'],
                ['Rithika', 30, 'Coimbatore', 'India'],
                ['Priya', 31, 'Coimbatore', 'India'],
                ['Sandy', 32, 'Tokyo', 'Japan'],
                ['Praneeth', 16, 'New York', 'US'],
                ['Praveen', 17, 'Toronto', 'Canada']]
     
    # Convert list to dataframe and assign column values
    df = Plot_ichimoku.get_stock_df_from_csv("MSFT")
    """
    df = pd.DataFrame(students,
                      columns=['Name', 'Age', 'City', 'Country'],
                      index=['a', 'b', 'c', 'd', 'e', 'f'])
    """
    # Create Bar chart
    fig = Plot_ichimoku.get_Ichimoku(df)
     
    # Create graphJSON
    plotly_plot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
    # Use render_template to pass graphJSON to html
    return render_template('front.html', plotly_plot=plotly_plot, user=current_user)