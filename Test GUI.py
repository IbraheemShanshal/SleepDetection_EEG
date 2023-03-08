import base64
import io


import dash
import pandas as pd
from dash import dcc,html,Dash

from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import mne
import pickle
import numpy as np

app = Dash(__name__)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Upload EDF', children=[
            dcc.Upload(
                id='upload-edf',
                accept='.edf',
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
        dcc.Tab(label='EEG Signals', children=[
            dcc.Graph(id='eeg-graph'),
            html.Div(id='warning')
        ]),
        dcc.Tab(label='Classification',children=[

        ])
    ])
])

#below is before i add the preprocessing part
'''
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-edf', 'contents'),
              State('upload-edf', 'filename'))
def update_output(content, filename):
    
    if content is not None:

        # Read EDF file


        return html.Div([
            html.H5(filename),
            html.P('Data uploaded and preprocessed successfully!')
        ])

    else:
        return html.Div([
            html.P('Upload EDF file to begin')
        ])

@app.callback(Output('eeg-graph', 'figure'),
              Input('output-data-upload', 'children'))'''

#below is after putting preprocesing

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-edf', 'contents'),
              State('upload-edf', 'filename'))
def update_output(content, filename):

        event_id = {'Sleep stage W': 1,
                    'Sleep stage 1': 2,
                    'Sleep stage 2': 3,
                    'Sleep stage 3': 4,
                    'Sleep stage 4': 4,
                    'Sleep stage R': 5}

        if content is not None:
            # Read EDF file
            content_type, content_string = content.split(',')
            decoded = base64.b64decode(content_string)
            file_like_object = io.BytesIO(decoded)

            raw = mne.io.read_raw_edf(file_like_object, stim_channel='marker', misc=['rectal'])
            raw.load_data()

            scalings = dict(eeg=40e-5)
            raw.plot(duration=60, scalings=scalings, remove_dc=False, )
            tmax = 30. - 1. / raw.info['sfreq']  # Epoch size
            events, _ = mne.events_from_annotations(raw, event_id=event_id, chunk_duration=30.)

            # Preprocess data
            raw.drop_channels(['EOG horizontal', 'Resp oro-nasal', 'EMG submental', 'Temp rectal', 'Event marker'])
            raw.filter(l_freq=2, h_freq=49)
            epochs = mne.Epochs(raw=raw, events=events, event_id=event_id, tmin=0., tmax=tmax, baseline=None)

            # Save preprocessed data to file
            with open("preprocessed_data.pkl", "wb") as f:
                pickle.dump({"data": epochs.get_data(), "labels": epochs.events[:, 2]}, f)

            return html.Div([
                html.H5(filename),
                html.P('Data uploaded and preprocessed successfully!')
            ])
        else:
            return html.Div([
                html.P('Upload EDF file to begin')
            ])

@app.callback(Output('eeg-graph', 'figure'),
              Input('output-data-upload', 'children'))

def update_eeg_graph(data):

    with open("preprocessed_data.pkl", "rb") as f:
        preprocessed_data = pickle.load(f)

# access the preprocessed data and labels
    data = preprocessed_data["data"]
    labels = preprocessed_data["labels"]

    # create the plotly figure object
    fig = go.Figure()
    for i in range(data.shape[0]):
        fig.add_trace(go.Scatter(x=np.arange(data.shape[1])/100, y=data[i], name=f"Channel {i+1}"))

    fig.update_layout(title='EEG Signals')

    return fig

@app.callback(Output('warning', 'children'),
              Input('eeg-graph', 'figure'))
def check_sleep_stage_threshold(figure):
    # Determine sleep stage threshold and check if exceeded
    exceeded = True
    # ...
    if exceeded:
        return html.Div([
            html.P('WARNING: WAKE UP, YOU ARE DRIVING')
        ])
    else:
        return html.Div([])

if __name__ == '__main__':
    app.run_server(debug=True)

