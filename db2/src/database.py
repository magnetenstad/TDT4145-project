import sqlite3
import pandas as pd

class Database:

  def __init__(self, path):
    self.connection = sqlite3.connect(path)
    self.cursor = self.connection.cursor()
    
    if len(self.get_tables()) == 0:
      self.reset()

  def create_tables(self):
    with open('tables.sql', 'r') as file:
      for i, statement in enumerate(file.read().split(';')):
        try:
          self.cursor.execute(statement)
          self.connection.commit()
        except Exception as e:
          print(f'[DB] [ERROR] in create table {i}: {statement}')
          print(e)
      print('\n ✅ Successfully built tables!\n')

  def get_tables(self):
    self.cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
    return list(map(lambda x: x[0], self.cursor.fetchall()))

  def drop_tables(self):
    for table in self.get_tables():
        self.cursor.execute(f'DROP TABLE {table}')
   
  def reset(self):
    self.drop_tables()
    self.create_tables()
    self.insert_defaults()

  def close(self):
    self.connection.close()

  ### Inserts ###

  def insert_kaffe(self, attributes):
    """attributes: [KaffebrenneriNavn, Navn, Dato, Brenningsgrad, Beskrivelse, Kilopris, KaffepartiId]"""
    try:
      self.cursor.execute('''
      INSERT INTO Kaffe
        (KaffebrenneriNavn, Navn, Dato, Brenningsgrad, Beskrivelse, Kilopris, KaffepartiId) 
      VALUES (?, ?, ?, ?, ?, ?, ?)
      ''', (attributes))
      self.connection.commit()
      print(f'\n ✅ Satt inn kaffen {attributes} \n')
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn kaffen {attributes}! Kanskje den allerede finnes?')
      print(f'\n Feilmelding: \n {e}')

  def insert_kaffebrenneri(self, attributes):
    """attributes: [Navn]"""
    try:
      self.cursor.execute('''
      INSERT INTO Kaffebrenneri
        (Navn)
      VALUES
        (?)
      ''', attributes)
      self.connection.commit()
      print(f'\n ✅ Satt inn kaffebrenneriet {attributes} \n')
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn kaffebrenneriet {attributes}! Kanskje det allerede finnes?')
      print(f'\n Feilmelding: \n {e}')

  def insert_kaffeparti(self, attributes) -> int:
    """attributes: [Id, Innhoestingsaar, Kilopris, KaffegaardNavn, ForedlingsmetodeNavn]"""
    try:
      kaffeparti_id = self.get_uuid()
      self.cursor.execute('''
      INSERT INTO Kaffeparti
        (Id, Innhoestingsaar, Kilopris, KaffegaardNavn, ForedlingsmetodeNavn)
      VALUES
        (?, ?, ?, ?, ?)
      ''', [kaffeparti_id] + attributes)
      self.connection.commit()
      print(f'\n ✅ Satt inn kaffepartiet {attributes} \n')
      return kaffeparti_id
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn kaffepartiet {attributes}! Kanskje det allerede finnes?')
      print(f'\n Feilmelding: \n {e}')
      
  def insert_kaffeboenne(self, attributes):
    """attributes: [Art]"""
    try:
      self.cursor.execute('''
      INSERT INTO Kaffeboenne
        (Art)
      VALUES
        (?)
      ''', attributes)
      self.connection.commit()
      print(f'\n ✅ Satt inn kaffebønnen {attributes} \n')
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn kaffebønnen {attributes}! Kanskje den allerede finnes?')
      print(f'\n Feilmelding: \n {e}')

  def insert_kaffegaard(self, attributes):
    """attributes: [Navn, HoeydeOverHavet, Land, Region]"""
    try:
      self.cursor.execute('''
      INSERT INTO Kaffegaard
        (Navn, HoeydeOverHavet, Land, Region)
      VALUES
        (?, ?, ?, ?)
      ''', attributes)
      self.connection.commit()
      print(f'\n ✅ Satt inn kaffegården {attributes} \n')
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn kaffegården {attributes}! Kanskje den allerede finnes?')
      print(f'\n Feilmelding: \n {e}')

  def insert_bruker(self, attributes):
    """attributes: [Epost, Passord, FulltNavn, Land]"""
    try:
      self.cursor.execute('''
      INSERT INTO Bruker
        (Epost, Passord, FulltNavn, Land)
      VALUES
        (?, ?, ?, ?)
      ''', attributes)
      self.connection.commit()
      print(f'\n ✅ Satt inn brukeren {attributes} \n')
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn brukeren {attributes}! Kanskje den allerede finnes?')
      print(f'\n Feilmelding: \n {e}')

  def insert_foredlingsmetode(self, attributes):
    """attributes: [Navn, Beskrivelse]"""
    try:
      self.cursor.execute('''
      INSERT INTO Foredlingsmetode
        (Navn, Beskrivelse)
      VALUES
        (?, ?)
      ''', attributes)
      self.connection.commit()
      print(f'\n ✅ Satt inn foredlingsmetoden {attributes} \n')
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn foredlingsmetoden {attributes}! Kanskje den allerede finnes?')
      print(f'\n Feilmelding: \n {e}')

  def insert_kaffesmaking(self, attributes):
    """attributes: [Epost, KaffebrenneriNavn, KaffeNavn, Smaksnotater, Poeng, Dato]"""
    try:
      self.cursor.execute('''
      INSERT INTO Kaffesmaking
        (Epost, KaffebrenneriNavn, KaffeNavn, Smaksnotater, Poeng, Dato)
      VALUES
        (?, ?, ?, ?, ?, ?)
      ''', attributes)
      self.connection.commit()
      print(f'\n ✅ Satt inn kaffesmakingen {attributes} \n')
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn kaffesmakingen {attributes}! Kanskje den allerede finnes?')
      print(f'\n Feilmelding: \n {e}')

  def insert_dyrketAv(self, attributes):
    """attributes: [KaffeboenneArt, KaffegaardNavn]"""
    try:
      self.cursor.execute('''
      INSERT INTO DyrketAv
        (KaffeboenneArt, KaffegaardNavn)
      VALUES
        (?, ?)
      ''', attributes)
      self.connection.commit()
      print(f'\n ✅ Satt inn at kaffegården {attributes[1]} dyrker kaffebønnen {attributes[0]} \n')
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn at kaffegården {attributes[1]} dyrker kaffebønnen {attributes[0]}! Kanskje det allerede er satt inn?')
      print(f'\n Feilmelding: \n {e}')
  
  def insert_partiBestaarAv(self, attributes):
    """attributes: [KaffeboenneArt, KaffepartiId]"""
    try:
      self.cursor.execute('''
      INSERT INTO PartiBestaarAv
        (KaffeboenneArt, KaffepartiId)
      VALUES
        (?,?)
      ''', attributes)
      self.connection.commit()
      print(f'\n ✅ Satt inn at kaffebønnen {attributes[0]} i parti {attributes[1]} \n')
    except Exception as e:
      print(f'\n ❌ Kunne ikke sette inn kaffbønnen {attributes[0]} i pati {attributes[1]}! Kanskje den allerede er satt inn?')
      print(f'\n Feilmelding: \n {e}')

  ### Getters ###

  def get_uuid(self):
    """KaffepartiId is the only generated key.
    A new uuid is given by MAX(Kaffeparti.id) + 1"""
    self.cursor.execute('''
    SELECT MAX(Id)
    FROM Kaffeparti
    ''')
    max_id = self.cursor.fetchone()[0]
    return max_id + 1 if max_id != None else 0

  def get_kaffer(self):
    self.cursor.execute('''
    SELECT * 
    FROM Kaffe
    ''')
    return self.cursor.fetchall()
  
  def get_kaffepartier(self):
    self.cursor.execute('''
    SELECT * 
    FROM Kaffeparti
    ''')
    return self.cursor.fetchall()
  
  def get_foredlingsmetoder(self):
    self.cursor.execute('''
    SELECT * 
    FROM Foredlingsmetode
    ''')
    return self.cursor.fetchall()

  def get_kaffegaarder(self):
    self.cursor.execute('''
    SELECT * 
    FROM Kaffegaard
    ''')
    return self.cursor.fetchall()
  
  def get_kaffeboenner(self):
    self.cursor.execute('''
    SELECT * 
    FROM Kaffeboenne
    ''')
    return self.cursor.fetchall()

  def get_kaffeboenner_on_kaffegaard(self, attributes):
    self.cursor.execute('''
    SELECT KaffeboenneArt
    FROM DyrketAv
    WHERE KaffegaardNavn = ?
    ''', attributes)
    return list(map(lambda x: x[0], self.cursor.fetchall()))

  def get_kaffesmakinger(self) -> pd.DataFrame:
    return pd.read_sql_query('''
        SELECT * 
        FROM Kaffesmaking
        ''', self.connection)
  
  def get_unique_coffees_per_user(self) -> pd.DataFrame:
    return pd.read_sql_query('''
        SELECT FulltNavn, COUNT(*) AS Antall
        FROM Kaffesmaking INNER JOIN Bruker USING (Epost)
        WHERE Dato LIKE '%2022'
        GROUP BY Epost
        ORDER BY Antall DESC
        ''', self.connection)

  def get_value_per_money(self) -> pd.DataFrame:
    return pd.read_sql_query('''
        SELECT Kaffe.KaffebrenneriNavn, Kaffe.Navn, Kaffe.Kilopris, AVG(Poeng) AS GjPoeng  
        FROM Kaffe INNER JOIN Kaffesmaking
        ON Kaffe.KaffebrenneriNavn = KaffeSmaking.KaffebrenneriNavn
          AND Kaffe.Navn = KaffeSmaking.KaffeNavn 
        GROUP BY Kaffe.KaffebrenneriNavn, Kaffe.Navn
        ORDER BY GjPoeng DESC
        ''', self.connection)

  def get_floral_description(self) -> pd.DataFrame:
    return pd.read_sql_query('''
        SELECT Kaffe.KaffebrenneriNavn, Kaffe.Navn
        FROM Kaffe LEFT OUTER JOIN Kaffesmaking
        ON Kaffe.KaffebrenneriNavn = KaffeSmaking.KaffebrenneriNavn
          AND Kaffe.Navn = KaffeSmaking.KaffeNavn 
        WHERE Kaffe.Beskrivelse LIKE '%floral%'
          OR Kaffesmaking.Smaksnotater LIKE '%floral%'
        ''', self.connection)

  def get_not_washed_rwanda_colombia(self) -> pd.DataFrame:
    return pd.read_sql_query('''
        SELECT Kaffe.Navn, Kaffe.KaffebrenneriNavn
        FROM (Kaffe INNER JOIN Kaffeparti) INNER JOIN Kaffegaard
        ON Kaffe.KaffepartiId = Kaffeparti.Id AND Kaffeparti.KaffegaardNavn = Kaffegaard.Navn
        WHERE (Kaffegaard.Land='Rwanda' OR Kaffegaard.Land='Colombia') 
          AND Kaffeparti.ForedlingsmetodeNavn != 'vasket'
        ''', self.connection)

  def print_all(self) -> str:
    result = ''
    for table_name in self.get_tables():
        table = pd.read_sql_query('SELECT * from %s' % table_name,
            self.connection)
        result += f'\n _{table_name}_ \n{table.to_markdown(index=False)}\n'
    return result

  def bruker_exists(self, attributes):
    self.cursor.execute('''
    SELECT Epost, Passord
    FROM Bruker
    ''')
    all_users = self.cursor.fetchall()
    for user in all_users:
      if user[0] == attributes[0] and user[1] == attributes[1]:
        return True
    return False

  def kaffesmaking_exists(self, attributes):
    self.cursor.execute('''
      SELECT *
      FROM Kaffesmaking
      WHERE Epost = ? AND KaffebrenneriNavn = ? AND KaffeNavn = ?
    ''', attributes)
    return bool(self.cursor.fetchone())

  def delete_kaffesmaking(self, attributes):
    self.cursor.execute('''
      DELETE *
      FROM Kaffesmaking
      WHERE Epost = ? AND KaffebrenneriNavn = ? AND KaffeNavn = ?
    ''', attributes)
    self.connection.commit()

  def kaffe_exists(self, attributes):
    self.cursor.execute('''
    SELECT * 
    FROM Kaffe
    WHERE KaffebrenneriNavn = ? AND Navn = ? 
    ''', attributes)
    return bool(self.cursor.fetchone())

  def kaffegaard_exists(self, attributes):
    self.cursor.execute('''
    SELECT * 
    FROM Kaffegaard
    WHERE Navn = ?
    ''', attributes)
    return bool(self.cursor.fetchone())

  def insert_defaults(self):
    self.insert_bruker(['admin', 'admin', 'admin', 'admin'])

    # oppretter alle Kaffeboennetypene

    self.insert_kaffeboenne(['Coffea arabica'])
    self.insert_kaffeboenne(['Coffea liberica'])
    self.insert_kaffeboenne(['Coffea robusta'])

    # oppretter to foredlingsmetoder, vasket og bærtørket
    
    self.insert_foredlingsmetode(['vasket', None])
    self.insert_foredlingsmetode(['bærtørket', None])
    
    # Brukerhistorie 1:
    # TODO: Change defaults

    self.insert_kaffegaard(['Nombre Dios', 1500, 'El Salvador', 'Santa Ana'])
    self.insert_dyrketAv(['Coffea arabica', 'Nombre de Dios'])
    kaffeparti_id = self.insert_kaffeparti([2021, 72, 'Nombre Dios', 'bærtørket'])
    if kaffeparti_id != None:
      self.insert_partiBestaarAv(['Coffea arabica', kaffeparti_id])
      self.insert_kaffe(['Jacobsen & Svart', 'Vinterkaffe', '20.01.2022', 'lysbrent', 'En velsmakende og kompleks kaffe for mørketiden', 600, kaffeparti_id])

    self.insert_kaffebrenneri(['Jacobsen & Svart'])
    self.insert_bruker(['ola@nordmann.no', 'Passord', 'Ola Nordmann', 'Norge'])
    self.insert_kaffesmaking(['ola@nordmann.no', 'Jacobsen & Svart', 'Vinterkaffe', 'Wow - en odyssé for smaksløkene:\nsitrusskall, melkesjokolade, aprikos!', 10, '20.1.2022'])

    # Brukerhistorie 4:

    self.insert_kaffegaard(['Akageragården', 1990, 'Rwanda', 'Akagera'])
    self.insert_kaffegaard(['Bogotagården', 1990, 'Columbia', 'Bogota'])
    
    kaffeparti_id = self.insert_kaffeparti([2021, 72, 'Akageragården', 'bærtørket'])
    if kaffeparti_id != None:
      self.insert_kaffe(['Jacobsen & Svart', 'Sommerkaffe', '10.02.2022', 'mørkbrent', 'God om sommeren.', 400,  kaffeparti_id])

    kaffeparti_id = self.insert_kaffeparti([2019, 10, 'Bogotagården', 'vasket'])
    if kaffeparti_id != None:
      self.insert_kaffe(['Jacobsen & Svart', 'Bogotakaffe', '10.02.2020', 'mørkbrent', 'God i Bogota.', 300, kaffeparti_id])
