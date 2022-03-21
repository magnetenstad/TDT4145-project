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
      'kaffe', 'kaffebrenneri','kaffeparti', 'kaffeboenne', 'kaffegaard','kaffesmaking', 'dyrket av', 'parti består av', 'ingenting']):
       
    case 'ingenting':
      pass

    case 'kaffe':
      attributes = ask(
        ['Navn', 'Brenningsdato (yyyy.mm.dd)', 'Brenningsgrad', 'Beskrivelse', 'Kilopris', 'KaffebrenneriNavn', 'KaffepartiID'],
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
      kaffesmaking = ask(
        ['KaffebrenneriNavn', 'KaffeNavn', 'Smaksnotater', 'Poeng', 'Dato (yyyy.mm.dd)'],
        [str, str, str, int, str]
      )
 
      state.db.insert_kaffebrenneri([kaffesmaking[0]])

      if (state.db.kaffesmaking_exists([state.user] + kaffesmaking[:2])):
        print('Du har allerede smakt på denne kaffen.')
        if ask_select('\nVil du erstatte den eksisterende kaffesmakingen?', ['Ja', 'Nei']) == 'Ja':
          state.db.delete_kaffesmaking([state.user] + kaffesmaking[:2])
          state.db.insert_kaffesmaking([state.user] + kaffesmaking)
      else:
        state.db.insert_kaffesmaking([state.user] + kaffesmaking)
      
      if not state.db.kaffe_exists(kaffesmaking[:2]):
        print('\nVi har ikke informasjon om kaffen du har smakt. Vennligst fyll inn følgende:\n')

        # Kaffe

        kaffe = ask(
        ['Brenningsdato (yyyy.mm.dd)', 'Brenningsgrad', 'Beskrivelse', 'Kilopris'],
        [str, str, str, float])

        kaffe.insert(0, kaffesmaking[1])
        kaffe.insert(5, kaffesmaking[0])

        kaffeparti_options = {
          str(x[1:]): x[0] for x in state.db.get_kaffepartier()
        }
        kaffeparti_options['Ingen av disse.'] = -1
        kaffeparti_id = kaffeparti_options[ask_select('\nHvilket kaffeparti er kaffen din fremstilt av?', kaffeparti_options.keys())]

        if kaffeparti_id == -1:
          print(f'Du valgte ingen av de eksisterende kaffepartiene. Vennligst fyll inn følgende: ')

          kaffeparti = ask(
            ['Innhøstningsår', 'Kilopris'],
            [int, float])
          
          # Kaffegård
          
          kaffegaard_options = {
            str(x[:]): x[0] for x in state.db.get_kaffegaarder()
          }
          kaffegaard_options['Ingen av disse.'] = -1
          kaffegaard_navn = kaffegaard_options[
            ask_select('\nHvilken kaffegård har produsert partiet?', kaffegaard_options.keys())
          ]

          if kaffegaard_navn == -1:
            kaffegaard = ask(['Navn', 'HoeydeOverHavet', 'Land', 'Region'], [str, float, str, str])
            state.db.insert_kaffegaard(kaffegaard)
            kaffeparti.append(kaffegaard[0])
          else:
            kaffeparti.append(kaffegaard_navn)

          # Foredlingsmetode

          foredlingsmetode_options = {
            str(x[:]): x[0] for x in state.db.get_foredlingsmetoder()
          }
          foredlingsmetode_options['Ingen av disse.'] = -1
          foredlingsmetode_navn = foredlingsmetode_options[
            ask_select('\nHvilken foredlingsmetode er brukt?', foredlingsmetode_options.keys())
          ]

          if foredlingsmetode_navn == -1:
            foredlingsmetode = ask(['Navn', 'Beskrivelse'], [str, str])
            state.db.insert_foredlingsmetode(foredlingsmetode)
            kaffeparti.append(foredlingsmetode[0])
          else:
            kaffeparti.append(foredlingsmetode_navn)
          
          kaffeparti_id = state.db.insert_kaffeparti(kaffeparti)
          kaffe.append(kaffeparti_id)
          
          # Kaffebønner?

          for boenne in state.db.get_kaffeboenner():
            if ask_select(f'Består partiet av {boenne[0]}?',
                ['Ja', 'Nei']) == 'Ja':
              state.db.insert_partiBestaarAv([boenne[0], kaffeparti_id])

        else:
          print(f'Du valgte {kaffeparti_id}')
          kaffe.append(kaffeparti_id)
        
        state.db.insert_kaffe(kaffe)

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
