import joblib
import pandas as pd
import os
import sys


from sklearn.metrics import confusion_matrix
from SleepinessLevel import process_data
from SleepinessLevel import eeg_power_band


UPLOAD_FOLDER = os.path.join(os.getcwd(), r"/Users/yanhui/eclipse-workspace/SEGP-groupXv3/files")

folder_id = sys.argv[1]
folder_path = os.path.join(UPLOAD_FOLDER, folder_id)
print(folder_path)
print(folder_id)


# Get a list of all the files in the folder
files = os.listdir(folder_path)

# Select the first file from the list
if len(files) > 0:
    first_file = files[0]
    second_file = files[1]
else:
    print("No files found in the folder.")

event_id = {'Sleep stage W': 1,
            'Sleep stage 1': 2,
            'Sleep stage 2': 3,
            'Sleep stage 3': 4,
            'Sleep stage 4': 4,
            'Sleep stage R': 5}

file1 = os.path.join(folder_path, first_file)
file2 = os.path.join(folder_path, second_file)
print(file1)
print(file2)

#Download all the datasets
#all_data = fetch_data(subjects=[1], recording=[1])

all_data = [[file1,file2]]



event_id = {'Sleep stage W': 1,
            'Sleep stage 1': 2,
            'Sleep stage 2': 3,
            'Sleep stage 3': 4,
            'Sleep stage 4': 4,
            'Sleep stage R': 5}




#Download all the datasets
#all_data = fetch_data(subjects=[1], recording=[1])

#all_data = [['/Users/yanhui/mne_data/physionet-sleep-data/SC4001E0-PSG.edf','/Users/yanhui/mne_data/physionet-sleep-data/SC4001EC-Hypnogram.edf']]

#all_data = [['/Users/yanhui/eclipse-workspace/SEGP-groupXv3/files/801f57d6-793f-45c6-af61-22f57d5937ae/SC4001E0-PSG.edf','/Users/yanhui/eclipse-workspace/SEGP-groupXv3/files/801f57d6-793f-45c6-af61-22f57d5937ae/SC4001EC-Hypnogram.edf']]

all_ep = [process_data(dpath) for dpath in all_data]

#Loop the epochs data gathering for each data downloaded so that it does not look so cluttered
epochs_datas = [all_ep[i] for i in range(len(all_ep))]


## Here is where i loop thru all preprocessed datas and assign the subject id to it

for i in range(len(all_ep)):
    epochs_data = all_ep[i]
    file_name = os.path.basename(all_data[i][0])
    subject_id = file_name[:8]
    epochs_data.info['subject_info'] = {'id': str(subject_id)}



#Looping sequence for dataframe
dfs = [] #Creates an empty list to store the dfs
for epochs_data in all_ep:
    df = eeg_power_band(epochs_data)
    dfs.append(df)
    #print(df.head()) #Print first five data from the dataframe for all df to see whether everything is working accordingly

#Concatenate all the dataframes
df = pd.concat(dfs, ignore_index=True)


#load model
model, ref_col, target = joblib.load('model.pkl')


X_new = df[ref_col]
y_new = df[target]
predictions = model.predict(X_new)


output = {
    '1': 'Awake',#change to output string that we want to show on GUI
    '2': 'Half asleep',
    '3': 'Fully asleep',
    '4': 'Fully asleep',
    '5': 'Fully asleep'
}


outputs = [output[value] for value in predictions]

print(outputs)

output_df = pd.DataFrame({'output': outputs})

#output files used to display output on GUI
output_df.to_csv('output.csv',index=False)
output_df.to_pickle('output.pkl')

print(predictions)

print(confusion_matrix(y_new, predictions))


