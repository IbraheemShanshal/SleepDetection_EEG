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
import os

# download the dataset with EEG files from physionet
from mne.datasets import sleep_physionet
sleep_physionet.age.fetch_data(subjects=[0])

#reading database
sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_filt-0-40_raw.fif')

# loading data into memory
raw = mne.io.read_raw_fif(sample_data_raw_file,preload=True) #preload is true because the file is preloaded, if its not working change it to false

#Getting basic info about the dataset
print('raw info:')
print(raw.info)

original_raw = raw.copy()
rereferenced_raw, ref_data = mne.set_eeg_reference(raw, ['EEG 003'],copy=True)

#modifying data in-place
raw.crop(tmax=60.)
print('raw:')
print(raw)

print('bad channels:', raw.info['bads'])
print(raw.info['sfreq'], 'Hz')
print(raw.info['description'], '\n')

# we make copy is equal to true, so we preserve a copy of the original file for comparison or to do operations on it
rereferenced_raw, ref_data = mne.set_eeg_reference(raw, ['EEG 003'],copy=True)
original_raw = raw.copy()
eeg = raw.copy().pick_types(meg=False, eeg=True, eog=False) #we only want to select EEG so we dropped other chanlles
print(len(raw.ch_names), '→', len(eeg.ch_names))

raw_temp = raw.copy()
print('Number of channels in raw_temp:')
print(len(raw_temp.ch_names), end=' → drop two → ')
raw_temp.drop_channels(['EEG 037', 'EEG 059'])
print(len(raw_temp.ch_names), end=' → pick three → ')

#selection of frontal eeg censors
raw_temp.pick_channels(['EEG 017'])
channel_names = [ 'EEG 003', 'EEG 002', 'EEG 001']
frontal_eeg = raw.copy().reorder_channels(channel_names)

# selection of data in a time domain, because the time is too long for a full file to be processed
# we need to copy the data first
raw_selection = raw.copy().crop(tmin=10, tmax=12.5)
print(raw_selection)
print(raw_selection.times.min(), raw_selection.times.max())
raw_selection.crop(tmin=1)
print(raw_selection.times.min(), raw_selection.times.max())