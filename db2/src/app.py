from utils import *


class Response:
  exit = 0


class AppState:
  db = None
  user = None
  route = None


def App(state):
  state.route = Welcome
  while True:
    print()
    if state.user:
      print(f'Logget inn som \'{state.user}\'\n')
    if state.route(state) == Response.exit:
      break


# Pages

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
    'Logge ut': SignOut
  }
  if state.user == 'admin':
    options['Gå til admin-panel'] = Admin
  state.route = options[ask_select('Hva vil du gjøre?', options.keys())]


def Admin(state):
  options = {
      'Resette databasen til standardverdier': state.db.reset,
      'Ingenting, gå tilbake': lambda: None
  }
  options[ask_select('Hva vil du gjøre?', options.keys())]()
  if ask_select('\nVil du gjøre noe mer i admin-panelet?', 
      ['Ja', 'Nei']) == 'Nei':
    state.route = Main


def SignOut(state):
  state.user = None
  state.route = Welcome


def Exit(_):
  return Response.exit


def Login(state):
  print('Logg inn med epost og passord:\n')
  attributes = ask(['Epost', 'Password'])
  if state.db.bruker_exists(attributes):
    state.user = attributes[0]
    state.route = Main
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
  options = {
      'kaffe': ask_kaffe,
      'kaffebrenneri': ask_kaffebrenneri,
      'kaffeparti': ask_kaffeparti,
      'kaffegaard': ask_kaffegaard,
      'kaffesmaking': ask_kaffesmaking, 
      'Ingenting, gå tilbake': lambda _: None
  }
  options[ask_select('Hva vil du sette inn?', options.keys())](state)
  if ask_select('\nVil du sette inn noe mer?', ['Ja', 'Nei']) == 'Nei':
    state.route = Main


def Select(state):
  options = {
    'Alle kaffesmakinger': state.db.get_kaffesmakinger,
    'Flest unike kaffer i år': state.db.get_unique_coffees_per_user,
    'Mest for pengene': state.db.get_value_per_money,
    'Beskrevet som floral': state.db.get_floral_description,
    'Ikke vasket fra Rwanda eller Colombia':
        state.db.get_not_washed_rwanda_colombia,
    'Hele databasen': state.db.print_all,
  }
  selected = ask_select('Hva vil du gjøre spørring på?', options.keys())
  print(f'\nResultatet ble:\n\n{options[selected]()}\n')
  if ask_select('\nVil du gjøre en ny spørring?', ['Ja', 'Nei']) == 'Nei':
    state.route = Main


# ask_x

def ask_kaffebrenneri(state):
  print('\nFyll inn følgende verdier for kaffebrenneriet.\n')
  kaffebrenneri = ask(['Navn'], [str])
  state.db.insert_kaffebrenneri(kaffebrenneri)
  return kaffebrenneri[0]


def ask_foredlingsmetode(state):
  print('\nFyll inn følgende verdier for foredlingsmetoden.\n')
  foredlingsmetode = ask(['Navn', 'Beskrivelse'], [str, str])
  state.db.insert_foredlingsmetode(foredlingsmetode)
  return foredlingsmetode[0]


def ask_kaffegaard(state):
  print('\nFyll inn følgende verdier for kaffegården.\n')
  kaffegaard = ask(['Navn', 'HoeydeOverHavet', 'Land', 'Region'],
      [str, float, str, str])
  state.db.insert_kaffegaard(kaffegaard)
  
  for kaffeboenne in state.db.get_kaffeboenner():
    if ask_select(f'Dyrker gården kaffebønnen {kaffeboenne[0]}?',
        ['Ja', 'Nei']) == 'Ja':
      state.db.insert_dyrketAv([kaffeboenne[0], kaffegaard[0]])

  return kaffegaard[0]


def ask_kaffeparti(state):
  print('\nFyll inn følgende verdier for kaffepartiet.\n')
  kaffeparti = ask(
      ['Innhøstningsår', 'Kilopris'],
      [int, float])

  kaffegaard_id = ask_select_or_create(state,
          '\nVed hvilken kaffegård er partiet produsert?',
          state.db.get_kaffegaarder(),
          ask_kaffegaard)
  kaffeparti.append(kaffegaard_id)

  kaffeparti.append(
      ask_select_or_create(state,
          '\nHvilken foredlingsmetode er brukt?',
          state.db.get_foredlingsmetoder(),
          ask_foredlingsmetode))

  kaffeparti_id = state.db.insert_kaffeparti(kaffeparti)

  if kaffeparti_id == None:
    return

  for kaffeboenne in state.db.get_kaffeboenner_on_kaffegaard([kaffegaard_id]):
    if ask_select(f'Består partiet av kaffebønnen {kaffeboenne[0]}?',
        ['Ja', 'Nei']) == 'Ja':
      state.db.insert_partiBestaarAv([kaffeboenne[0], kaffeparti_id])
  
  return kaffeparti_id


def ask_kaffe(state):
  print('\nFyll inn følgende verdier for kaffen.\n')
  kaffe = ask(['KaffebrenneriNavn', 'Navn', 'Brenningsdato (yyyy.mm.dd)', 
      'Brenningsgrad', 'Beskrivelse', 'Kilopris'],
      [str, str, str, str, str, float])

  kaffeparti_id = ask_select_or_create(state,
          '\nHvilket kaffeparti er kaffen fremstilt av?',
          state.db.get_kaffepartier(),
          ask_kaffeparti)

  if kaffeparti_id == None:
    return

  kaffe.append(kaffeparti_id)

  state.db.insert_kaffe(kaffe)
  return kaffe[:2]


def ask_kaffesmaking(state):
  kaffe = list(ask_select_or_create(state,
      '\nHvilken kaffe har du smakt?',
      state.db.get_kaffer(),
      ask_kaffe, key_end=2))
  
  if kaffe == None:
    return

  if (state.db.kaffesmaking_exists([state.user] + kaffe)):
    print('\nDu har allerede smakt på denne kaffen.\n')
    if ask_select(
        'Vil du erstatte den eksisterende kaffesmakingen?',
        ['Ja', 'Nei']) == 'Nei':
      return
    state.db.delete_kaffesmaking([state.user] + kaffe)
  
  print('\nFyll inn følgende verdier for kaffesmakingen.\n')
  kaffesmaking = [state.user] + kaffe + \
      ask(['Smaksnotater', 'Poeng', 'Dato (yyyy.mm.dd)'],
          [str, str, str, int, str])

  state.db.insert_kaffesmaking(kaffesmaking)
  return kaffesmaking[:2]
