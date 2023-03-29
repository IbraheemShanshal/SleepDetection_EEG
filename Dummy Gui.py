import dash
from dash import dcc, html, Dash
import pickle
import winsound
import random

# Load the pickle file when the Dash app is launched
with open('output.pkl', 'rb') as f:
    data = pickle.load(f)
    prediction = data.iloc[2]['output']

#image_path = '/SEGP-groupXver3/Drowsy.png'

# Define the layout of the app

def layout (prediction):
    if prediction == "Awake":
        return html.Div([
            html.H1('You are currently'),
            html.Img(src='assets/Awake.png'),
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
app.layout = layout(prediction)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
