import sqlite3
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import DBSCAN
from datetime import datetime
import os

def run_clustering(eps_value, min_samples_value, success_threshold):
    # Record the start time
    start_time = datetime.now()

    # Connect to SQLite database and load data
    conn = sqlite3.connect('db.sqlite3')
    df = pd.read_sql_query("SELECT user_agent, client_ip, accept, accept_encoding, accept_language, connection, host, successful_login FROM myapp_requestlog", conn)
    conn.close()

    # Encode categorical variables
    label_encoder = LabelEncoder()
    original_values = {}
    for col in ['client_ip', 'accept', 'accept_encoding', 'accept_language', 'connection', 'host']:
        df[col] = label_encoder.fit_transform(df[col])
        original_values[col] = label_encoder.classes_

    # Combine the user_agent parts without encoding
    user_agents = df['user_agent'].str.split(';').apply(lambda x: ' '.join(x))
    df.drop(columns=['user_agent'], inplace=True)

    # Perform clustering using DBSCAN with user-defined parameters
    dbscan = DBSCAN(eps=eps_value, min_samples=min_samples_value)
    df['cluster'] = dbscan.fit_predict(df.drop(columns=['successful_login']))

    # Restore original categorical values
    for col in original_values:
        df[col] = df[col].map(lambda x: original_values[col][x])

    # Restore original user_agent values
    df['user_agent'] = user_agents

    # Reorder columns
    columns_order = ['cluster', 'user_agent', 'client_ip', 'accept', 'accept_encoding', 'accept_language', 'connection', 'host', 'successful_login']
    df = df[columns_order]

    # Count login attempts and successful attempts in each cluster
    cluster_counts = df.groupby('cluster').agg(Attempts=('successful_login', 'size'), Successful=('successful_login', 'sum'))

    # Calculate processing time
    processing_time = datetime.now() - start_time

    # Calculate flag based on the specified condition
    total_attempts = cluster_counts['Attempts']
    successful_attempts = cluster_counts['Successful']
    flag = (successful_attempts / total_attempts) < success_threshold
    flag.index = flag.index.astype(str)  # Ensure index is string for compatibility with GUI
    cluster_counts['Flag'] = flag.astype(int)

    # Generate log file
    log_folder = "scan_logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"clustered_records_{timestamp}.csv"

    df.to_csv(os.path.join(log_folder, log_filename), index=False)

    return cluster_counts, processing_time.total_seconds(), len(df), flag
