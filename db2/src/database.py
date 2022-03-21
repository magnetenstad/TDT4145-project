import sqlite3
import pandas as pd

class Database:

  def __init__(self, path) -> None:
    self.connection = sqlite3.connect(path)
    self.cursor = self.connection.cursor()
    self.uuid = 0 # NOTE: This only works in memory
    self.create_tables()
    self.insert_defaults()

  def close(self):
    self.connection.close()

  def create_tables(self):
    with open('db2/src/tables.sql', 'r') as file:
      for i, statement in enumerate(file.read().split(';')):
        try:
          self.cursor.execute(statement)
        except Exception as e:
          print(f'[DB] [ERROR] in create table {i}: {statement}')
          print(e)
      print('\n[DB] Successfully built tables!\n')

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

    self.insert_kaffegaard(['Nombre Dios', 1500, 'El Salvador', 'Santa Ana'])
    self.insert_dyrketAv(['Coffea arabica', 'Nombre de Dios'])
    uuid = self.insert_kaffeparti([2021, 72, 'Nombre Dios', 'bærtørket'])
    self.insert_partiBestaarAv(['Coffea arabica', uuid])
    self.insert_kaffe(['Vinterkaffe', '20.01.2022', 'lysbrent', 'En velsmakende og kompleks kaffe for mørketiden', 600, 'Jacobsen & Svart', uuid])
    self.insert_kaffebrenneri(['Jacobsen & Svart'])
    self.insert_bruker(['ola@nordmann.no', 'Passord', 'Ola Nordmann', 'Norge'])
    self.insert_kaffesmaking(['ola@nordmann.no', 'Jacobsen & Svart', 'Vinterkaffe', 'Wow - en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!', 10, '20.1.2022'])

    # Brukerhistorie 4:

    self.insert_kaffegaard(['Akageragården', 1990, 'Rwanda', 'Akagera'])
    uuid = self.insert_kaffeparti([2021, 72, 'Akageragården', 'bærtørket'])
    self.insert_kaffe(['Sommerkaffe', '10.02.2022', 'mørkbrent', 'God om sommeren.', 400, 'Jacobsen & Svart', uuid])

    self.insert_kaffegaard(['Bogotagården', 1990, 'Columbia', 'Bogota'])
    uuid = self.insert_kaffeparti([2019, 10, 'Bogotagården', 'vasket'])
    self.insert_kaffe(['Bogotakaffe', '10.02.2020', 'mørkbrent', 'God i Bogota.', 300, 'Jacobsen & Svart', uuid])

  def insert_kaffe(self, attributes):
    self.cursor.execute('''
    INSERT INTO Kaffe
      (Navn, Dato, Brenningsgrad, Beskrivelse, Kilopris, KaffebrenneriNavn, KaffepartiID) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (attributes))

  def insert_kaffebrenneri(self, attributes):
    self.cursor.execute('''
    INSERT INTO Kaffebrenneri
      (Navn)
    VALUES
      (?)
    ''', attributes)

  def insert_kaffeparti(self, attributes) -> int:
    self.uuid += 1
    self.cursor.execute('''
    INSERT OR IGNORE INTO Kaffeparti
      (ID, Innhoestingsaar, Kilopris, KaffegaardNavn, ForedlingsmetodeNavn)
    VALUES
      (?, ?, ?, ?, ?)
    ''', [self.uuid] + attributes)
    return self.uuid
  
  def insert_kaffeboenne(self, attributes):
    self.cursor.execute('''
    INSERT INTO Kaffeboenne
      ('Art')
    VALUES
      (?)
    ''', attributes)

  def insert_kaffegaard(self, attributes):
    self.cursor.execute('''
    INSERT INTO Kaffegaard
      (Navn, HoeydeOverHavet, Land, Region)
    VALUES
      (?, ?, ?, ?)
    ''', attributes)

  def insert_bruker(self, attributes):
    self.cursor.execute('''
    INSERT INTO Bruker
      (Epost, Passord, FulltNavn, Land)
    VALUES
      (?, ?, ?, ?)
    ''', attributes)

  def insert_foredlingsmetode(self, attributes):
    self.cursor.execute('''
    INSERT INTO Foredlingsmetode
      (Navn, Beskrivelse)
    VALUES
      (?, ?)
    ''', attributes)

  def insert_kaffesmaking(self, attributes):
    self.cursor.execute('''
    INSERT INTO Kaffesmaking
      (Epost, KaffebrenneriNavn, KaffeNavn, Smaksnotater, Poeng, Dato)
    VALUES
      (?, ?, ?, ?, ?, ?)
    ''', attributes)

  def insert_dyrketAv(self, attributes):
    self.cursor.execute('''
    INSERT INTO DyrketAv
      (KaffeboenneArt, KaffegaardNavn)
    VALUES
      (?, ?)
    ''', attributes)

  def insert_partiBestaarAv(self, attributes):
    self.cursor.execute('''
    INSERT INTO PartiBestaarAv
      (KaffeboenneArt, KaffepartiId)
    VALUES
      (?,?)
    ''', attributes)

  ### Getters ###

  def get_kaffer(self):
    self.cursor.execute('''
    SELECT * 
    FROM Kaffe
    ''')
    return self.cursor.fetchall()
  
  def get_kaffesmakinger(self):
    self.cursor.execute('''
    SELECT * 
    FROM Kaffesmaking
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

  def get_unique_coffees_per_user(self):
    self.cursor.execute('''
    SELECT FulltNavn, COUNT(*) AS Antall
    FROM Kaffesmaking INNER JOIN Bruker USING (Epost)
    WHERE Dato LIKE '%2022'
    GROUP BY Epost
    ORDER BY Antall DESC
    ''')
    return self.cursor.fetchall()

  def get_value_per_money(self):
    self.cursor.execute('''
    SELECT Kaffe.KaffebrenneriNavn, Kaffe.Kilopris, AVG(Poeng) AS GjPoeng  
    FROM Kaffe INNER JOIN Kaffesmaking
    ON Kaffe.KaffebrenneriNavn = KaffeSmaking.KaffebrenneriNavn
      AND Kaffe.Navn = KaffeSmaking.KaffeNavn 
    GROUP BY Kaffe.KaffebrenneriNavn, Kaffe.Navn
    ORDER BY GjPoeng DESC
    ''')
    return self.cursor.fetchall()

  def get_floral_description(self):
    self.cursor.execute('''
    SELECT Kaffe.KaffebrenneriNavn, Kaffe.Navn
    FROM Kaffe LEFT OUTER JOIN Kaffesmaking
    ON Kaffe.KaffebrenneriNavn = KaffeSmaking.KaffebrenneriNavn
      AND Kaffe.Navn = KaffeSmaking.KaffeNavn 
    WHERE Kaffe.Beskrivelse LIKE '%floral%'
      OR Kaffesmaking.Smaksnotater LIKE '%floral%'
    ''')
    return self.cursor.fetchall()

  def get_not_washed_rwanda_colombia(self):
    self.cursor.execute('''
    SELECT Kaffe.Navn, Kaffe.KaffebrenneriNavn
    FROM (Kaffe INNER JOIN Kaffeparti) INNER JOIN Kaffegaard
    ON Kaffe.KaffepartiID = Kaffeparti.ID AND Kaffeparti.KaffegaardNavn = Kaffegaard.Navn
    WHERE (Kaffegaard.Land='Rwanda' OR Kaffegaard.Land='Colombia') 
      AND Kaffeparti.ForedlingsmetodeNavn != 'vasket'
    ''')
    return self.cursor.fetchall()

  def login(self, attributes):
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

  def print_all(self):
    # TODO
    self.connection.commit()
    return pd.read_sql_query("SELECT * FROM sqlite_master WHERE type='table'", self.connection)
