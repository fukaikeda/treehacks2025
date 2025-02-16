import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the extracted features CSV
data = pd.read_csv("ppg_extracted_features.csv")

# Convert 'sdsd' column to numeric (force non-numeric to NaN)
data["sdsd"] = pd.to_numeric(data["sdsd"], errors='coerce')

# Drop non-numeric columns
if 'filename' in data.columns:
    data = data.drop(columns=['filename'])

# Separate features and target
X = data.drop(columns=["label"])
y = data["label"]

# Convert all columns to numeric, forcing non-convertible values to NaN
X = X.apply(pd.to_numeric, errors='coerce')

# Replace infinite values with NaN
X.replace([np.inf, -np.inf], np.nan, inplace=True)

# Impute missing values with column medians
X.fillna(X.median(), inplace=True)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets (90% train, 10% test)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.1, random_state=42, stratify=y
)

# Initialize and train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print(classification_report(y_test, y_pred))

# Save the trained model
joblib.dump(model, 'classify_model.pkl')
