import os
import pandas as pd
import numpy as np
import joblib
import heartpy as hp
import scipy.signal as signal

# Define paths
unclassified_folder = "unclassified"
classified_results_csv = "classified_ppg_results.csv"
output_csv = "cardiac_risk_predictions.csv"

# Load classification results
classified_df = pd.read_csv(classified_results_csv)

# Load cardiac risk models
reg_model = joblib.load("reg_model.pkl")  # For regular (0)
irreg_model = joblib.load("irreg_model.pkl")  # For irregular (1)
afib_model = joblib.load("afib_model.pkl")  # For AFib (2)

# Define sampling rate
sampling_rate = 25  # Hz
window_size = sampling_rate * 60  # 1-minute segment

# Function to extract features from PPG files
def extract_features_from_ppg(ppg_file):
    try:
        # Load PPG data
        df = pd.read_csv(ppg_file)
        
        # Extract PPG signal
        ppg_signal = df["green"].values  # Use "red" or "IR" if needed

        # Ensure enough data for a full segment
        if len(ppg_signal) < window_size:
            print(f"Skipping {ppg_file}: insufficient data")
            return None

        # Detrend signal
        ppg_signal = signal.detrend(ppg_signal)

        # Apply bandpass filter (0.5 - 4 Hz)
        b, a = signal.butter(3, [0.5 / (sampling_rate / 2), 4 / (sampling_rate / 2)], btype='band')
        filtered_signal = signal.filtfilt(b, a, ppg_signal)

        # Normalize signal
        filtered_signal = (filtered_signal - np.mean(filtered_signal)) / np.std(filtered_signal)

        # Process with HeartPy
        wd, m = hp.process(filtered_signal, sampling_rate, bpmmin=30, bpmmax=220)

        return m  # Extracted features

    except hp.exceptions.BadSignalWarning:
        print(f"Skipping {ppg_file}: Bad signal detected")
        return None
    except Exception as e:
        print(f"Error processing {ppg_file}: {e}")
        return None

# Process and make cardiac risk predictions
results = []
for index, row in classified_df.iterrows():
    filename = row["Filename"]
    classification = row["Prediction"]
    
    file_path = os.path.join(unclassified_folder, filename)
    
    # Extract features
    features = extract_features_from_ppg(file_path)
    
    if features:
        # Convert features to numpy array for model input
        features_array = np.array(list(features.values())).reshape(1, -1)

        # Select the appropriate model
        if classification == 0:
            risk_prediction = reg_model.predict(features_array)[0]
        elif classification == 1:
            risk_prediction = irreg_model.predict(features_array)[0]
        elif classification == 2:
            risk_prediction = afib_model.predict(features_array)[0]
        else:
            print(f"Invalid classification for {filename}")
            continue
        
        # Store results
        results.append({
            "Filename": filename,
            "Classification": classification,
            "Cardiac Risk Score": risk_prediction
        })

# Save results to CSV
df_results = pd.DataFrame(results)
df_results.to_csv(output_csv, index=False)

print(f"Cardiac risk predictions saved to {output_csv}.")
