import dash
from dash import dcc, html, Dash
import pickle
import winsound
import random

# Load the pickle file when the Dash app is launched
with open('output.pkl', 'rb') as f:
    data = pickle.load(f)
    prediction = "Awake"

# Define the layout of the app
def layout(prediction, awake_time, half_asleep_time, fully_asleep_time):
    return html.Div([
        html.Div(id='page-content', style={'textAlign': 'center'}),
        html.Div([
            html.Button('Start Drive', id='start-drive-button', n_clicks=0, style={'borderRadius': '50%', 'height': '150px', 'width': '150px', 'fontSize': '24px', 'backgroundColor': 'red', 'color': 'white'})
        ], style={'textAlign': 'center'}),
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
            html.Img(src='assets/Awake.jpg'),
            html.H2('Fully Awake'),

        ])
    elif prediction == "Half asleep":
        winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
        return html.Div([
            html.H1('Caution: You are currently'),
            #html.Audio(src='assets/Lily Laughs.wav', controls=False),
            html.Img(src='assets/Sleepy.png'),
            html.H3('Tired and Sleepy'),
            html.H2('Suggestions: Take a nap or drink coffee')
        ])
    elif prediction == "Fully asleep":
        return html.Div([
            html.H1('Warning: You are currently'),
            html.Img(src='assets/Drowsy.png'),
            html.H3('Drowsy'),
            html.P('Immediately Pull over and take a nap')
        ])
    return prediction

# Create the Dash app
app = dash.Dash(__name__)
app.title = 'Sleepiness Detection'
server = app.server    # set server

# Define the layout of the app
app.layout = layout(prediction, 0, 0, 0)

# Define the callback for the start-drive-button
@app.callback(dash.dependencies.Output('page-content', 'children'),
              dash.dependencies.Input('start-drive-button', 'n_clicks'))
def toggle_prediction_layout(n_clicks):
    if n_clicks > 0:
        return prediction_layout(prediction)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



