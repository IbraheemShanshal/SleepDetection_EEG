import base64
import io
import plotly.express as px

import warnings
import dash
import pandas as pd
from dash import dcc,html,Dash

from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import mne
import pickle
import numpy as np
from mne_features.feature_extraction import extract_features


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
    scalings = {'eeg': 40e-5}
    #raw.plot(duration=60, scalings=scalings, remove_dc=False, )
    tmax = 30. - 1. / raw.info['sfreq']  # Epoch size


    events, _ = mne.events_from_annotations(raw, event_id=event_id, chunk_duration=30.)
    # u, indices = np.unique(annot['description'], return_index=True)
    # Create epochs of 30 sec from the continuous signal
    epochs = mne.Epochs(raw=raw, events=events, event_id=event_id, tmin=0., tmax=tmax, baseline=None)

def get_sleep_stages(epochs):
    """
    Returns an array of sleep stage labels corresponding to each epoch in the given MNE Epochs object.
    """
    # Assuming you have access to the sleep stage information in your code, you can get it using the following:
    sleep_stage_data = epochs.events[:, 2]
    sleep_stages = []

    # Map the sleep stage codes to their corresponding labels
    for stage in sleep_stage_data:
        if stage == 1:
            sleep_stages.append('1')
        elif stage == 2:
            sleep_stages.append('2')
        elif stage == 3:
            sleep_stages.append('3')
        elif stage == 4:
            sleep_stages.append('4')
        elif stage == 5:
            sleep_stages.append('5')
        #elif stage == 6:
        #    sleep_stages.append('5')
        else:
            sleep_stages.append('UNKNOWN')

    return sleep_stages

def feature_extract(epochs):
    #specific frequency bands
    FREQ_BANDS = {"delta": [0.5, 4.5],
                  "theta": [4.5, 8.5],
                  "alpha": [8.5, 11.5],
                  "sigma": [11.5, 15.5],
                  "beta": [15.5, 30],
                  }  # no gamma because it has freq higher than Ntquist frequency

    warnings.simplefilter(action='ignore', category=FutureWarning)

    selected_features = ['pow_freq_bands']

    freq_bands = np.unique(np.concatenate(list(map(list, (FREQ_BANDS.values())))))

    funcs_params = dict(pow_freq_bands__normalize=False,
                        pow_freq_bands__ratios='all',
                        pow_freq_bands__psd_method='fft',
                        pow_freq_bands__freq_bands=freq_bands)

    sfreq = epochs.info['sfreq']
    features_all = extract_features(epochs.get_data(),
                                    sfreq,
                                    selected_funcs=selected_features,
                                    return_as_df=True,
                                    funcs_params=funcs_params)

    # Get the subject ID
    file_name = epochs.info['subject_info']['id']
    subject_name = file_name[:8]


    # Get the sleep stage information, assuming it's available
    sleep_stages = get_sleep_stages(epochs)  # replace this with your own function that gets the sleep stages

    # create a new dataframe with the data, sleep stage, and subject_id columns
    data = pd.DataFrame(features_all)
    data['sleep_stage'] = sleep_stages
    data['subject_id'] = subject_name


    # display the data in a table-like view
    #print(data.to_string(index=False))

    return data

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
            dcc.Graph(id='eeg-graph'),
            html.Div(id='warning')
        ]),
        dcc.Tab(label='Classification',children=[

        ])
    ])
])

@app.callback(Output('output-data-upload', 'children'),
                Input('upload-edf', 'contents'),
                State('upload-edf', 'filename'))

def update_output(contents, filename):

    if contents is not None:
        processed_data = preprocessed_data(contents)

        extracted_features = feature_extract(processed_data)
    return html.Div(id = 'featured_data')



if __name__ == '__main__':
    app.run_server(debug=True)
