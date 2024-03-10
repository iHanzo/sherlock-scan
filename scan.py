import sqlite3
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import DBSCAN

# Connect to SQLite database
conn = sqlite3.connect('db.sqlite3')

# Load data from SQLite database
df = pd.read_sql_query("SELECT user_agent, client_ip, accept, accept_encoding, accept_language, connection, host, successful_login FROM myapp_requestlog", conn)

# Close the database connection
conn.close()

# Impute missing values using the most frequent value
imputer = SimpleImputer(strategy='most_frequent')
df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Encode categorical variables
label_encoder = LabelEncoder()
for col in ['user_agent', 'client_ip', 'accept', 'accept_encoding', 'accept_language', 'connection', 'host']:
    df[col] = label_encoder.fit_transform(df[col])

# Perform clustering using DBSCAN
dbscan = DBSCAN(eps=1, min_samples=3)
df['cluster'] = dbscan.fit_predict(df.drop(columns=['successful_login']))

# Count the number of failed and successful login attempts in each cluster
cluster_counts = df.groupby(['cluster', 'successful_login']).size().unstack(fill_value=0)

# Print cluster information
print(cluster_counts)

