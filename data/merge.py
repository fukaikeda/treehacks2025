import pandas as pd

# Load PPG extracted features
ppg_features = pd.read_csv("ppg_extracted_features.csv")

#### PREPROCESS EXTRACTED DATA ####
# Step 1: Identify and remove rows with all null or corrupted values
ppg_features_cleaned = ppg_features.dropna(how='all')  # Drops rows where ALL values are NaN

# Step 2: Drop rows with too many missing values 
threshold = int(ppg_features.shape[1] * 0.69) 
ppg_features_cleaned = ppg_features_cleaned.dropna(thresh=threshold)

# Step 3: Fill remaining missing values with median (EXCLUDING the filename column)
numeric_cols = ppg_features_cleaned.select_dtypes(include=['number']).columns  # Only numeric columns
ppg_features_cleaned[numeric_cols] = ppg_features_cleaned[numeric_cols].fillna(ppg_features_cleaned[numeric_cols].median())

# Step 4: Ensure correct data types (convert all but `filename` to float)
for col in numeric_cols:
    ppg_features_cleaned[col] = pd.to_numeric(ppg_features_cleaned[col], errors='coerce')

# Display summary
#print("Cleaned dataset shape:", ppg_features_cleaned.shape)
#print(ppg_features_cleaned.head())

# Load Metadata
metadata = pd.read_csv("metadata.csv")

# Merge on the 'filename' column
merged_df = ppg_features_cleaned.merge(metadata, on="filename", how="inner")

# Save merged dataset
merged_df.to_csv("final_ppg_dataset.csv", index=False)

# Display summary
print("Merged dataset shape:", merged_df.shape)
print(merged_df.head())