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
    if state.route(state) == Response.exit:
      break


# Pages

def Welcome(state):
  print('Velkommen til Kaffedatabasen 😊☕\n')
  options = {
    'Logge inn': Login,
    'Logge inn som gjest': LoginGuest,
    'Registrere en ny bruker': Register,
    'Avslutte': Exit
  }
  state.route = options[ask_select('Hva vil du gjøre?', options.keys())]


def Main(state):
  options = {}
  if state.user != 'guest': options['Skrive data'] = Insert
  options['Lese data'] = Select
  if state.user == 'admin': options['Gå til admin-panel'] = Admin
  options['Logge ut'] = SignOut
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
  print(f'Logget ut.')
  state.route = Welcome


def Exit(_):
  print('Takk for nå!')
  return Response.exit


def Login(state):
  print('Logg inn med epost og passord:\n')
  attributes = ask(['Epost', 'Password'])
  if state.db.bruker_exists(attributes):
    state.user = attributes[0]
    print(f'\nLogget inn som \'{state.user}\'')
    state.route = Main
  else:
    print('\nUgyldig epost eller passord!')
    if ask_select('\nVil du prøve på nytt?', ['Ja', 'Nei']) == 'Nei':
      state.route = Welcome


def LoginGuest(state):
  state.user = 'guest'
  print(f'Logget inn som \'{state.user}\'')
  state.route = Main


def Register(state):
  print('Registrer deg med epost, passord, navn og land:\n')
  attributes = ask(['Epost', 'Passord', 'Fullt navn', 'Land'],
      [str, str, str, str])
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
      'Kaffe': ask_kaffe,
      'Kaffebrenneri': ask_kaffebrenneri,
      'Kaffeparti': ask_kaffeparti,
      'Kaffegård': ask_kaffegaard,
      'Kaffesmaking': ask_kaffesmaking,
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
  result = options[selected]()
  if type(result) != str and type(result) != list:
    result = result.to_markdown(index=False)
  print(f'\nResultatet ble:\n\n{result}')
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
  
  n = 0
  while not n:
    for kaffeboenne in state.db.get_kaffeboenner():
      if ask_select(f'Dyrker gården kaffebønnen {kaffeboenne[0]}?',
          ['Ja', 'Nei']) == 'Ja':
        state.db.insert_dyrketAv([kaffeboenne[0], kaffegaard[0]])
        n += 1
    if n == 0:
      print('\nEn kaffegård må dyrke minst én kaffebønne!\n')
  
  return kaffegaard[0]


def ask_kaffeparti(state):
  print('\nFyll inn følgende verdier for kaffepartiet.\n')
  kaffeparti = ask(
      ['Innhøstningsår', 'Kilopris'],
      [int, float])

  kaffegaard_navn = ask_select_or_create(state,
          '\nVed hvilken kaffegård er partiet produsert?',
          state.db.get_kaffegaarder(),
          ask_kaffegaard)
  kaffeparti.append(kaffegaard_navn)

  kaffeparti.append(
      ask_select_or_create(state,
          '\nHvilken foredlingsmetode er brukt?',
          state.db.get_foredlingsmetoder(),
          ask_foredlingsmetode))

  kaffeparti_id = state.db.insert_kaffeparti(kaffeparti)

  if kaffeparti_id == None:
    return
  
  kaffeboenner = state.db.get_kaffeboenner_on_kaffegaard([kaffegaard_navn])

  print(f'Kaffegården {kaffegaard_navn} dyrker følgende kaffebønner: {kaffeboenner}\n')

  n = 0
  while not n:
    for kaffeboenne in kaffeboenner:
      if ask_select(f'Består partiet av kaffebønnen {kaffeboenne}?',
          ['Ja', 'Nei']) == 'Ja':
        state.db.insert_partiBestaarAv([kaffeparti_id, kaffeboenne])
        n += 1
    if n == 0:
      print('\nEt kaffeparti må bestå av minst én kaffebønne!\n')
  
  return kaffeparti_id


def ask_kaffe(state):
  print('\nFyll inn følgende verdier for kaffen.\n')
  kaffe = ask(['KaffebrenneriNavn', 'Navn', 'Brenningsdato (yyyy.mm.dd)', 
      'Brenningsgrad', 'Beskrivelse', 'Kilopris'],
      [str, str, Date, str, str, float])

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
      ask(['Smaksnotater', 'Poeng', 'Smaksdato (yyyy.mm.dd)'],
          [str, int, Date])

  state.db.insert_kaffesmaking(kaffesmaking)
  return kaffesmaking[:2]
