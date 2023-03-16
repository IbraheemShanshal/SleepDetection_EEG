from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GroupKFold

import pandas as pd

df = pd.read_pickle('data.pkl')


#X = data of selected features of each epochs (select first to third last column of datas of df)
X = df.iloc[:, :-2]
#y = sleep stage of each epochs (select second last column of df)
y = df.iloc[:, -2]

#Groups = subject_id
groups = df.iloc[:, -1]

# 3 folds
n_splits = 3

# Define the GroupKFold cross-validation object
gkf = GroupKFold(n_splits=n_splits)


#random_state=42 -> fixed the seed value for the random number generator used by the algorithm
# number of decision trees = 100
model = RandomForestClassifier(n_estimators=100, random_state=42)


for i, (train_index, test_index) in enumerate(gkf.split(X, y, groups)):
    print(f"Fold {i}:")
    print(f"  Train: index={train_index}, group={groups[train_index].values}")
    print(f"  Test:  index={test_index}, group={groups[test_index].values}")
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y[train_index], y[test_index]

#split training and testing sets 70% 30%
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#fit the training data set to randomforest classifier
model.fit(X_train,y_train)


# Test
y_pred = model.predict(X_test)

# Assess the results
# compares each element of y_test with the corresponding element of y_pred
acc = accuracy_score(y_test, y_pred)

print("Accuracy score: {}".format(acc))
# Further analysis of the data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# We can check the confusion matrix or the classification report.

print(confusion_matrix(y_test, y_pred))


print(classification_report(y_test, y_pred,target_names={'Sleep stage W': 1,
                                                        'Sleep stage 1': 2,
                                                        'Sleep stage 2': 3,
                                                        'Sleep stage 3/4': 4,
                                                        'Sleep stage R': 5}))

#recall -> proportion of actual positive instances that are correctly identified as positive by the model
#F1 score -> balanced measure of precision and recall
#support -> shows the number of samples in the test set that belong to each class
#accuracy -> overall accuracy of the model on the test set
#macro avg -> calculates the average metric score across all classes, regardless of the number of samples in each class
#weighted avg -> average metric score across all classes, weighted by the number of samples in each class



# later on map to output to GUI using this
output = {
    '1': 'Awake',#change to output string that we want to show on GUI
    '2': 'Half asleep',
    '3': 'Fully asleep',
    '4': 'Fully asleep',
    '5': 'Fully asleep'
}


outputs = [output[value] for value in y_pred]

output_df = pd.DataFrame({'output': outputs})

output_df.to_csv('output.csv',index=False)
output_df.to_pickle('output.pkl')
