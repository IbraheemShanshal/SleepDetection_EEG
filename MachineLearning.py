from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

import pandas as pd

df = pd.read_pickle('data.pkl')

#X = data of selected features of each epochs (select first to third last column of datas of df)
X = df.iloc[:, :-2]
#y = sleep stage of each epochs (select second last column of df)
y = df.iloc[:, -2]


#random_state=42 -> fixed the seed value for the random number generator used by the algorithm
# number of decision trees = 100
model = RandomForestClassifier(n_estimators=100, random_state=42)

#split training and testing sets 70% 30%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

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

#print(X_test)
#print(y_pred)

# later on map to output to GUI using this
output = {
    1: 'awake',#change to output string that we want to show on GUI
    2: 'Sleep stage 1',
    3: 'Sleep stage 2',
    4: 'Sleep stage 3/4',
    5: 'Sleep stage R'
}


