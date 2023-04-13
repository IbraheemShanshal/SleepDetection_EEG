import dash
from dash import dcc, html, Dash, callback
import pickle
import time

from dash.exceptions import PreventUpdate

dash.register_page(__name__, name="Start_Drive")

# Load the pickle file when the Dash app is launched
with open('output.pkl', 'rb') as f:
    data = pickle.load(f)
    data = data.iloc[:, 0].tolist()  # Convert the DataFrame to a list, iloc is for specific column
    prediction = data[0] if data else None  # make the first content in pkl as first output
    nextline = 1  # Go to next line of output by 1

start_time = time.time()
awake_time = 0
half_asleep_time = 0
fully_asleep_time = 0

# Define the layout of the app
def layout():
    return html.Div([
        html.Div(id='page-content', style={'textAlign': 'center'}),
        html.Div([
            html.Button('Start Drive', id='start-drive-button', n_clicks=0,
                        style={'borderRadius': '50%', 'height': '150px', 'width': '150px', 'fontSize': '24px',
                               'backgroundColor': 'red', 'color': 'white'})
        ], style={'textAlign': 'center'}),
        dcc.Interval(  # For updating in realtime without having to refresh
            id='interval',
            n_intervals=0,
            interval=1000  # update every second
        )
        ])


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

def sleep_summary( awake_time, half_asleep_time, fully_asleep_time):
    return html.Div([
            html.Div([
                html.Details([
                    html.Summary('sleep summary', style={'textAlign': 'center'}),
                    html.Div([
                        html.Div([
                            html.H2('Time Spent Awake', style={'textAlign': 'center'}),
                            html.H1(f'{awake_time} seconds', style={'textAlign': 'center', 'font-size': '2em'})
                        ], className='col-md-4'),
                        html.Div([
                            html.H2('Time Spent Half Asleep', style={'textAlign': 'center'}),
                            html.H1(f'{half_asleep_time} seconds', style={'textAlign': 'center','font-size': '2em'})
                        ], className='col-md-4'),
                        html.Div([
                            html.H2('Time Spent Fully Asleep', style={'textAlign': 'center'}),
                            html.H1(f'{fully_asleep_time} seconds', style={'textAlign': 'center','font-size': '2em'})
                        ], className='col-md-4'),
                    ], className='row', style={'marginBottom': '5%'})
                ], style={'backgroundColor': '#3B296A'})
            ], style={'backgroundColor': '#191A21'})])


# Define the layout of the app
layout = layout()


# Define the callback for the start-drive-button and interval
@callback(dash.dependencies.Output('page-content', 'children'),
          dash.dependencies.Input('start-drive-button', 'n_clicks'),
          dash.dependencies.Input('interval', 'n_intervals'))
def toggle_prediction_layout(n_clicks, n_intervals):
    global start_time, prediction, nextline, data, awake_time, half_asleep_time, fully_asleep_time

    if n_clicks is None:  # this is to make sure there is nothing displayed before pressing the start button
        return html.Div()
    elif n_clicks == 1 or n_intervals < 0: # This is to make it so that the prediction only appears after the start
        # button is pressed
        timer = time.time() - start_time
        if timer > 10:
            if data and nextline < len(data):
                prev_prediction = prediction
                prediction = data[nextline]
                nextline = (nextline + 1) % len(data)

                # Update time variables based on prediction
                if prediction == "Awake":
                    awake_time += 10
                    print(awake_time)
                elif prediction == "Half asleep":
                    half_asleep_time += 10
                elif prediction == "Fully asleep":
                    fully_asleep_time += 10

            else:
                prediction = None
            start_time = time.time()
        return prediction_layout(prediction), sleep_summary(awake_time, half_asleep_time, fully_asleep_time)
    else:
        raise PreventUpdate

