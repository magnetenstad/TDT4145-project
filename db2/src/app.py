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
    print()#'\n'*48)
    if state.user:
      print(f'Logget inn som \'{state.user}\'')
    print()#'\n'*4)
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
      'kaffeboenne': ask_kaffeboenne,
      'kaffegaard': ask_kaffegaard,
      'kaffesmaking': ask_kaffesmaking, 
      'dyrket av': ask_dyrketAv,
      'parti består av': ask_partiBestaarAv,
      'Ingenting, gå tilbake': lambda _: None
  }
  options[ask_select('Hva vil du sette inn?', options.keys())](state)
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
  print(f'\nResultatet ble: {options[selected]()}')
  if ask_select('\nVil du gjøre en ny spørring?', ['Ja', 'Nei']) == 'Nei':
    state.route = Main


def Update(state):
  print('TODO: ikke implementert.')
  state.route = Main



def ask_kaffebrenneri(state):
  kaffebrenneri = ask(
    ['Navn'], [str]
  )
  state.db.insert_kaffebrenneri(kaffebrenneri)
  return kaffebrenneri[0]

def ask_kaffeboenne(state):
  kaffeboenne = ask(
    ['Art'], [str]
  )
  state.db.insert_kaffeboenne(kaffeboenne)

def ask_dyrketAv(state):
  attributes = ask(
    ['KaffeboenneArt', 'KaffegaardNavn'],
    [str, str])
  state.db.insert_dyrketAv(attributes)

def ask_partiBestaarAv(state):
  attributes = ask(
    ['KaffeboenneArt', 'KaffepartiID'],
    [str, str])
  state.db.insert_partiBestaarAv(attributes)

def ask_foredlingsmetode(state):
  foredlingsmetode = ask(['Navn', 'Beskrivelse'], [str, str])
  state.db.insert_foredlingsmetode(foredlingsmetode)
  return foredlingsmetode[0]

def ask_kaffegaard(state):
  kaffegaard = ask(['Navn', 'HoeydeOverHavet', 'Land', 'Region'],
      [str, float, str, str])
  state.db.insert_kaffegaard(kaffegaard)
  return kaffegaard[0]

def ask_kaffeparti(state):
  kaffeparti = ask(
      ['Innhøstningsår', 'Kilopris'],
      [int, float])

  kaffeparti.append(
      ask_select_or_create(state,
          '\nVed hvilken kaffegård er partiet produsert?',
          state.db.get_kaffegaarder(),
          ask_kaffegaard))

  kaffeparti.append(
      ask_select_or_create(state,
          '\nHvilken foredlingsmetode er brukt?',
          state.db.get_foredlingsmetoder(),
          ask_foredlingsmetode))

  kaffeparti_id = state.db.insert_kaffeparti(kaffeparti)

  for kaffeboenne in state.db.get_kaffeboenner():
    if ask_select(f'Består partiet av {kaffeboenne[0]}?',
        ['Ja', 'Nei']) == 'Ja':
      state.db.insert_partiBestaarAv([kaffeboenne[0], kaffeparti_id])
  
  return kaffeparti_id

def ask_kaffe(state, kaffe_PK=None):
    if kaffe_PK:
      kaffe = kaffe_PK + ask(['Brenningsdato (yyyy.mm.dd)', 
          'Brenningsgrad', 'Beskrivelse', 'Kilopris'],
          [str, str, str, float])
    else:
      kaffe = ask(['KaffebrenneriNavn', 'Navn', 'Brenningsdato (yyyy.mm.dd)', 
          'Brenningsgrad', 'Beskrivelse', 'Kilopris'],
          [str, str, str, str, str, float])

    kaffe.append(
        ask_select_or_create(state,
            '\nHvilket kaffeparti er kaffen fremstilt av?',
            state.db.get_kaffepartier(),
            ask_kaffeparti))

    state.db.insert_kaffe(kaffe)

def ask_kaffesmaking(state):
  kaffesmaking = ask(['KaffebrenneriNavn', 'KaffeNavn',
      'Smaksnotater', 'Poeng', 'Dato (yyyy.mm.dd)'],
      [str, str, str, int, str])

  state.db.insert_kaffebrenneri([kaffesmaking[0]])

  if (state.db.kaffesmaking_exists([state.user] + kaffesmaking[:2])):
    print('Du har allerede smakt på denne kaffen.')
    if ask_select(
        '\nVil du erstatte den eksisterende kaffesmakingen?',
        ['Ja', 'Nei']) == 'Ja':
      state.db.delete_kaffesmaking([state.user] + kaffesmaking[:2])
      state.db.insert_kaffesmaking([state.user] + kaffesmaking)
  else:
    state.db.insert_kaffesmaking([state.user] + kaffesmaking)
  
  if not state.db.kaffe_exists(kaffesmaking[:2]):
    print('\nVi har ikke informasjon om kaffen du har smakt. Vennligst fyll inn følgende:\n')
    ask_kaffe(state, kaffesmaking[:2])

