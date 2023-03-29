import time
import uuid

import dash
import joblib
import pandas as pd
from dash import dcc,html,Dash

from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import mne
import pickle
import numpy as np
from mne_features.feature_extraction import extract_features
import pyedflib
import dash_uploader as du




model, ref_col, target = joblib.load('model.pkl')
data = pd.read_pickle('output.pkl')

app = Dash(__name__)    # create Dash app
app.title = 'Sleepiness Detection'  # set title
server = app.server    # set server

UPLOAD_FOLDER_ROOT = r"/Users/yanhui/eclipse-workspace/SEGP-groupXv3/files"
du.configure_upload(app, UPLOAD_FOLDER_ROOT)

def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=100, # 1800 Mb
        filetypes=['edf'],
        upload_id=uuid.uuid1(), # Unique session id
        max_files=2,  # Maximum number of files allowed to be uploaded
    )


app.layout = html.Div([ # define layout
    dcc.Tabs([  # define tabs
        dcc.Tab(label='Upload EDF', children=[ # define tab for uploading edf
            html.Div(
                [
                    get_upload_component(id='dash-uploader'),
                    html.Div(id='callback-output'),
                ],

            ),
            html.Button('Show output', id='show-row-button'),
            html.Div(
                id='output-data-upload',
            ),
            #dcc.Interval(id='interval', interval=2000, n_intervals=0)
        ]),
        dcc.Tab(label='EEG Signals', children=[ # define tab for eeg signals
            html.Div(id='warning')
        ]),
        dcc.Tab(label='Classification',children=[

        ])
    ])
])

'''
@app.callback(Output('output-data-upload', 'children'),
              State('show-row-button', 'n_clicks'),
              Input('interval', 'n_intervals')
)
'''
@du.callback(
    output=Output('callback-output', 'children'),
    id='dash-uploader',
)

@app.callback(Output('output-data-upload', 'children'),
              Input('show-row-button', 'n_clicks')
              )



def prediction(n_clicks):
    # load the model from disk
    values_list = []
    if n_clicks is None:
        return ''
    else:
        data.reset_index(drop=True, inplace=True)
        for i in range(len(data)):
            value = data.iloc[i].values
            #time.sleep(1)
            #print(value)
            values_list.append(html.Div([html.P(value)]))
            # Return a Div containing the current value
        return html.Div(values_list)
        #return values_list

#@app.callback(Output('output-data-upload', 'children'),
#                Input('upload-edf', 'contents'))


#def show_output(n_intervals):
#        return prediction(n_intervals)


'''
def warnings(contents):

    if contents is not None:
        #Read the EDF file
        #df = pyedflib.EdfReader(contents)

        #extracted_features = feature_extract(processed_data)


        prediction()

        return html.Div([
            html.H5('warning'),
            html.Pre(model)
        ])
    else:
        # If no file has been uploaded yet
        return html.Div('Upload EDF again')
'''







if __name__ == '__main__':
    app.run_server(debug=True)

