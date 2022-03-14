import sqlite3

connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

with open('tables.sql', 'r') as file:
  for i, statement in enumerate(file.read().split(';')):
    print(i, statement)
    cursor.execute(statement)
  print('Success!')

# cursor.execute('''
# INSERT INTO person VALUES (1, 'Ola Nordmann', '2002-02-02')
# ''')

# cursor.execute("SELECT * FROM person")
# rows = cursor.fetchall()

# print("All rows in the table person:")
# print(rows)

connection.close()
