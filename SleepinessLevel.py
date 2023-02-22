import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import mne
from mne.datasets.sleep_physionet.age import fetch_data
from mne.decoding import Vectorizer

import mne_features
from mne_features.feature_extraction import extract_features
from mne.time_frequency import psd_multitaper

event_id = {'Sleep stage W': 1,
            'Sleep stage 1': 2,
            'Sleep stage 2': 3,
            'Sleep stage 3': 4,
            'Sleep stage 4': 4,
            'Sleep stage R': 5}


def some_operation(dpath):
    # Read the PSG data
    raw = mne.io.read_raw_edf(dpath[0], stim_channel='marker', misc=['rectal'])
    raw.load_data()

    # Select only EEG
    raw.drop_channels(['EOG horizontal', 'Resp oro-nasal', 'EMG submental', 'Temp rectal',
                       'Event marker'])

    #Filter the high-pass frequency to be 49
    raw.filter(l_freq=2,h_freq=49)

    scalings = dict(eeg=40e-5)
    raw.plot(duration=60, scalings=scalings, remove_dc=False, )
    tmax = 30. - 1. / raw.info['sfreq']  # Epoch size

    # Extract the annotation from the raw file
    annot = mne.read_annotations(dpath[1])
    annot.crop(annot[1]['onset'] - 30 * 60, annot[-2]['onset'] + 30 * 60)

    raw.set_annotations(annot, emit_warning=False)

    events, _ = mne.events_from_annotations(raw, event_id=event_id, chunk_duration=30.)
    # u, indices = np.unique(annot['description'], return_index=True)

    # Create epochs of 30 sec from the continous signal
    epochs = mne.Epochs(raw=raw, events=events, event_id=event_id, tmin=0., tmax=tmax, baseline=None)

    return epochs


Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# Download data from sleep Physionet dataset
all_data = fetch_data(subjects=[Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10], recording=[1])
# Read the PSG data and Hypnograms to create a raw object
all_ep = [some_operation(dpath) for dpath in all_data]

epochs_data1, epochs_data2, epochs_data3, epochs_data4, epochs_data5, epochs_data6, epochs_data7, epochs_data8, epochs_data9, epochs_data10 = all_ep
print(epochs_data1.info)
print(epochs_data2.info)
print(epochs_data3.info)
print(epochs_data4.info)
print(epochs_data5.info)
print(epochs_data6.info)
print(epochs_data7.info)
print(epochs_data8.info)
print(epochs_data9.info)
print(epochs_data10.info)

stage_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10) = plt.subplots(ncols=10, figsize=(50, 6))

stages = sorted(event_id.keys())
for ax, title, epochs in zip([ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10],
                             ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8', 'Data9',
                              'Data10'],
                             [epochs_data1, epochs_data2, epochs_data3, epochs_data4, epochs_data5, epochs_data6,
                              epochs_data7, epochs_data8, epochs_data9, epochs_data10]):

    for stage, color in zip(stages, stage_colors):
        epochs[stage].plot_psd(area_mode=None, color=color, ax=ax, fmin=0.1, fmax=40., show=False,
                               average=True, spatial_colors=False)

    ax.set(title=title, xlabel='Frequency (Hz)')
ax2.set(ylabel='µV^2/Hz (dB)')
ax2.legend(ax2.lines[2::3], stages)
plt.tight_layout()
plt.show()

def eeg_power_band(epochs):
    # specific frequency bands
    FREQ_BANDS = {"delta": [0.5, 4.5],
                  "theta": [4.5, 8.5],
                  "alpha": [8.5, 11.5],
                  "sigma": [11.5, 15.5],
                  "beta": [15.5, 30],
                  } # no gamma because it has freq higher than Ntquist frequency

    selected_features = ['pow_freq_bands']

    freq_bands=np.unique(np.concatenate(list(map(list, (FREQ_BANDS.values())))))

    funcs_params = dict ( pow_freq_bands__normalize=False,
                          pow_freq_bands__ratios='all',
                          pow_freq_bands__psd_method='fft',
                          pow_freq_bands__freq_bands=freq_bands)

    sfreq=epochs.info['sfreq']
    features_all = extract_features(epochs.get_data(),
                                    sfreq,
                                    selected_funcs=selected_features,
                                    return_as_df=True,
                                    funcs_params=funcs_params)

    return features_all
df = eeg_power_band(epochs)
print(df.head())
df.to_csv('eeg_power.csv', index=False)
