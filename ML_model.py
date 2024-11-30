import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
Data = pd.read_csv('data.csv')

# Select all columns except the last one as features (x), and the last column as the target (y)
x = Data.iloc[:, :-1]
y = Data.iloc[:, -1] 

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=42)

# Initialize the RandomForestClassifier
clf2 = RandomForestClassifier(n_estimators=100, random_state=42)
clf2.fit(x_train, y_train)

# Predict the test set
y_pred = clf2.predict(x_test)

# Print the accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save the trained model to a file for later use
import pickle
with open('model.pkl', 'wb') as file:
    pickle.dump(clf2, file)
