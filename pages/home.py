import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name="Homepage", external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Description')),
    ]),
    dbc.Row([

        dbc.Col(html.Img(src='../assets/Awake.png')),
        dbc.Col(html.Img(src='../assets/Drowsy.png')),
    ]),
    dbc.Row([
        dbc.Col(html.P('This app performs sleep stage classification for a subject\'s recorded EEG signals. The goal of our project is to create a web application that can alert people when they fall asleep while driving.To accomplish this, we need to determine if the person is awake, half asleep (N1), or asleep (N2 and below).This is done by using machine learning algorithm - random forest classification.'
)),
    ]),
])

#    background-color: #1c1446;