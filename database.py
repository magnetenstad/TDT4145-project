import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS person
(id INTEGER PRIMARY KEY, name TEXT, birthday TEXT)
''')

cursor.execute('''
INSERT INTO person VALUES (1, 'Ola Nordmann', '2002-02-02')
''')

cursor.execute("SELECT * FROM person")
rows = cursor.fetchall()
print("All rows in the table person:")
print(rows)

connection.close()
