import pandas as pd
import numpy as np
from mne.decoding import Vectorizer
from mne_features.feature_extraction import FeatureExtractor  # Take some time because of Numba

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

import SleepinessLevel as sl

df = pd.read_pickle('data.pkl')



sfreq=100

funcs_params = dict ( pow_freq_bands__normalize=False,
                      pow_freq_bands__ratios='all',
                      pow_freq_bands__psd_method='fft',
                      pow_freq_bands__freq_bands=df)

selected_funcs = ['line_length',
                  'kurtosis',
                  'ptp_amp',
                  'skewness',
                  'pow_freq_bands']

# FeatureExtractor >> function under mne-feature
pipe = make_pipeline( FeatureExtractor(sfreq=sfreq,params=funcs_params,
                                       selected_funcs=selected_funcs),
                      Vectorizer(),
                      RandomForestClassifier(n_estimators=100, random_state=42))


X = sl.epochs.get_data()
y = sl.epochs.events[:, 2]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# epochs_train,epochs_test=epochs_alice,epochs_bob
pipe.fit(X_train,y_train)

# Test
y_pred = pipe.predict(X_test.get_data())

# define the mapping
output = {
    1: 'Sleep stage W',#change to output string that we want to show on GUI?
    2: 'Sleep stage 1',
    3: 'Sleep stage 2',
    4: 'Sleep stage 3/4',
    5: 'Sleep stage R'
}

# use the mapping to convert integers to strings
event_id = 2
event_name = output[event_id]

print(event_name)  # output: Sleep stage 1

# Assess the results
y_test_result = y_test.events[:, 2]
acc = accuracy_score(y_test_result, y_pred)



print("Accuracy score: {}".format(acc))
# Further analysis of the data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# We can check the confusion matrix or the classification report.

print(confusion_matrix(y_test_result, y_pred))


print(classification_report(y_test_result, y_pred,target_names={'Sleep stage W': 1,
                                                                'Sleep stage 1': 2,
                                                                'Sleep stage 2': 3,
                                                                'Sleep stage 3/4': 4,
                                                                'Sleep stage R': 5}))