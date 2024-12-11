import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect("currency.db")
# Create a cursor object to interact with the database
cursor = connection.cursor()
# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_metals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code INTEGER NOT NULL,
    literal TEXT NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    delta REAL,
    delta100 REAL,
    date TEXT NOT NULL
)
""")
# Commit changes and close the connection
connection.commit()
# connection.close()


def get_all_metal():
    cursor.execute("SELECT * FROM bank_metals")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # connection.close()
    return rows


def insert_one_metal(code, literal, name, price, delta, delta100, date):
    cursor.execute("INSERT INTO bank_metals (code,literal,name,price,delta,delta100,date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (code, literal, name, price, delta, delta100, date))
    connection.commit()
    # connection.close()
    return
