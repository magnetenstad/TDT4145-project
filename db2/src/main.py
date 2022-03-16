import sqlite3

### Globals ###

cursor = None

### Utils ###

def ask(questions, types=None):
	try:
		if types == None:
			return [input(f'{q}: ') for q in questions]
		else:
			return [types[i](input(f'<{types[i].__name__}> {q}: ')) for i, q in enumerate(questions)]
	except Exception as e:
		print(f'ERROR - {e}')

### Database initialization ###

def build_tables():
  with open('db2/src/tables.sql', 'r') as file:
    for i, statement in enumerate(file.read().split(';')):
      try:
        cursor.execute(statement)
      except Exception as e:
        print(f'[ERROR] in create table {i}: {statement}')
        print(str(e))
    print('\nSuccessfully build tables!\n')

def fill_database():
  insert_kaffebonne(['Coffea arabica'])
  insert_kaffebonne(['Coffea liberica'])
  insert_kaffebonne(['Coffea robusta'])
  insert_foredlingsmetode(['vasket', None])
  insert_foredlingsmetode(['bærtørket', None])
  
  # Brukerhistorie 1:

  insert_kaffegard(['Nombre Dios', 1500, 'El Salvador', 'Santa Ana'])
  insert_kaffeparti([1, 2021, 72, 'Nombre Dios', 'bærtørket'])
  insert_kaffe(['Vinterkaffe', '20.01.2022', 'lysbrent', 'En velsmakende og kompleks kaffe for mørketiden', 600, 'Jacobsen & Svart', 1])
  insert_kaffebrenneri(['Jacobsen & Svart'])
  insert_kaffebonne(['Coffea arabica'])
  insert_bruker(['ola@nordmann.no', 'Passord', 'Ola Nordmann', 'Norge'])
  insert_kaffesmaking(['ola@nordmann.no', 'Jacobsen & Svart', 'Vinterkaffe', 'Wow - en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!', 10, '20.1.2022'])
  insert_dyrketAv(['Coffea arabica', 'Nombre de Dios'])
  insert_partiBestarAv(['Coffea arabica', 1])

  # Brukerhistorie 4:

  insert_kaffegard(['Akageragården', 1990, 'Rwanda', 'Akagera'])
  insert_kaffeparti([2, 2021, 72, 'Akageragården', 'bærtørket'])
  insert_kaffe(['Sommerkaffe', '10.02.2022', 'mørkbrent', 'God om sommeren.', 400, 'Jacobsen & Svart', 2])

  insert_kaffegard(['Bogotagården', 1990, 'Columbia', 'Bogota'])
  insert_kaffeparti([3, 2019, 10, 'Bogotagården', 'vasket'])
  insert_kaffe(['Bogotakaffe', '10.02.2020', 'mørkbrent', 'God i Bogota.', 300, 'Jacobsen & Svart', 2])


def insert_kaffe(attributes):
  cursor.execute('''
  INSERT INTO Kaffe
    (Navn, Dato, Brenningsgrad, Beskrivelse, Kilopris, KaffebrenneriNavn, KaffepartiID) 
  VALUES (?, ?, ?, ?, ?, ?, ?)
  ''', (attributes))

def insert_kaffebrenneri(attributes):
  cursor.execute('''
  INSERT INTO Kaffebrenneri
    (Navn)
  VALUES
    (?)
  ''', attributes)

def insert_kaffeparti(attributes):
  cursor.execute('''
  INSERT INTO Kaffeparti
    (ID, Innhøstingsår, Kilopris, KaffegårdNavn, ForedlingsmetodeNavn)
  VALUES
    (?, ?, ?, ?, ?)
  ''', attributes)
  
def insert_kaffebonne(attributes):
  cursor.execute('''
  INSERT INTO Kaffebønne
    ('Art')
  VALUES
    (?)
  ''', attributes)

def insert_kaffegard(attributes):
  cursor.execute('''
  INSERT INTO Kaffegård
    (Navn, HøydeOverHavet, Land, Region)
  VALUES
    (?, ?, ?, ?)
  ''', attributes)

def insert_bruker(attributes):
  cursor.execute('''
  INSERT INTO Bruker
    (Epost, Passord, FulltNavn, Land)
  VALUES
    (?, ?, ?, ?)
  ''', attributes)

def insert_foredlingsmetode(attributes):
  cursor.execute('''
  INSERT INTO Foredlingsmetode
    (Navn, Beskrivelse)
  VALUES
    (?, ?)
  ''', attributes)

def insert_kaffesmaking(attributes):
  cursor.execute('''
  INSERT INTO Kaffesmaking
    (Epost, KaffebrenneriNavn, KaffeNavn, Smaksnotater, Poeng, Dato)
  VALUES
    (?, ?, ?, ?, ?, ?)
  ''', attributes)

def insert_dyrketAv(attributes):
  cursor.execute('''
  INSERT INTO DyrketAv
    (KaffebønneArt, KaffegårdNavn)
  VALUES
    (?, ?)
  ''', attributes)

def insert_partiBestarAv(attributes):
  cursor.execute('''
  INSERT INTO PartiBestårAv
    (KaffebønneArt, KaffepartiId)
  VALUES
    (?,?)
  ''', attributes)

### Selects ###

def get_kaffe():
  cursor.execute('''
  SELECT * FROM Kaffe
  ''')
  return cursor.fetchall()

