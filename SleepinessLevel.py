import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import warnings

import mne
#from mne.datasets.sleep_physionet.age import fetch_data

from mne_features.feature_extraction import extract_features

event_id = {'Sleep stage W': 1,
            'Sleep stage 1': 2,
            'Sleep stage 2': 3,
            'Sleep stage 3': 4,
            'Sleep stage 4': 4,
            'Sleep stage R': 5}

# this function will process
def process_data(dpath):            # new way to write with added parameter is " def process_data(dpath, subject_id) "

    # Read the PSG data, raw contains the following:
    # 2d numpy array for data
    # times, info
    # annotations
    raw = mne.io.read_raw_edf(dpath[0], stim_channel='marker', misc=['rectal'])
    #load data into memory
    raw.load_data()

    # Select only EEG
    raw.drop_channels(['EOG horizontal', 'Resp oro-nasal', 'EMG submental', 'Temp rectal',
                       'Event marker'])

    # Extract feature names from channel names
    feature_names = raw.ch_names

    # Filter the high-pass frequency to be 49 and low-pass to 2
    raw.filter(l_freq=2, h_freq=49)

    # making a dictionary for scalings where eeg is the key and the value is 40e-5
    scalings = {'eeg': 40e-5}
    #raw.plot(duration=60, scalings=scalings, remove_dc=False, )
    tmax = 10. - 1. / raw.info['sfreq']  # Epoch size

    # Extract the annotation from the raw file
    annot = mne.read_annotations(dpath[1])
    annot.crop(annot[1]['onset'] - 30 * 60, annot[-2]['onset'] + 30 * 60)

    raw.set_annotations(annot, emit_warning=False)

    events, _ = mne.events_from_annotations(raw, event_id=event_id, chunk_duration=10.)
    # u, indices = np.unique(annot['description'], return_index=True)
    # Create epochs of 30 sec from the continuous signal
    epochs = mne.Epochs(raw=raw, events=events, event_id=event_id, tmin=0., tmax=tmax, baseline=None)
     
    # we can also put this code here but need to add a new parameter for subject_id above
    # epochs_data.info['subject_info'] = {'id': str(subject_id)} 


    return epochs




"""new code"""
subject_ids = range(0, 10) #We can just put range(10) where the ids will start from 0-9


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
        else:
            sleep_stages.append('UNKNOWN')

    return sleep_stages


def eeg_power_band(epochs):
    # specific frequency bands
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


