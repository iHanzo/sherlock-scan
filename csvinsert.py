import csv
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Open and read CSV file
with open('records.csv', 'r', newline='') as file:
    csv_reader = csv.DictReader(file, quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        # Filter out rows with missing values
        if None in row.values():
            print("Skipping row with missing values:", row)
            continue
        
        # Prepare column names and values
        columns = ', '.join(str(key) for key in row.keys())
        placeholders = ', '.join('?' * len(row))
        values = tuple(row.values())
        
        # Insert data into the table
        cursor.execute(f'INSERT INTO myapp_requestlog ({columns}) VALUES ({placeholders})', values)

# Commit changes and close connection
conn.commit()
conn.close()

