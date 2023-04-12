import os
import subprocess
import uuid
import base64

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, callback


dash.register_page(__name__, path='/', name="Upload_Page")

UPLOAD_FOLDER_ROOT = r"C:/Jinming/UNM/SEGP/files"


# Set the upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), r"C:/Jinming/UNM/SEGP/files")

# Define the layout of the home page
layout = html.Div([
    html.H1('Upload a file'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and drop or click to select a file to upload.'
        ]),
        style={
            'width': '99%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True,
        accept='.edf'
    ),
    html.Div(id='output-data-upload')
])

# Define the callback function to save uploaded files
@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'filename'),
              State('upload-data', 'contents'))
def update_output(list_of_filenames, list_of_contents):
    if list_of_contents is None or list_of_filenames is None:
        return html.Div([
            'No file has been uploaded yet'
        ])

    edf_files = []
    for content, filename in zip(list_of_contents, list_of_filenames):
        if content is None:
            continue

        try:
            content_type, content_string = content.split(',')
        except ValueError:
            return html.Div([
                'Error: Could not process file'
            ])

        decoded = base64.b64decode(content_string)
        file_extension = os.path.splitext(filename)[1]

        if file_extension != '.edf':
            return html.Div([
                'Error: Only EDF files are allowed'
            ])

        try:
            # process the uploaded file here
            edf_files.append(filename)
        except Exception as e:
            print(e)
            return html.Div([
                'Error: Could not process file'
            ])

    if len(edf_files) != 2:
        return html.Div([
            'Error: Please upload exactly two EDF files'
        ])

    # process the uploaded files here
    return save_uploaded_files(list_of_filenames, list_of_contents)
    # return an empty div to reset the error message
    # return html.Div()

def save_uploaded_files(filenames, contents):
    if filenames is not None and contents is not None:
        # Generate a unique ID for the folder
        folder_id = str(uuid.uuid4())
        folder_path = os.path.join(UPLOAD_FOLDER, folder_id)
        os.makedirs(folder_path)
        # Save the uploaded files to the folder
        for filename, content in zip(filenames, contents):
            with open(os.path.join(folder_path, filename), 'wb') as f:
                f.write(base64.b64decode(content.split(',')[1]))
        # Run the other Python file with the folder ID as a command-line argument
        subprocess.run(['python', 'predict.py', folder_id])
        # Return a message with the folder ID and uploaded filenames
        return html.Div([html.P('The following files have been uploaded and saved to folder ' + folder_id + ':')] + [html.P(filename) for filename in filenames])
    else:
        return html.Div([
            html.P('No files have been uploaded.')
        ])


"""
def save_uploaded_files(filenames, contents):
    if filenames is not None and contents is not None:
        for filename, content in zip(filenames, contents):
            with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
                f.write(content.encode('utf-8'))
        return html.Div([
                            html.P('The following files have been uploaded and saved:')
                        ] + [html.P(filename) for filename in filenames])
    else:
        return html.Div([
            html.P('No files have been uploaded.')
        ])

"""