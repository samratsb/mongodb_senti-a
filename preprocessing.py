import csv
import pandas as pd
from pymongo import MongoClient

# Read the CSV file
rows = []
with open('training.1600000.processed.noemoticon.csv', encoding='latin-1') as file:
    reader = csv.reader(file)
    for row in reader:
        rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)

# Rename columns
df.columns = ['label', 'timestamp', 'date', 'query', 'username', 'text']
print(df.head())

# Drop 'timestamp' and 'date' columns
df = df.drop(columns=['timestamp', 'date','username'], errors='ignore')

# Check the DataFrame after dropping columns
print("DataFrame after dropping 'timestamp' and 'date' columns:")
print(df.head())

# Check if DataFrame is empty before inserting
if df.empty:
    print("No data available to insert into MongoDB.")
else:
    # Initialize MongoDB client
    client = MongoClient("mongodb+srv://mongodb:mongodb@cluster0.3shd3.mongodb.net/db1?retryWrites=true&w=majority")
    db = client.db1
    collection = db.collec1

    # Prepare the DataFrame for MongoDB
    data_to_insert = df.to_dict(orient='records')

    # Insert into MongoDB
    collection.insert_many(data_to_insert)
    print("Data has been exported to MongoDB.")
