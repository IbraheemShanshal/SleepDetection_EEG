import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

import mne
from mne.datasets.sleep_physionet.age import fetch_data

from mne_features.feature_extraction import extract_features

#
event_id = {'Sleep stage W': 1,
            'Sleep stage 1': 2,
            'Sleep stage 2': 3,
            'Sleep stage 3': 4,
            'Sleep stage 4': 4,
            'Sleep stage R': 5}

# this function will process
def process_data(dpath):

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
    raw.plot(duration=60, scalings=scalings, remove_dc=False, )
    tmax = 30. - 1. / raw.info['sfreq']  # Epoch size

    # Extract the annotation from the raw file
    annot = mne.read_annotations(dpath[1])
    annot.crop(annot[1]['onset'] - 30 * 60, annot[-2]['onset'] + 30 * 60)

    raw.set_annotations(annot, emit_warning=False)

    events, _ = mne.events_from_annotations(raw, event_id=event_id, chunk_duration=30.)
    # u, indices = np.unique(annot['description'], return_index=True)
    # Create epochs of 30 sec from the continuous signal
    epochs = mne.Epochs(raw=raw, events=events, event_id=event_id, tmin=0., tmax=tmax, baseline=None)

    return epochs

# assigning numbers here for easy readability
Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# Download data from sleep Physionet dataset
all_data = fetch_data(subjects=[Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10], recording=[1])
# Read the PSG data and Hypnograms to create a raw object
all_ep = [process_data(dpath) for dpath in all_data]

# assigning data to epochs
epochs_data1, epochs_data2, epochs_data3, epochs_data4, epochs_data5, epochs_data6, epochs_data7, epochs_data8, epochs_data9, epochs_data10 = all_ep


#this is all a trial:
for i in range(len(all_data)):
    file_name = os.path.basename(all_data[i][0])
    subject_name = file_name[:8]
    print(subject_name)


#Do something with the subject's data or name


# print(epochs_data1.info)
# print(epochs_data1.events[:,2])
# print(epochs_data2.info)
# print(epochs_data3.info)
# print(epochs_data4.info)
# print(epochs_data5.info)
# print(epochs_data6.info)
# print(epochs_data7.info)
# print(epochs_data8.info)
# print(epochs_data9.info)
# print(epochs_data10.info)

stage_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10) = plt.subplots(ncols=10, figsize=(50, 6))

stages = sorted(event_id.keys())
for ax, title, epochs in zip([ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10],
                             ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8', 'Data9',
                              'Data10'],
                             [epochs_data1, epochs_data2, epochs_data3, epochs_data4, epochs_data5, epochs_data6,
                              epochs_data7, epochs_data8, epochs_data9, epochs_data10]):

    for stage, color in zip(stages, stage_colors):
        ps = epochs[stage].compute_psd(fmin=0.1, fmax=40.)
        ps.plot(ci=None, color=color, axes=ax,
                show=False, average=True, spatial_colors=False)

    ax.set(title=title, xlabel='Frequency (Hz)')
ax1.set(ylabel='µV^2/Hz (dB)')
ax2.legend(ax2.lines[2::3], stages)
plt.tight_layout()
plt.show()

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
            sleep_stages.append('4')
        elif stage == 6:
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

    file_name = os.path.basename(all_data[1][0])
    subject_name = file_name[:8]

    # Get the sleep stage information, assuming it's available
    sleep_stages = get_sleep_stages(epochs)  # replace this with your own function that gets the sleep stages

    # create a new dataframe with the data, sleep stage, and subject_id columns
    data = pd.DataFrame(features_all)
    data['sleep_stage'] = sleep_stages
    data['subject_id'] = subject_name

    # display the data in a table-like view
    print(data.to_string(index=False))

    return data




# features_all, subject_name = eeg_power_band(epochs_data1)
# selected_features = ['pow_freq_bands']

df1 = eeg_power_band(epochs_data1)
df2 = eeg_power_band(epochs_data2)
df3 = eeg_power_band(epochs_data3)
df4 = eeg_power_band(epochs_data4)
df5 = eeg_power_band(epochs_data5)
df6 = eeg_power_band(epochs_data6)
df7 = eeg_power_band(epochs_data7)
df8 = eeg_power_band(epochs_data8)
df9 = eeg_power_band(epochs_data9)
df10 = eeg_power_band(epochs_data10)
df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10])

# print the concatenated dataframe
print(df)
df.to_csv('test.csv',index=False)
df.to_pickle('data.pkl')

