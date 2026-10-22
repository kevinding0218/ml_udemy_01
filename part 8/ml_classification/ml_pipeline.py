# numpy: a library for working with numbers and arrays (lists of data)
import numpy as np
# pandas: a library for loading and working with tables of data (like Excel)
import pandas as pd

# Read a CSV file (spreadsheet) into a "DataFrame" (a table with rows and columns)
training_data = pd.read_csv('storepurchasedata.csv')

# Print summary statistics about the data (min, max, average, etc.) — good for understanding what's inside
training_data.describe()

# X = the input "features" (all columns EXCEPT the last one) — e.g., age, salary
# iloc[:, :-1] means: take ALL rows (:), and all columns except the last (:-1)
# .values converts the table into a plain array of numbers
X = training_data.iloc[:, :-1].values

# y = the "label" or answer we want to predict (the LAST column) — e.g., "bought" or "didn't buy"
y = training_data.iloc[:,-1].values

# Import the function that splits data into training and testing sets
from sklearn.model_selection import train_test_split

# Split: 80% of the data is used to TRAIN the model, 20% is kept aside to TEST it
# random_state=0 makes the split the same every time you run the code
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.20, random_state=0)

# Import the tool that "scales" (normalizes) the numbers so they're all on a similar range
from sklearn.preprocessing import StandardScaler

# Create a scaler object
sc = StandardScaler()

# fit_transform: learn the average and range from X_train, then rescale every value in X_train.
# X_train is REPLACED (overwritten) because the raw version is no longer useful after scaling.
#
# WHY do we need to scale at all?
# -----------------------------------------------
# KNN finds "nearest neighbors" by computing DISTANCE between two data points.
# For N columns: distance = sqrt((a1-b1)² + (a2-b2)² + ... + (aN-bN)²)
#   → each column's gap is squared, then all squared gaps are ADDED together
#   → e.g. total of 4,000,900 = age-gap² + salary-gap² = 900 + 4,000,000
#   → a column with huge raw numbers produces a huge squared gap and drowns out the rest
#
# REAL-WORLD EXAMPLE (2 columns: age and salary):
#   Person A: age=30, salary=50000
#   Person B: age=32, salary=90000
#   (a 2-year age gap and a $40k salary gap — both are real, meaningful differences)
#
#   RAW distance = sqrt( (32-30)²  +  (90000-50000)²  )
#                = sqrt(    4      +  1,600,000,000    )
#                ≈ 40,000
#
#   Age's share:    4 / 1,600,000,004 ≈ 0.000%  ← completely invisible
#   Salary's share: 1,600,000,000 / 1,600,000,004 ≈ 100%  ← salary is everything
#
#   The 0% for age is NOT because age is unimportant — it's because salary
#   is measured in units of thousands while age is in tens. The unit size,
#   not real importance, is controlling the result.
#
# IS THERE A TARGET SPLIT (50/50, or "at least 10% each")?
#   No fixed target. The goal is not equal shares — it's that each column's
#   share reflects genuine data differences, not fake distortion from unit sizes.
#   After scaling: if age still takes 80% for a specific pair of people, that
#   just means those two people genuinely differ a lot on age — which is fine.
#   The problem is 99.98% caused purely by salary being in bigger units.
#
# AFTER SCALING — each column is converted to the same unit (roughly -3 to +3):
#   A 2-year age gap across a dataset where ages span 20–60 → small scaled gap (~0.2)
#   A $40k salary gap across a dataset where salaries span $15k–$150k → larger scaled gap (~1.1)
#   Both now live on the same ruler. Salary still contributes more for this pair
#   (because $40k IS a bigger real gap than 2 years), but age is no longer invisible.
#   The split now reflects real differences — not just which column has bigger numbers.
#
# WHAT DOES THE DISTANCE NUMBER MEAN?
#   The absolute value (40,000 or 1.4) has no meaning on its own.
#   KNN never asks "is 40,000 too far?" — it just RANKS all data points by
#   distance and picks the 5 smallest. It's always a relative comparison, never a threshold.
X_train = sc.fit_transform(X_train)

# transform: scale the TEST data using the SAME averages learned from training (do NOT re-learn)
X_test = sc.transform(X_test)

# Import the K-Nearest Neighbors classifier algorithm
from sklearn.neighbors import KNeighborsClassifier

# Create the classifier:
# - n_neighbors=5: when predicting, look at the 5 closest data points and take a majority vote
# - metric='minkowski' with p=2: use Euclidean distance (straight-line distance) to measure "closeness"
classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)

# Train the model: show it the training inputs (X_train) and the correct answers (y_train)
# The model learns patterns from this data
classifier.fit(X_train, y_train)

# Use the trained model to predict labels for the test data
# y_pred = the model's guesses for each row in X_test
y_pred = classifier.predict(X_test)

# Get the probability (0.0 to 1.0) that each test sample belongs to class 1
# [:,1] picks the probability for class "1" (the positive class)
y_prob = classifier.predict_proba(X_test)[:,1]

# Import the confusion matrix tool — shows how many predictions were correct/wrong
from sklearn.metrics import confusion_matrix

# Build the confusion matrix: compares actual answers (y_test) vs model's guesses (y_pred)
# Rows = actual class, Columns = predicted class
cm = confusion_matrix(y_test, y_pred)

# Import accuracy score — simplest metric: what % of predictions were correct
from sklearn.metrics import accuracy_score

# Print the accuracy (e.g., 0.93 means 93% of predictions were correct)
print(accuracy_score(y_test, y_pred))

# Import classification report — gives detailed stats: precision, recall, F1-score per class
from sklearn.metrics import classification_report

# Print the full report showing performance for each class
print(classification_report(y_test, y_pred))

# Predict for a NEW, never-seen person: age=40, salary=20000
# sc.transform(...) scales the new input the same way training data was scaled
new_prediction = classifier.predict(sc.transform(np.array([[40, 20000]])))

# Get the probability that this person belongs to class 1
new_prediction_proba = classifier.predict_proba(sc.transform(np.array([[40, 20000]])))[:,1]

# Predict for another new person: age=42, salary=50000
new_pred = classifier.predict(sc.transform(np.array([[42, 50000]])))

# Get the probability for this second person
new_pred_proba = classifier.predict_proba(sc.transform(np.array([[42, 50000]])))[:,1]


# --- Save the trained model and scaler to disk so you can reuse them later ---

# pickle: a library for saving Python objects to files
import pickle

# File name where the classifier model will be saved
model_file = "classifier.pickle"

# Save the classifier to a file
# open(model_file, 'wb') opens the file in "write binary" mode
# pickle.dump(...) writes the object into that file
pickle.dump(classifier, open(model_file, 'wb'))

# File name where the scaler will be saved
scaler_file = "sc.pickle"

# Save the scaler to a file — you need this later to scale new inputs the same way
pickle.dump(sc, open(scaler_file, 'wb'))
