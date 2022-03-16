import sqlite3

from database import Database

### Globals ###

db = None

### Utils ###

def ask(questions, types=None):
	try:
		if types == None:
			return [input(f'{q}: ') for q in questions]
		else:
			return [types[i](input(f'<{types[i].__name__}> {q}: ')) for i, q in enumerate(questions)]
	except Exception as e:
		print(f'ERROR - {e}')

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
      db.insert_kaffe(attributes)
      
    case 'kaffebrenneri':
      attributes = ask(
        ['Navn'], [str]
      )
      db.insert_kaffebrenneri(attributes)

    case 'kaffeparti':
      attributes = ask(
        ['ID', 'Innhøstingsår', 'Kilopris', 'KaffegårdNavn', 'ForedlingsmetodeNavn'],
        [str, int, float, str, str])
      db.insert_kaffebrenneri(attributes)
      
    case 'kaffebønne':
      attributes = ask(
        ['Art'], [str]
      )
      db.insert_kaffebonne(attributes)
      
    case 'kaffegård':
      attributes = ask(
        ['Navn', 'HøydeOverHavet', 'Land', 'Region'],
        [str, str, str, str])
      db.insert_kaffegard(attributes)
      
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
      db.insert_kaffesmaking(attributes)

    case 'dyrket av':
      attributes = ask(
        ['KaffebønneArt', 'KaffegårdNavn'],
        [str, str])
      db.insert_dyrketAv(attributes)
      
    case 'parti består av':
      attributes = ask(
        ['KaffebønneArt', 'KaffepartiID'],
        [str, str])
      db.insert_partiBestarAv(attributes)
  

def handle_select():
  options = ['(1) flest unike kaffer i år', '(2) mest for pengene', '(3) beskrevet som floral', '(4) ikke vasket fra Rwanda eller Colombia']
  options_str = '\t' + '\n\t'.join(options)
  command = input(f'Hva vil du gjøre spørring på? (Skriv tallet)\n{options_str}\n').lower()
  
  match command:
    case '1':
      print(db.get_unique_coffees_per_user())
    case '2':
      print(db.get_value_per_money())
    case '3':
      print(db.get_floral_description())
    case '4':
      print(db.get_not_washed_rwanda_colombia())

def handle_update():
  print('TODO: ikke implementert.')

### Main ###

def main():
  global db
  connection = sqlite3.connect(':memory:')
  cursor = connection.cursor()

  db = Database(cursor)

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

