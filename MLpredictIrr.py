import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Read the CSV file into a DataFrame
df = pd.read_csv('final_ppg_dataset.csv')

# Filter the DataFrame to only include rows where the 'label' column is 0
df_irregular = df[df['label'] == 1]

# Extract features and targets:
#   - Features: first 13 columns (e.g., bpm, ibi, sdnn, etc.)
#   - Targets: last 14 columns (from 'sinus' to 'extrasystoles_trig_episode')
# Note: Adjust column indices if necessary.
X = df_irregular.iloc[:, :13]
Y = df_irregular.iloc[:, 15:29]

# Replace inf values with NaN
X.replace([np.inf, -np.inf], np.nan, inplace=True)

# Option 1: Drop rows with NaN values
X_clean = X.dropna()

# If you drop rows from X, make sure to drop corresponding rows from Y:
Y_clean = Y.loc[X_clean.index]

# Split data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Use a MultiOutputRegressor with a RandomForestRegressor as the base estimator
model = MultiOutputRegressor(RandomForestRegressor(random_state=42))
model.fit(X_train, Y_train)

# Make predictions on the test set
Y_pred = model.predict(X_test)

# Evaluate the model using Mean Squared Error
#mse = mean_squared_error(Y_test, Y_pred)
#print("Mean Squared Error:", mse)

joblib.dump(model, 'irreg_model.pkl')