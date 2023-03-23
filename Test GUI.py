import dash
import pandas as pd
from dash import dcc,html,Dash

from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import mne
import pickle
import numpy as np
from mne_features.feature_extraction import extract_features
import pyedflib


def preprocessed_data(data):


    event_id = {'Sleep stage W': 1,
                'Sleep stage 1': 2,
                'Sleep stage 2': 3,
                'Sleep stage 3': 4,
                'Sleep stage 4': 4,
                'Sleep stage R': 5}

    # Read the PSG data, raw contains the following:
    # 2d numpy array for data
    # times, info
    # annotations
    raw = mne.io.read_raw_edf(data, stim_channel='marker', misc=['rectal'])
    #load data into memory
    raw.load_data()

    # Select only EEG
    raw.drop_channels(['EOG horizontal', 'Resp oro-nasal', 'EMG submental', 'Temp rectal',
                       'Event marker'])

    # Extract feature names from channel names
    #feature_names = raw.ch_names

    # Filter the high-pass frequency to be 49 and low-pass to 2
    raw.filter(l_freq=2, h_freq=49)

    # making a dictionary for scalings where eeg is the key and the value is 40e-5
    #scalings = {'eeg': 40e-5}
    #raw.plot(duration=60, scalings=scalings, remove_dc=False, )

    tmax = 30. - 1. / raw.info['sfreq']  # Epoch size

    # Extract the annotation from the raw file
    annot = mne.read_annotations(data)
    annot.crop(annot[1]['onset'] - 30 * 60, annot[-2]['onset'] + 30 * 60)

    raw.set_annotations(annot, emit_warning=False)


    events, _ = mne.events_from_annotations(raw, event_id=event_id, chunk_duration=30.)
    # u, indices = np.unique(annot['description'], return_index=True)
    # Create epochs of 30 sec from the continuous signal
    epochs = mne.Epochs(raw=raw, events=events, event_id=event_id, tmin=0., tmax=tmax, baseline=None)

def prediction(model, data):
    # load the model from disk
    load_model = pickle.load(open('model.pkl', 'rb'))

    predictions = model.predict(load_model.get_data())

    if predictions == 1:
        return html.Div([
            html.P('You are sleepy')
        ])
    elif predictions == 0:
        return html.Div([
            html.P('You are not sleepy')
        ])
    elif predictions == 2:
        return html.Div([
            html.P('You are very sleepy')
        ])
    elif predictions == 3:
        return html.Div([
            html.P('You are asleep')
        ])
    elif predictions == 4:
        return html.Div([
            html.P('You are asleep')
        ])
    elif predictions == 5:
        return html.Div([
            html.P('You are asleep')
        ])
    return predictions

app = Dash(__name__)    # create Dash app
app.title = 'Sleepiness Detection'  # set title
server = app.server    # set server

app.layout = html.Div([ # define layout
    dcc.Tabs([  # define tabs
        dcc.Tab(label='Upload EDF', children=[ # define tab for uploading edf
            dcc.Upload(
                id='upload-edf',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                },
                multiple=False
            ),
            html.Div(id='output-data-upload')
        ]),
        dcc.Tab(label='EEG Signals', children=[ # define tab for eeg signals
            html.Div(id='warning')
        ]),
        dcc.Tab(label='Classification',children=[

        ])
    ])
])

@app.callback(Output('output-data-upload', 'children'),
                Input('upload-edf', 'contents'))

def warnings(contents):

    if contents is not None:
        #Read the EDF file
        df = pyedflib.EdfReader(contents)
        
        processed_data = preprocessed_data(df)
        #extracted_features = feature_extract(processed_data)

        model = prediction(processed_data,df)

        return html.Div([
            html.H5('warning'),
            html.Pre(model)
        ])
    else:
        # If no file has been uploaded yet
        return html.Div('Upload EDF again')




if __name__ == '__main__':
    app.run_server(debug=True)

