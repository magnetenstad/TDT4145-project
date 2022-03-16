from database import Database
from utils import ask

### Globals ###

db = None
user = None

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

def open_app():
  options = ['(1) Logg inn', '(2) Opprett ny bruker']
  options_str = '\t' + '\n\t'.join(options)
  command = input(f'\nHva vil du gjøre? Skriv inn tallet\n{options_str}\n').lower()
  
  match command:
    case '1':
      handle_login()
    case '2':
      handle_registration()

def handle_login():
  global user
  while True:
    attributes = ask(['Epost', 'Password'])
    if db.login(attributes):
      user = attributes[0]
      print(f'Logget inn som {user}!')
      break
    else:
      print('Ugyldig epost eller passord!')

def handle_registration():
  global user
  while True:
    attributes = ask(['Epost', 'Passord', 'Fullt navn', 'Land'])
    try:
      db.insert_bruker(attributes)
      user = attributes[0]
      print(f'Registrert og logget inn som {user}!')
      break
    except:
      print('Eposten er allerede i bruk.')


### Main ###

def main():
  global db
  global user

  db = Database(':memory:')

  print('\nVelkommen til Kaffedatabasen 😊\n')
  
  while True:
    options = ['login', 'register']
    options_str = '\t' + '\n\t'.join(options)
    command = input(f'\nHva vil du gjøre?\n{options_str}\n').lower()
    
    match command:
      case 'login':
        handle_login()
      case 'register':
        handle_registration()
      case 'exit':
        break

    while True:
      options = ['insert', 'select', 'update', 'sign out']
      options_str = '\t' + '\n\t'.join(options)
      command = input(f'\nHva vil du gjøre?\n{options_str}\n').lower()
      
      match command:
        case 'insert':
          handle_insert()
        case 'select':
          handle_select()
        case 'update':
          handle_select()
        case 'sign out':
          user = None
          break

  db.close()


if __name__ == '__main__':
  main()

