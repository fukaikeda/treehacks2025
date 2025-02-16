import os
import pandas as pd
import numpy as np
import joblib
import heartpy as hp
import scipy.signal as signal

# Define paths
unclassified_folder = "unclassified"
model_path = "classify_model.pkl"
output_csv = "classified_ppg_results.csv"

# Load the trained classifier model
classifier_model = joblib.load(model_path)

# Define sampling rate
sampling_rate = 25  # Hz
window_size = sampling_rate * 60  # 1-minute segment

# List to store extracted feature data
features_list = []
filenames_list = []  # Store filenames for tracking

# Function to preprocess and extract features from PPG data
def extract_features_from_ppg(ppg_file):
    try:
        # Load raw PPG data
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

# Process all unclassified PPG files
results = []
for filename in sorted(os.listdir(unclassified_folder)):  # Sort to maintain order
    if filename.endswith(".csv"):
        file_path = os.path.join(unclassified_folder, filename)
        features = extract_features_from_ppg(file_path)

        if features:
            # Convert features to numpy array for model input
            features_array = np.array(list(features.values())).reshape(1, -1)
            
            # Predict category (0 = Regular, 1 = Irregular, 2 = AFib)
            prediction = classifier_model.predict(features_array)[0]  # Single prediction
            
            # Store result
            results.append({"Filename": filename, "Prediction": prediction})

# Save results to CSV
df_results = pd.DataFrame(results)
df_results.to_csv(output_csv, index=False)

print(f"Classification complete. Results saved to {output_csv}.")
