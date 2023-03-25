import joblib
import numpy as np
import pandas as pd


from sklearn.metrics import confusion_matrix


df = pd.read_pickle('data.pkl')

# Define the subject ID to use for prediction
subject_ids = ['SC4091E0']

# Filter your data to only include the selected subject
new_data = df[df['subject_id'].isin(subject_ids)]

#select random 20 epochs from this selected subject
random_epoch = new_data.sample(20)

#load model
model, ref_col, target = joblib.load('model.pkl')


X_new = random_epoch[ref_col]
y_new = random_epoch[target]
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

