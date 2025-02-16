import os
import pandas as pd
import heartpy as hp
import numpy as np
import scipy.signal as signal

# Set your folder paths
regular_folder = "regular"
irregular_folder = "irregular"
afib_folder = "afib"

def load_ppg_data(folder, label):
    """Loads all CSVs from a folder, adds a label and filename column, and concatenates them."""
    data_list = []
    filenames = []
    
    for file in sorted(os.listdir(folder)):  # Sort to maintain order consistency
        if file.endswith(".csv"):
            file_path = os.path.join(folder, file)
            df = pd.read_csv(file_path)
            df["label"] = label  # 0 = Regular, 1 = Irregular, 2 = afib
            df["filename"] = file  # Store the filename
            
            data_list.append(df)
    
    return pd.concat(data_list, ignore_index=True)

# Load all categories
regular_data = load_ppg_data(regular_folder, label=0)
irregular_data = load_ppg_data(irregular_folder, label=1)
afib_data = load_ppg_data(afib_folder, label=2)

# Combine into one dataset
full_ppg_data = pd.concat([regular_data, irregular_data, afib_data], ignore_index=True)

# List to store extracted feature data
features_list = []
filenames_list = []  # Store filenames corresponding to each segment

# Define sampling rate
sampling_rate = 25  # Hz
window_size = sampling_rate * 60  # Assuming 1-minute segments

# Process each time-series segment
for start in range(0, len(full_ppg_data), window_size):
    segment = full_ppg_data.iloc[start:start + window_size]
    
    if len(segment) < window_size:
        continue  # Skip incomplete segments
    
    try:
        # Extract PPG signal as an array
        ppg_signal = segment["green"].values  # Use "red" or "IR" if needed

        # Detrend signal
        ppg_signal = signal.detrend(ppg_signal)

        # Apply bandpass filter (0.5 - 4 Hz for heart rate detection)
        b, a = signal.butter(3, [0.5 / (sampling_rate / 2), 4 / (sampling_rate / 2)], btype='band')
        filtered_signal = signal.filtfilt(b, a, ppg_signal)

        # Normalize signal
        filtered_signal = (filtered_signal - np.mean(filtered_signal)) / np.std(filtered_signal)

        # Process with HeartPy
        wd, m = hp.process(filtered_signal, sampling_rate, bpmmin=30, bpmmax=220)

        # Add label and filename
        features = m
        features["label"] = segment["label"].iloc[0]  # Use first label for this segment
        filename = segment["filename"].iloc[0]  # Get filename for this segment

        # Append to lists
        features_list.append(features)
        filenames_list.append(filename)

    except hp.exceptions.BadSignalWarning as e:
        #print(f"Skipping segment {start} due to bad signal:", e)
        continue

# Convert to DataFrame
features_df = pd.DataFrame(features_list)
features_df["filename"] = filenames_list  # Add filename column

# Save to CSV for ML training
features_df.to_csv("ppg_extracted_features.csv", index=False)

# Display results
print("Extracted features shape:", features_df.shape)
print(features_df.head())
