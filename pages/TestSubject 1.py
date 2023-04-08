import dash
from dash import dcc, html, Dash, callback
import pickle
import random
import time



dash.register_page(__name__,path='/')

# Load the pickle file when the Dash app is launched
with open('output.pkl', 'rb') as f:
    data = pickle.load(f)
    prediction = "Half asleep"


start_time = time.time()

# Define the layout of the app
def layout(prediction, awake_time, half_asleep_time, fully_asleep_time):
    return html.Div([
        html.Div(id='page-content', style={'textAlign': 'center'}),
        html.Div([
            html.Button('Start Drive', id='start-drive-button', n_clicks=0, style={'borderRadius': '50%', 'height': '150px', 'width': '150px', 'fontSize': '24px', 'backgroundColor': 'red', 'color': 'white'})
        ], style={'textAlign': 'center'}),
        dcc.Interval(
            id='update-prediction-interval',
            interval=10000,  # this is in miliseconds
            n_intervals=0
        ),
        html.Div([
            html.Div([
                html.Details([
                    html.Summary('sleep summary', style= {'textAlign': 'center'}),
                    html.Div([
                        html.Div([
                            html.H2('Time Spent Awake', style= {'textAlign': 'center'}),
                            html.H1(f'{awake_time} hours', style= {'textAlign': 'center', 'font-size': '2em'})
                        ], className='col-md-4'),
                        html.Div([
                            html.H2('Time Spent Half Asleep', style= {'textAlign': 'center'}),
                            html.H1(f'{half_asleep_time} hours', style= {'textAlign': 'center'})
                        ], className='col-md-4'),
                        html.Div([
                            html.H2('Time Spent Fully Asleep', style= {'textAlign': 'center'}),
                            html.H1(f'{fully_asleep_time} hours', style= {'textAlign': 'center'})
                        ], className='col-md-4'),
                    ], className='row', style={'marginBottom': '5%'})
                ], style={'backgroundColor': '#3B296A'})
            ], style={'backgroundColor': '#191A21'})])])

# Define the layout of the prediction page
def prediction_layout(prediction):
    if prediction == "Awake":
        return html.Div([
            html.H1('You are currently'),
            html.Img(src='../assets/Awake.png'),
            html.H2('Fully Awake'),

        ])
    elif prediction == "Half asleep":

        return html.Div([
            html.H1('Caution: You are currently'),
            html.Img(src='../assets/Sleepy.png'),
            html.H3('Tired and Sleepy'),
            html.H2('Suggestions: Take a nap or drink coffee'),
            html.Audio(src='../assets/beep beep.wav', autoPlay=True)
        ])
    elif prediction == "Fully asleep":
        return html.Div([
            html.H1('Warning: You are currently'),
            html.Img(src='../assets/Drowsy.png'),
            html.H3('Drowsy'),
            html.P('Immediately Pull over and take a nap'),
            html.Audio(src='../assets/Alarm.wav', autoPlay=True)
        ])
    return prediction


# Define the layout of the app
layout = layout(prediction, 0, 0, 0)

# Define the callback for the start-drive-button
@callback(dash.dependencies.Output('page-content', 'children'),
    dash.dependencies.Input('start-drive-button', 'n_clicks'),
    dash.dependencies.Input('update-prediction-interval', 'n_intervals'))

def toggle_prediction_layout(n_clicks, n_intervals):
    if n_intervals > 0:
        # Update prediction randomly
        prediction = random.choice(["Awake", "Half asleep", "Fully asleep"])
        return prediction_layout(prediction)


# Run the app




