import sqlite3
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import DBSCAN
from datetime import datetime
import os

# Record the start time
start_time = datetime.now()

# Connect to SQLite database and load data
conn = sqlite3.connect('db.sqlite3')
df = pd.read_sql_query("SELECT user_agent, client_ip, accept, accept_encoding, accept_language, connection, host, successful_login FROM myapp_requestlog", conn)
conn.close()

# Impute missing values
imputer = SimpleImputer(strategy='most_frequent')
df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Encode categorical variables
label_encoder = LabelEncoder()
original_values = {}
for col in ['user_agent', 'client_ip', 'accept', 'accept_encoding', 'accept_language', 'connection', 'host']:
    df[col] = label_encoder.fit_transform(df[col])
    original_values[col] = label_encoder.classes_

# Perform clustering using DBSCAN
dbscan = DBSCAN(eps=1, min_samples=3)
df['cluster'] = dbscan.fit_predict(df.drop(columns=['successful_login']))

# Convert numerical labels back to original string values
for col in ['user_agent', 'client_ip', 'accept', 'accept_encoding', 'accept_language', 'connection', 'host']:
    df[col] = df[col].map(lambda x: original_values[col][x])

# Count login attempts in each cluster
cluster_counts = df.groupby(['cluster', 'successful_login']).size().unstack(fill_value=0)

# Print cluster information with improved formatting
print("Cluster\tAttempts\tSuccess")
for index, row in cluster_counts.iterrows():
    print(f"{index}\t{row[0]}\t\t{row[1]}")

# Calculate and print processing time, rows processed, and processing rate
processing_time = datetime.now() - start_time
rows_processed = len(df)
processing_time_seconds = processing_time.total_seconds()
rows_per_sec = rows_processed / processing_time_seconds

print(f"\nDuration (seconds): {processing_time_seconds:.2f}")
print(f"Rows Processed: {rows_processed}")
print(f"Processing Rate (Rows/Second): {rows_per_sec:.2f}")

# Create a folder named "scan_logs" if it doesn't exist and export clustered data to CSV file with timestamp
if not os.path.exists('scan_logs'):
    os.makedirs('scan_logs')

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
csv_file_path = os.path.join('scan_logs', f'clustered_data_{timestamp}.csv')
df.to_csv(csv_file_path, index=False)
print(f"\nClustered data saved to {csv_file_path}")

