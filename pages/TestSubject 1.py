import dash
from dash import dcc, html, Dash, callback
import pickle
import time

from dash.exceptions import PreventUpdate

dash.register_page(__name__         )

# Load the pickle file when the Dash app is launched
with open('output.pkl', 'rb') as f:
    data = pickle.load(f)
    data = data.iloc[:, 0].tolist()  # Convert the DataFrame to a list, iloc is for specific column
    prediction = data[0] if data else None  # make the first content in pkl as first output
    nextline = 1  # Go to next line of output by 1

start_time = time.time()

# Define the layout of the app
def layout(prediction, awake_time, half_asleep_time, fully_asleep_time):
    return html.Div([
        html.Div(id='page-content', style={'textAlign': 'center'}),
        html.Div([
            html.Button('Start Drive', id='start-drive-button', n_clicks=0,
                        style={'borderRadius': '50%', 'height': '150px', 'width': '150px', 'fontSize': '24px',
                               'backgroundColor': 'red', 'color': 'white'})
        ], style={'textAlign': 'center'}),
        dcc.Interval(  # For updating in realtime without having to refresh
            id='interval',
            n_intervals=0
        ),
        html.Div([
            html.Div([
                html.Details([
                    html.Summary('sleep summary', style={'textAlign': 'center'}),
                    html.Div([
                        html.Div([
                            html.H2('Time Spent Awake', style={'textAlign': 'center'}),
                            html.H1(f'{awake_time} hours', style={'textAlign': 'center', 'font-size': '2em'})
                        ], className='col-md-4'),
                        html.Div([
                            html.H2('Time Spent Half Asleep', style={'textAlign': 'center'}),
                            html.H1(f'{half_asleep_time} hours', style={'textAlign': 'center'})
                        ], className='col-md-4'),
                        html.Div([
                            html.H2('Time Spent Fully Asleep', style={'textAlign': 'center'}),
                            html.H1(f'{fully_asleep_time} hours', style={'textAlign': 'center'})
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


# Define the callback for the start-drive-button and interval
@callback(dash.dependencies.Output('page-content', 'children'),
          dash.dependencies.Input('start-drive-button', 'n_clicks'),
          dash.dependencies.Input('interval', 'n_intervals'))
def toggle_prediction_layout(n_clicks, n_intervals):
    global start_time, prediction, nextline, data

    if n_clicks is None:  # this is to make sure there is nothing displayed before pressing the start button
        return html.Div()
    elif n_clicks == 1 or n_intervals < 0:  # This is to make it so that the prediction only appears after the start
        # button is pressed
        timer = time.time() - start_time
        if timer > 10:  # Update prediction every 10 seconds *note: change to liking
            if data and nextline < len(data):
                prediction = data[nextline]  # Get next content from output.pkl
                nextline = (nextline + 1) % len(data)  # Go to the next line in output.pkl
            else:
                prediction = None
            start_time = time.time()  # Reset start button
        return prediction_layout(prediction)
    else:
        raise PreventUpdate
