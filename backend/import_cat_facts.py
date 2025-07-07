import requests
import sqlite3

# connects/creates cat_facts database
conn = sqlite3.connect("./cat_facts.db")
cursor = conn.cursor()
numFactsAdded = 0

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cat_facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fact TEXT UNIQUE,
        created_at DATE DEFAULT (DATE('now'))
    )
''')

# fetches and adds 5 unique cat facts into database
while numFactsAdded < 5:
    response = requests.get("https://catfact.ninja/fact").json()
    fact = response["fact"]

    try:
        cursor.execute("INSERT INTO cat_facts (fact) VALUES (?)", (fact,))
        conn.commit()
        print("Added: " + fact)
        numFactsAdded += 1
    except Exception as e:
        print("Fact not added: " + fact)
        pass

conn.close()
