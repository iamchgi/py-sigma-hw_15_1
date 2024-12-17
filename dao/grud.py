import sqlite3


def init_db():
    global connection, cursor
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("bank.db")
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bank_currencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code INTEGER NOT NULL,
            count INTEGER NOT NULL,
            literal TEXT NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            delta REAL,
            delta100 REAL,
            date TEXT NOT NULL
        )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS bitochki (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                `date` TEXT NOT NULL,
                price REAL NOT NULL,
                `open` REAL NOT NULL,
                `high` REAL NOT NULL,
                low REAL NOT NULL,
                vol REAL NOT NULL,
                delta100 REAL NOT NULL
            )
            """)

    # Commit changes and close the connection
    connection.commit()
    # connection.close()
    return connection, cursor


def close_db():
    connection.commit()
    cursor.close()
    connection.close()


def get_all_metal():
    cursor.execute("SELECT * FROM bank_metals")
    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # connection.close()
    return rows

def get_all_bitochki():
    cursor.execute("SELECT * FROM bitochki")
    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # connection.close()
    return rows


def get_all_currency_price_by_name(name):
    cursor.execute("SELECT `price` FROM bank_currencies where name = '%s' order by id" % name)
    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # connection.close()
    return rows


def get_all_metal_price_by_name(name):
    cursor.execute("SELECT `price` FROM bank_metals where name = '%s' order by id" % name)
    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # connection.close()
    return rows

def get_all_bitochki_price():
    cursor.execute("SELECT `price` FROM bitochki")
    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # connection.close()
    return rows


def insert_one_metal(code, literal, name, price, delta, delta100, date):
    cursor.execute("INSERT INTO bank_metals (code,literal,name,price,delta,delta100,date) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (code, literal, name, price, delta, delta100, date))
    # connection.commit()
    # connection.close()
    return


def insert_one_currency(code, literal, count, name, price, delta, delta100, date):
    cursor.execute("INSERT INTO bank_currencies (code,literal,count,name,price,delta,delta100,date) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (code, literal, count, name, price, delta, delta100, date))
    # connection.commit()
    # connection.close()
    return

def insert_one_bitochek(date, price, open, high, low, vol, delta100):
    cursor.execute("INSERT INTO bitochki (`date`,`price`,`open`, `high`, `low`, `vol`, `delta100`) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (date, price, open, high, low, vol, delta100))
    # connection.commit()
    # connection.close()
    return


def clear_all_metals():
    cursor.execute("DELETE FROM bank_metals")
    connection.commit()


def clear_all_currency():
    cursor.execute("DELETE FROM bank_currencies")
    connection.commit()

def clear_all_bitki():
    cursor.execute("DELETE FROM bitochki")
    connection.commit()