from utils import ask, ask_select


class Response:
  exit = 0


class AppState:
  db = None
  user = None
  route = None

def App(state):
  state.route = Welcome
  while True:
    print('\n'*48)
    if state.user:
      print(f'Logget inn som \'{state.user}\'')
    print('\n'*4)
    if state.route(state) == Response.exit:
      break


def Welcome(state):
  print('Velkommen til Kaffedatabasen 😊☕\n')
  options = {
    'Logge inn': Login,
    'Registrere en ny bruker': Register,
    'Avslutte': Exit
  }
  state.route = options[ask_select('Hva vil du gjøre?', options.keys())]


def Main(state):
  options = {
    'Skrive data': Insert,
    'Lese data': Select,
    'Oppdatere data': Update,
    'Logge ut': SignOut
  }
  state.route = options[ask_select('Hva vil du gjøre?', options.keys())]


def SignOut(state):
  state.user = None
  state.route = Welcome


def Exit(_):
  return Response.exit


def Login(state):
  print('Logg inn med epost og passord:\n')
  attributes = ask(['Epost', 'Password'])
  if state.db.login(attributes):
    state.user = attributes[0]
    state.route = Main
    print(f'Logget inn som {state.user}!')
  else:
    print('\nUgyldig epost eller passord!')
    if ask_select('\nVil du prøve på nytt?', ['Ja', 'Nei']) == 'Nei':
      state.route = Welcome


def Register(state):
  print('Registrer deg med epost, passord, navn og land:\n')
  attributes = ask(['Epost', 'Passord', 'Fullt navn', 'Land'])
  try:
    state.db.insert_bruker(attributes)
    state.user = attributes[0]
    state.route = Main
    print(f'\nRegistrert og logget inn som {state.user}!\n')
  except:
    print('\nEposten er allerede i bruk.\n')
    if ask_select('\nVil du prøve på nytt?', ['Ja', 'Nei']) == 'Nei':
      state.route = Welcome


def Insert(state):
  match ask_select('Hva vil du sette inn?', [
      'kaffe', 'kaffebrenneri','kaffeparti', 'kaffeboenne', 'kaffegaard',
      'bruker','kaffesmaking', 'dyrket av', 'parti består av']):
    
    case 'kaffe':
      attributes = ask(
        ['Navn', 'Dato', 'Brenningsgrad', 'Beskrivelse', 'Kilopris', 'KaffebrenneriNavn', 'KaffepartiID'],
        [str, str, str, str, float, str, str])
      print(attributes)
      state.db.insert_kaffe(attributes)
      
    case 'kaffebrenneri':
      attributes = ask(
        ['Navn'], [str]
      )
      state.db.insert_kaffebrenneri(attributes)

    case 'kaffeparti':
      attributes = ask(
        ['ID', 'Innhoestingsaar', 'Kilopris', 'KaffegaardNavn', 'ForedlingsmetodeNavn'],
        [str, int, float, str, str])
      state.db.insert_kaffebrenneri(attributes)
      
    case 'kaffeboenne':
      attributes = ask(
        ['Art'], [str]
      )
      state.db.insert_kaffeboenne(attributes)
      
    case 'kaffegaard':
      attributes = ask(
        ['Navn', 'HoeydeOverHavet', 'Land', 'Region'],
        [str, str, str, str])
      state.db.insert_kaffegaard(attributes)
      
    case 'bruker':
      attributes = ask(
        ['Epost','Passord', 'FulltNavn', 'Land'],
        [str, str, str, str]
      )
      
    case 'kaffesmaking':
      attributes = ask(
        ['Epost', 'KaffebrenneriNavn', 'KaffeNavn', 'Smaksnotater', 'Poeng', 'Dato'],
        [str, str, str, str, int, str]
      )
      state.db.insert_kaffesmaking(attributes)

    case 'dyrket av':
      attributes = ask(
        ['KaffeboenneArt', 'KaffegaardNavn'],
        [str, str])
      state.db.insert_dyrketAv(attributes)
      
    case 'parti består av':
      attributes = ask(
        ['KaffeboenneArt', 'KaffepartiID'],
        [str, str])
      state.db.insert_partiBestaarAv(attributes)
  state.route = Main


def Select(state):
  options = {
    'Flest unike kaffer i år': state.db.get_unique_coffees_per_user,
    'Mest for pengene': state.db.get_value_per_money,
    'Beskrevet som floral': state.db.get_floral_description,
    'Ikke vasket fra Rwanda eller Colombia':
        state.db.get_not_washed_rwanda_colombia
  }
  selected = ask_select('Hva vil du gjøre spørring på?', options.keys())
  print(f'\nResultatet ble: {options[selected]()}')
  if ask_select('\nVil du gjøre en ny spørring?', ['Ja', 'Nei']) == 'Nei':
    state.route = Main


def Update(state):
  print('TODO: ikke implementert.')
  state.route = Main
