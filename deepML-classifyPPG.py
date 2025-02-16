"""
attempted to implement a deep learning (1D-CNN) ML model for classifying raw ppg data. max accuracy achieved <50%
~65% accuracy achieved with model trained using Random Forest and Feature Engineering, so proceed to classify data with 
traditional ML techniques. 
"""

import numpy as np
import pandas as pd
import glob
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from keras.optimizers import Adam

# Fixed maximum length for all waveforms
MAX_LENGTH = 1500  

# Function to load and preprocess data
def load_data(folder, label):
    file_paths = glob.glob(os.path.join(folder, '*.csv'))
    data_list = []
    labels = []

    for file in file_paths:
        df = pd.read_csv(file)
        
        if df.shape[0] == 0:
            print(f"Warning: {file} is empty, skipping.")
            continue
        
        waveform = df.iloc[:, 0].values.astype(np.float32)

        # Ensure all sequences are exactly MAX_LENGTH
        if len(waveform) < MAX_LENGTH:
            waveform = np.pad(waveform, (0, MAX_LENGTH - len(waveform)), mode='constant')
        elif len(waveform) > MAX_LENGTH:
            waveform = waveform[:MAX_LENGTH]
        
        data_list.append(waveform)
        labels.append(label)

    return data_list, labels

# Load data for each class
regular_data, regular_labels = load_data('regular', 0)
irregular_data, irregular_labels = load_data('irregular', 1)
afib_data, afib_labels = load_data('afib', 2)

# Combine data and labels
data = np.array(regular_data + irregular_data + afib_data)
labels = np.array(regular_labels + irregular_labels + afib_labels)

# Optionally, normalize each recording (e.g., min-max or standard scaling)
data = (data - np.mean(data, axis=1, keepdims=True)) / (np.std(data, axis=1, keepdims=True) + 1e-8)

# Add a channel dimension (needed for Conv1D input shape: (timesteps, channels))
data = np.expand_dims(data, axis=-1)

# Convert labels to one-hot encoding
def custom_to_categorical(labels, num_classes):
    """
    Converts a class vector (integers) to a binary class matrix (one-hot encoding).
    
    Parameters:
    - labels: array-like, shape (n_samples,)
    - num_classes: int, total number of categories
    
    Returns:
    - One-hot encoded numpy array, shape (n_samples, num_classes)
    """
    labels = np.array(labels, dtype=int)
    one_hot = np.zeros((labels.shape[0], num_classes))
    one_hot[np.arange(labels.shape[0]), labels] = 1
    return one_hot

labels = custom_to_categorical(labels, num_classes=3)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, stratify=labels, random_state=42)

if os.path.exists("ppg_model.h5"):
    print("🔄 Loading existing model...")
    model = load_model("ppg_model.h5")
    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
else:
    print("🆕 Creating new model...")
    # Define a simple Conv1D model
    model = Sequential([
        Conv1D(filters=64, kernel_size=5, activation='relu', input_shape=(1500, 1)),
        MaxPooling1D(pool_size=2),
        Conv1D(filters=128, kernel_size=5, activation='relu'),
        MaxPooling1D(pool_size=2),
        Conv1D(filters=256, kernel_size=5, activation='relu'),
        MaxPooling1D(pool_size=2),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.4),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(3, activation='softmax')
    ])
    
    # Compile model
    model.compile(optimizer=Adam(learning_rate=0.0003),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Print model summary
    model.summary()

# Train the model (even if loaded from file, you can continue training)
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Save the trained model
model.save("ppg_model.h5")
print("✅ Model saved successfully.")

# Evaluate the model
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"📊 Test Accuracy: {test_acc:.4f}")

print(f"Train Accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")