def get_unique_coffees_per_user():
  cursor.execute('''
  SELECT FulltNavn, COUNT(*) AS Antall
  FROM Kaffesmaking INNER JOIN Bruker USING (Epost)
  WHERE Dato LIKE '%2022'
  GROUP BY Epost
  ORDER BY Antall DESC
  ''')
  return cursor.fetchall()

def get_value_per_money():
  cursor.execute('''
  SELECT Kaffe.KaffebrenneriNavn, Kaffe.Kilopris, AVG(Poeng) AS GjPoeng  
  FROM Kaffe INNER JOIN Kaffesmaking
  ON Kaffe.KaffebrenneriNavn = KaffeSmaking.KaffebrenneriNavn
    AND Kaffe.Navn = KaffeSmaking.KaffeNavn 
  GROUP BY Kaffe.KaffebrenneriNavn, Kaffe.Navn
  ORDER BY GjPoeng DESC
  ''')
  return cursor.fetchall()

def get_floral_description():
  cursor.execute('''
  SELECT Kaffe.KaffebrenneriNavn, Kaffe.Navn
  FROM Kaffe INNER JOIN Kaffesmaking
  ON Kaffe.KaffebrenneriNavn = KaffeSmaking.KaffebrenneriNavn
    AND Kaffe.Navn = KaffeSmaking.KaffeNavn 
  WHERE Kaffe.Beskrivelse LIKE '%floral%'
    OR Kaffesmaking.Smaksnotater LIKE '%floral%'
  ''')
  return cursor.fetchall()

def get_not_washed_rwanda_colombia():
  cursor.execute('''
  SELECT Kaffe.Navn, Kaffe.KaffebrenneriNavn
  FROM (Kaffe INNER JOIN Kaffeparti) INNER JOIN Kaffegård
  ON Kaffe.KaffepartiID = Kaffeparti.ID AND Kaffeparti.KaffegårdNavn = Kaffegård.Navn
  WHERE (Kaffegård.Land='Rwanda' OR Kaffegård.Land='Colombia') 
    AND Kaffeparti.ForedlingsmetodeNavn != 'vasket'
  ''')
  return cursor.fetchall()


### Handlers ###

def handle_insert():
  options = ['kaffe', 'kaffebrenneri','kaffeparti', 'kaffebønne', 'kaffegård', 'bruker','kaffesmaking', 'dyrket av', 'parti består av']
  options_str = '\t' + '\n\t'.join(options)
  command = input(f'Hva vil du sette inn?\n{options_str}\n').lower()
  
  match command:
    case 'kaffe':
      attributes = ask(
        ['Navn', 'Dato', 'Brenningsgrad', 'Beskrivelse', 'Kilopris', 'KaffebrenneriNavn', 'KaffepartiID'],
        [str, str, str, str, float, str, str])
      insert_kaffe(attributes)
      
    case 'kaffebrenneri':
      attributes = ask(
        ['Navn'], [str]
      )
      insert_kaffebrenneri(attributes)

    case 'kaffeparti':
      attributes = ask(
        ['ID', 'Innhøstingsår', 'Kilopris', 'KaffegårdNavn', 'ForedlingsmetodeNavn'],
        [str, int, float, str, str])
      insert_kaffebrenneri(attributes)
      
    case 'kaffebønne':
      attributes = ask(
        ['Art'], [str]
      )
      insert_kaffebonne(attributes)
      
    case 'kaffegård':
      attributes = ask(
        ['Navn', 'HøydeOverHavet', 'Land', 'Region'],
        [str, str, str, str])
      insert_kaffegard(attributes)
      
    case 'bruker':
      attributes = ask(
        ['Epost','Passord', 'FulltNavn', 'Land']
        [str, str, str, str]
      )
      
    case 'kaffesmaking':
      attributes = ask(
        ['Epost', 'KaffebrenneriNavn', 'KaffeNavn', 'Smaksnotater', 'Poeng', 'Dato'],
        [str, str, str, str, int, str]
      )
      insert_kaffesmaking(attributes)

    case 'dyrket av':
      attributes = ask(
        ['KaffebønneArt', 'KaffegårdNavn'],
        [str, str])
      insert_dyrketAv(attributes)
      
    case 'parti består av':
      attributes = ask(
        ['KaffebønneArt', 'KaffepartiID'],
        [str, str])
      insert_partiBestarAv(attributes)
  

def handle_select():
  options = ['(1) flest unike kaffer i år', '(2) mest for pengene', '(3) beskrevet som floral', '(4) ikke vasket fra Rwanda eller Colombia']
  options_str = '\t' + '\n\t'.join(options)
  command = input(f'Hva vil du gjøre spørring på? (Skriv tallet)\n{options_str}\n').lower()
  
  match command:
    case '1':
      print(get_unique_coffees_per_user())
    case '2':
      print(get_value_per_money())
    case '3':
      print(get_floral_description())
    case '4':
      print(get_not_washed_rwanda_colombia())

def handle_update():
  print('TODO: ikke implementert.')

### Main ###

def main():
  global cursor
  connection = sqlite3.connect(':memory:')
  cursor = connection.cursor()

  build_tables()
  fill_database()

  print('\nVelkommen til Kaffedatabasen 😊\n')

  while True:
    options = ['insert', 'select', 'update', 'exit']
    options_str = '\t' + '\n\t'.join(options)
    command = input(f'\nHva vil du gjøre?\n{options_str}\n').lower()
    
    match command:
      case 'insert':
        handle_insert()
      case 'select':
        handle_select()
      case 'update':
        handle_select()
      case 'exit':
        break

  connection.close()


if __name__ == '__main__':
  main()

