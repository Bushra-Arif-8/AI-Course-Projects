import pandas as pd
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import json

# Load the dataset
file_path = 'dataset of friendship compatibility.csv'
df = pd.read_csv(file_path)

# Drop unwanted columns if they exist
drop_columns = ['Full Name', 'Gender']
df_cleaned = df.drop(columns=[col for col in drop_columns if col in df.columns], errors='ignore')

# Select only numeric columns for processing
numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
df_numeric = df_cleaned[numeric_cols]

# Handle missing values if any
if df_numeric.isna().sum().sum() > 0:
    df_numeric.fillna(df_numeric.mean(), inplace=True)

# Scale the numeric data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df_numeric)

# Determine the optimal number of clusters using the elbow method (optional)
inertia = []
K_range = range(2, 11)
for k in K_range:
    kmeans_test = KMeans(n_clusters=k, random_state=42)
    kmeans_test.fit(scaled_data)
    inertia.append(kmeans_test.inertia_)

# You can plot inertia vs K to find elbow or set fixed
optimal_k = 5  # Adjust based on elbow plot or domain knowledge

# Fit final KMeans
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(scaled_data)

# Assign clusters back to original dataframe
df['Cluster'] = kmeans.labels_

# Save clustered data
df.to_csv('clustered_friends.csv', index=False)

# Save model and scaler for later use
joblib.dump(kmeans, 'kmeans_model.joblib')
joblib.dump(scaler, 'scaler.joblib')

# Save the list of features expected by the UI (cleaned column names)
expected_features = [col.strip().lower() for col in numeric_cols]
with open('expected_features.json', 'w') as f:
    json.dump(expected_features, f)

print("Model training and data clustering completed successfully!")