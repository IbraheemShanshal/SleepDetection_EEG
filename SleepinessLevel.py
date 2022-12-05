# this file will be used to write our own code

import matplotlib.pyplot as plt          #used for visualisations in python
import numpy as np                       #NumPy is used to do a wide range of mathmatical equations

import mne                                                 #to analyse EEG signals
import pandas as pd
from mne.datasets.sleep_physionet.age import fetch_data    #importing the dataset
from mne.decoding import (Vectorizer)



from sklearn.ensemble import RandomForestClassifier        #sklearn is used for machine learning
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
import featurewiz                                          #automated tool to help choose the best features in the dataset to focus on
from featurewiz import featurewiz

event_id = {'Sleep stage W': 1,
            'Sleep stage 1': 2,
            'Sleep stage 2': 3,
            'Sleep stage 3': 4,
            'Sleep stage 4': 4,
            'Sleep stage R': 5}

def some_operation(dpath):

    # Read the PSG data
    raw = mne.io.read_raw_edf(dpath[0], stim_channel='marker',misc=['rectal'])

    # Select only EEG
    raw.drop_channels(['EOG horizontal','Resp oro-nasal','EMG submental','Temp rectal',
                       'Event marker'])

    scalings = dict(eeg=40e-5)
    raw.plot(duration=60, scalings=scalings,remove_dc=False,)
    tmax = 30. - 1. / raw.info['sfreq']  # Epoch size
    # Extract the annotation from the raw file
    annot = mne.read_annotations(dpath[1])
    annot.crop(annot[1]['onset'] - 30 * 60,annot[-2]['onset'] + 30 * 60)

    raw.set_annotations(annot, emit_warning=False)
    events, _ = mne.events_from_annotations(raw, event_id=event_id, chunk_duration=30.)
    # u, indices = np.unique(annot['description'], return_index=True)

    # Create epochs of 30 sec from the continous signal
    epochs = mne.Epochs(raw=raw, events=events, event_id=event_id,tmin=0., tmax=tmax, baseline=None)

    return epochs

df = pd.read_csv("your_csv_file.csv")
df.head()
target = 'Event marker'
features = featurewiz(df, target, corr_limit=0.70, verbose=2)



ALICE, BOB = 0, 1
# Download data from sleep Physionet dataset
all_data = fetch_data(subjects=[ALICE, BOB], recording=[1])
# Read the PSG data and Hypnograms to create a raw object
all_ep=[some_operation(dpath) for dpath in all_data]

epochs_alice,epochs_bob=all_ep
print(epochs_alice.info)
print(epochs_bob.info)
