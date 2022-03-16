from utils import ask, ask_select


class Response:
  exit = 0


class AppState:
  db = None
  user = None
  route = lambda: print('[ERROR] Route is not defined.')


def App(state):
  state.route = Welcome
  while True:
    if state.route(state) == Response.exit:
      break

def Welcome(state):
  options = {
    'login': Login,
    'register': Register,
    'exit': Exit
  }
  state.route = options[ask_select('Hva vil du gjøre?', options.keys())]

def Main(state):
  options = {
    'insert': Insert,
    'select': Select,
    'update': Update,
    'sign out': SignOut
  }
  state.route = options[ask_select('Hva vil du gjøre?', options.keys())]

def SignOut(state):
  state.user = None
  state.route = Welcome

def Exit(_):
  return Response.exit

def Login(state):
  while True:
    attributes = ask(['Epost', 'Password'])
    if state.db.login(attributes):
      state.user = attributes[0]
      state.route = Main
      print(f'Logget inn som {state.user}!')
      break
    else:
      print('Ugyldig epost eller passord!')

def Register(state):
  while True:
    attributes = ask(['Epost', 'Passord', 'Fullt navn', 'Land'])
    try:
      state.db.insert_bruker(attributes)
      state.user = attributes[0]
      state.route = Main
      print(f'\nRegistrert og logget inn som {state.user}!\n')
      break
    except:
      print('\nEposten er allerede i bruk.\n')


def Insert(state):
  match ask_select('Hva vil du sette inn?', [
      'kaffe', 'kaffebrenneri','kaffeparti', 'kaffeboenne', 'kaffegaard',
      'bruker','kaffesmaking', 'dyrket av', 'parti består av']):
    
    case 'kaffe':
      attributes = ask(
        ['Navn', 'Dato', 'Brenningsgrad', 'Beskrivelse', 'Kilopris', 'KaffebrenneriNavn', 'KaffepartiID'],
        [str, str, str, str, float, str, str])
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
      state.db.insert_kaffebonne(attributes)
      
    case 'kaffegaard':
      attributes = ask(
        ['Navn', 'HoeydeOverHavet', 'Land', 'Region'],
        [str, str, str, str])
      state.db.insert_kaffegard(attributes)
      
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
      state.db.insert_partiBestarAv(attributes)
  state.route = Main


def Select(state):
  match ask_select('Hva vil du gjøre spørring på?', [
      'flest unike kaffer i år',
      'mest for pengene',
      'beskrevet som floral',
      'ikke vasket fra Rwanda eller Colombia'], indexed=True):
    case 0:
      print(state.db.get_unique_coffees_per_user())
    case 1:
      print(state.db.get_value_per_money())
    case 2:
      print(state.db.get_floral_description())
    case 3:
      print(state.db.get_not_washed_rwanda_colombia())
  state.route = Main

def Update(state):
  print('TODO: ikke implementert.')
  state.route = Main
