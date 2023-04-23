from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GroupKFold
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib


df = pd.read_pickle('data.pkl')



# Define the list of subject IDs to use for training and testing
subject_ids = ['SC4001E0', 'SC4011E0', 'SC4021E0', 'SC4031E0', 'SC4041E0', 'SC4051E0', 'SC4061E0', 'SC4071E0', 'SC4081E0']

# Filter your data to only include the selected subjects
filtered_data = df[df['subject_id'].isin(subject_ids)]


#X = data of selected features of each epochs (select first to third last column of datas of df)
X = filtered_data.iloc[:, 10:-2]
#y = sleep stage of each epochs (select second last column of df)
y = filtered_data.iloc[:, -2]

#Groups = subject_id
groups = filtered_data.iloc[:, -1]

# 3 folds
#since we have 10 subjects using 3 folds split train n test sets into about 70% 30%
n_splits = 3

# Define the GroupKFold cross-validation object
gkf = GroupKFold(n_splits=n_splits)


for i, (train_index, test_index) in enumerate(gkf.split(X, y, groups)):
    print(f"Fold {i}:")
    print(f"  Train: index={train_index}, group={groups[train_index].values}")
    print(f"  Test:  index={test_index}, group={groups[test_index].values}")
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y[train_index], y[test_index]


#random_state=42 -> fixed the seed value for the random number generator used by the algorithm
# number of decision trees = 100
model = RandomForestClassifier(n_estimators=100, random_state=42)


#fit the training data set to randomforest classifier
model.fit(X_train.values,y_train)


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


# Get the feature importances from your Random Forest classifier
importances = model.feature_importances_

# Sort the features by importance
indices = np.argsort(importances)[::-1]

print(X_train.columns[indices])
# Plot the feature importances
plt.bar(range(X_train.shape[1]), importances[indices])
plt.xticks(range(X_train.shape[1]), X_train.columns[indices], rotation=90)
plt.show()


ref_col = list(X.columns)

print(ref_col)

target = "sleep_stage"
print(target)

#export model
joblib.dump(value=[model, ref_col, target], filename='model.pkl')