import sqlite3


def ask(questions, types=None):
	try:
		if types == None:
			return [input(f'{q}: ') for q in questions]
		else:
			return [types[i](input(f'<{types[i].__name__}> {q}: ')) for i, q in enumerate(questions)]
	except Exception as e:
		print(f'ERROR - {e}')

def fill_database(cursor):
  insert_kaffe(cursor, ['Vinterkaffe', '20.01.2022', 'lysbrent', 'En velsmakende og kompleks kaffe for mørketiden', 600, 'Jacobsen & Svart', 1])
  insert_kaffebrenneri(cursor, ['Jacobsen & Svart'])
  insert_kaffeparti(cursor, [1, 2021, 72, 'Bærtørket'])
  insert_kaffebonne([])

def build_tables(cursor):
  with open('db2/src/tables.sql', 'r') as file:
    for i, statement in enumerate(file.read().split(';')):
      print(i, statement)
      cursor.execute(statement)
    print('\nSuccessfully build tables!\n')


def insert_kaffe(cursor, attributter):
  cursor.execute('''
  INSERT INTO Kaffe
    (Navn, Dato, Brenningsgrad, Beskrivelse, Kilopris, KaffebrenneriNavn, KaffepartiID) 
  VALUES (?, ?, ?, ?, ?, ?, ?)
  ''', attributter)


def insert_kaffebrenneri(cursor, attributter):
  cursor.execute('''
  INSERT INTO Kaffebrenneri
    (Navn)
  VALUES
    (?)
  ''', attributter)


def get_kaffe(cursor):
  cursor.execute('''
  SELECT * FROM Kaffe
  ''')
  return cursor.fetchall()


def insert_kaffeparti(cursor, attributter):
  cursor.execute('''
  INSERT INTO Kaffeparti
    (ID, Innhøstingsår, Kilopris, KaffegårdNavn, ForedlingsmetodeNavn)
  VALUES
    (?, ?, ?, ?)
  ''', attributter)
  
def insert_kaffebonne(cursor, attributter):
  cursor.execute('''
  INSERT INTO Kaffebønne
    ('Art')
  VALUES
    (?)
  ''', attributter)

def main():
  connection = sqlite3.connect(':memory:')
  cursor = connection.cursor()

  build_tables(cursor)
  fill_database(cursor)

  while True:
    command = input('Hva vil du gjøre?')
    if command == 'kaffe':
      attributes = ask([
        'Navn?', 'Dato?', 'Brenningsgrad?', 'Beskrivelse?', 'Kilopris?', 'KaffebrenneriNavn?', 'KaffepartiID?'], [str, str, str, str, float, str, str])
      print('Dine valg', attributes)
      insert_kaffe(cursor, attributes)
    elif command == 'vis meg':
      print(get_kaffe(cursor))
    elif command == 'ferdig':
      break

  connection.close()


if __name__ == '__main__':
  main()


# cursor.execute('''
# INSERT INTO person VALUES (1, 'Ola Nordmann', '2002-02-02')
# ''')

# cursor.execute('SELECT * FROM person')
# rows = cursor.fetchall()

# print('All rows in the table person:')
# print(rows)

