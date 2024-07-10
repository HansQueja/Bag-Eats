import sqlite3

# Connect to a new (or existing) database file
conn = sqlite3.connect('users.db')

# Create a cursor object
cursor = conn.cursor()

# Example: Create a new table (optional)
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    age TINYINT(3) NOT NULL,
    height DECIMAL(3, 2) NOT NULL,
    weight DECIMAL(3, 2) NOT NULL,
    bmi DECIMAL(2, 2) NOT NULL,
    hash VARCHAR(128) NOT NULL
);
''')

# Commit the changes (if any) and close the connection
conn.commit()
conn.close()

print("Database created successfully.")
