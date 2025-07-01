import requests
import sqlite3

conn = sqlite3.connect("backend/cat_facts.db")
cursor = conn.cursor()
numFactsAdded = 0

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cat_facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fact TEXT UNIQUE,
        created_at DATE DEFAULT (DATE('now'))
    )
''')

while numFactsAdded < 5:
    response = requests.get("https://catfact.ninja/fact").json()
    fact = response["fact"]

    try:
        cursor.execute("INSERT INTO cat_facts (fact) VALUES (?)", (fact,))
        conn.commit()
        print("Added: " + fact)
        numFactsAdded += 1
    except sqlite3.IntegrityError:
        print("Skipped: " + fact)
        pass

conn.close()
