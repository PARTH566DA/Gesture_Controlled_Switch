import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
Data = pd.read_csv('a.csv')

# Select all columns except the last one as features (x), and the last column as the target (y)
x = Data.iloc[:, :-1]
y = Data.iloc[:, -1]  # Select the last column for all rows

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

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


# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score
# import pickle

# # Load the dataset
# Data = pd.read_csv('test.csv')

# # Select all columns except the last one as features (x), and the last column as the target (y)
# x = Data.iloc[:, :-1]
# y = Data.iloc[:, -1]  # Select the last column for all rows

# # Split the data into training and testing sets
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# # Initialize the RandomForestClassifier
# clf2 = RandomForestClassifier(n_estimators=100, random_state=42)
# clf2.fit(x_train, y_train)

# # Set a probability threshold to detect unseen movements
# threshold = 0.98  # You can adjust this value based on experimentation

# # Predict the test set probabilities
# y_proba = clf2.predict_proba(x_test)

# # Get the predicted class and the highest probability for each prediction
# y_pred = clf2.predict(x_test)
# max_prob = np.max(y_proba, axis=1)

# # Set the prediction to 0 if the highest probability is below the threshold (i.e., unseen movement)
# final_predictions = np.where(max_prob >= threshold, y_pred, 0)

# # Print the accuracy for the valid class predictions (ignoring "unknown" cases)
# valid_predictions = final_predictions[final_predictions != 0]
# valid_y_test = y_test[final_predictions != 0]
# if len(valid_predictions) > 0:
#     accuracy = accuracy_score(valid_y_test, valid_predictions)
#     print("Accuracy for valid predictions:", accuracy)
# else:
#     print("No valid predictions were made.")

# # Save the trained model to a file for later use
# with open('model.pkl', 'wb') as file:
#     pickle.dump(clf2, file)

# print("Model has been saved to 'model.pkl'")
