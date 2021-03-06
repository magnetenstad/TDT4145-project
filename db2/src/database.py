import sqlite3
import pandas as pd

class Database:

  def __init__(self, path):
    self.verbose = True
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
      if self.verbose: print('\nā Successfully built tables!\n')

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
      if self.verbose: print(f'\nā Satt inn kaffen {attributes} \n')
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn kaffen {attributes}! Kanskje den allerede finnes?')
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
      if self.verbose: print(f'\nā Satt inn kaffebrenneriet {attributes} \n')
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn kaffebrenneriet {attributes}! Kanskje det allerede finnes?')
      print(f'\n Feilmelding: \n {e}')

  def insert_kaffeparti(self, attributes) -> int:
    """attributes: [Innhoestingsaar, Kilopris, KaffegaardNavn, ForedlingsmetodeNavn]"""
    try:
      kaffeparti_id = self.get_uuid()
      self.cursor.execute('''
      INSERT INTO Kaffeparti
        (Id, Innhoestingsaar, Kilopris, KaffegaardNavn, ForedlingsmetodeNavn)
      VALUES
        (?, ?, ?, ?, ?)
      ''', [kaffeparti_id] + attributes)
      self.connection.commit()
      if self.verbose: print(f'\nā Satt inn kaffepartiet {attributes} \n')
      return kaffeparti_id
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn kaffepartiet {attributes}! Kanskje det allerede finnes?')
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
      if self.verbose: print(f'\nā Satt inn kaffebĆønnen {attributes} \n')
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn kaffebĆønnen {attributes}! Kanskje den allerede finnes?')
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
      if self.verbose: print(f'\nā Satt inn kaffegĆ„rden {attributes} \n')
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn kaffegĆ„rden {attributes}! Kanskje den allerede finnes?')
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
      if self.verbose: print(f'\nā Satt inn brukeren {attributes} \n')
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn brukeren {attributes}! Kanskje den allerede finnes?')
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
      if self.verbose: print(f'\nā Satt inn foredlingsmetoden {attributes} \n')
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn foredlingsmetoden {attributes}! Kanskje den allerede finnes?')
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
      if self.verbose: print(f'\nā Satt inn kaffesmakingen {attributes} \n')
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn kaffesmakingen {attributes}! Kanskje den allerede finnes?')
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
      if self.verbose: print(f'\nā Satt inn at kaffegĆ„rden {attributes[1]} dyrker kaffebĆønnen {attributes[0]} \n')
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn at kaffegĆ„rden {attributes[1]} dyrker kaffebĆønnen {attributes[0]}! Kanskje det allerede er satt inn?')
      print(f'\n Feilmelding: \n {e}')
  
  def insert_partiBestaarAv(self, attributes):
    """attributes: [KaffepartiId, KaffeboenneArt]"""
    try:
      self.cursor.execute('''
      INSERT INTO PartiBestaarAv
        (KaffepartiId, KaffeboenneArt)
      VALUES
        (?,?)
      ''', attributes)
      self.connection.commit()
      if self.verbose: print(f'\nā Satt inn at kaffebĆønnen {attributes[1]} er del av parti {attributes[0]} \n')
    except Exception as e:
      print(f'\n ā Kunne ikke sette inn kaffbĆønnen {attributes[0]} i pati {attributes[1]}! Kanskje den allerede er satt inn?')
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
        SELECT FulltNavn, MAX(Antall) AS Antall
        FROM (
          SELECT Epost, FulltNavn, 0 AS Antall
          FROM Bruker
          UNION
          SELECT Epost, FulltNavn, COUNT(*) AS Antall
          FROM Bruker INNER JOIN Kaffesmaking USING (Epost)
          WHERE Dato LIKE '2022%'
          GROUP BY Epost
        )
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
        ORDER BY GjPoeng/Kaffe.Kilopris DESC
        ''', self.connection)

  def get_floral_description(self) -> pd.DataFrame:
    return pd.read_sql_query('''
        SELECT DISTINCT Kaffe.KaffebrenneriNavn, Kaffe.Navn
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
          AND Kaffeparti.ForedlingsmetodeNavn != 'Vasket'
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
    SELECT *
    FROM Bruker
    WHERE Epost = ? AND Passord = ?
    ''', attributes)
    return self.cursor.fetchone() != None

  def kaffesmaking_exists(self, attributes):
    self.cursor.execute('''
      SELECT *
      FROM Kaffesmaking
      WHERE Epost = ? AND KaffebrenneriNavn = ? AND KaffeNavn = ?
    ''', attributes)
    return bool(self.cursor.fetchone())

  def delete_kaffesmaking(self, attributes):
    self.cursor.execute('''
    DELETE FROM Kaffesmaking
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
    self.verbose = False

    # Admin-bruker
    self.insert_bruker(['admin', 'admin', 'admin', 'admin'])

    # Kun 3 kaffebĆønnetyper:
    self.insert_kaffeboenne(['Coffea arabica'])
    self.insert_kaffeboenne(['Coffea liberica'])
    self.insert_kaffeboenne(['Coffea robusta'])

    # Tar utgangspunkt i 4 foredlingsmetoder, kilde: https://kaffe.no/foredling/
    self.insert_foredlingsmetode(['BĆ¦rtĆørket', '''Den eldste og enkleste
foredlingsmetoden som tradisjonelt har hatt stĆørst utbredelse i omrĆ„der
med lite regn som Brasil og Indonesia.'''])
    
    self.insert_foredlingsmetode(['Vasket', '''God kontroll pĆ„ prosessen gir
stabil kvalitet. Vasket kaffe kjennetegnes ved en frisk og ren smak
med markant syre.'''])
    
    self.insert_foredlingsmetode(['Pulped natural', '''Kan ha mer kropp
og lavere syre enn vasket kaffe, og en renere, mer ensartet cup
enn bĆ¦rtĆørket.'''])
    
    self.insert_foredlingsmetode(['Delvis vasket', '''Kan gi kaffe med
intens sĆødme, god munnfĆølelse og balansert syre.'''])
    
    # Kaffebrennerier
    self.insert_kaffebrenneri(['Jacobsen & Svart']) # TODO: Trondheim?
    self.insert_kaffebrenneri(['Realfagsbrenneriet'])

    # KaffegĆ„rder, kaffepartier og kaffer

    self.insert_kaffegaard(['Nombre Dios', 1500, 'El Salvador', 'Santa Ana'])
    self.insert_dyrketAv(['Coffea arabica', 'Nombre de Dios'])
    id = self.insert_kaffeparti([2021, 72, 'Nombre Dios', 'BĆ¦rtĆørket'])
    self.insert_partiBestaarAv([id, 'Coffea arabica'])
    self.insert_kaffe(['Jacobsen & Svart', 'Vinterkaffe 2022', '2022.01.20',
        'lysbrent', 'En velsmakende og kompleks kaffe for mĆørketiden.',
        600, id])
      # Kilde: Oppgavetekst
    
    self.insert_kaffegaard(['Fazendas Dutra', 1100, 'Brasil', 'Minas Gerais'])
    self.insert_dyrketAv(['Coffea arabica', 'Fazendas Dutra'])
    id = self.insert_kaffeparti([2020, 60, 'Fazendas Dutra', 'Pulped natural'])
    self.insert_partiBestaarAv([id, 'Coffea arabica'])
    self.insert_kaffe(['Jacobsen & Svart', 'Diamond Santos',
        '2021.02.01', 'lysbrent',
        'En temmelig stabil og streit kaffe.',
        349, id])
      # Kilde: https://jacobsensvart.no/products/copy-of-1-kg-jose-vasquez-peru

    self.insert_kaffegaard(['Fernandez Familia', 1100, 'Peru', 'Colosay'])
    self.insert_dyrketAv(['Coffea arabica', 'Fernandez Familia'])
    id = self.insert_kaffeparti([2021, 69, 'Fernandez Familia', 'Vasket'])
    self.insert_partiBestaarAv([id, 'Coffea arabica'])
    self.insert_kaffe(['Jacobsen & Svart', 'La Palma', '2021.02.01',
        'lysbrent', 'Forfriskende og delikat.', 598, id])
      # Kilde: https://jacobsensvart.no/products/copy-of-1-kg-jose-vasquez-peru

    self.insert_kaffegaard(['Kivubelt', 1567, 'Rwanda', 'Kigali'])
    self.insert_dyrketAv(['Coffea arabica', 'Kivubelt'])
      # Kilde: https://www.mukasa.no/kaffe-fra-rwanda/
    id = self.insert_kaffeparti([2020, 50, 'Kivubelt', 'BĆ¦rtĆørket'])
    self.insert_partiBestaarAv([id, 'Coffea arabica'])
    self.insert_kaffe(['Realfagsbrenneriet', 'Data-kaffe',
        '2021.02.01', 'mĆørkbrent',
        'En kaffe for datateknologi-studenter.',
        600, id])

    self.insert_kaffegaard(['El Placer', 2115, 'Colombia', 'Tolima'])
    self.insert_dyrketAv(['Coffea arabica', 'El Placer'])
      # Kilde: https://sh.no/journal/kaffe-med-kjaerlighet-fra-colombia/
    id = self.insert_kaffeparti([2019, 62, 'El Placer', 'Vasket'])
    self.insert_partiBestaarAv([id, 'Coffea arabica'])
    self.insert_kaffe(['Realfagsbrenneriet', 'Kyb-kaffe',
        '2022.01.02', 'lysbrent',
        'En kaffe for kybernetikk-studenter.',
        412, id])

    self.insert_kaffegaard(['Amadeo', 400, 'Filippinene', 'Calabarzon'])
    self.insert_dyrketAv(['Coffea robusta', 'Amadeo'])
    self.insert_dyrketAv(['Coffea liberica', 'Amadeo'])
      # Kilde: https://philcoffeeboard.com/philippine-coffee/
    id = self.insert_kaffeparti([2021, 58, 'Amadeo', 'Delvis vasket'])
    self.insert_partiBestaarAv([id, 'Coffea robusta'])
    self.insert_partiBestaarAv([id, 'Coffea liberica'])
    self.insert_kaffe(['Realfagsbrenneriet', 'IndĆøk-kaffe',
        '2022.02.12', 'lysbrent',
        'En kaffe for indĆøk-studenter.',
        789, id])
    
    self.insert_kaffegaard(['Dak Lak', 1600, 'Vietnam', 'BuĆ“n MĆŖ Thuį»t'])
    self.insert_dyrketAv(['Coffea arabica', 'Dak Lak'])
    self.insert_dyrketAv(['Coffea robusta', 'Dak Lak'])
    self.insert_dyrketAv(['Coffea liberica', 'Dak Lak'])
      # Kilde: http://amarin.com.vn/buon-ma-thuot-coffee
    id = self.insert_kaffeparti([2022, 78, 'Dak Lak', 'Vasket'])
    self.insert_partiBestaarAv([id, 'Coffea arabica'])
    self.insert_partiBestaarAv([id, 'Coffea robusta'])
    self.insert_partiBestaarAv([id, 'Coffea liberica'])
    self.insert_kaffe(['Realfagsbrenneriet', 'I&IKT-kaffe',
        '2022.03.12', 'mĆørkbrent',
        'En kaffe for ingeniĆørvitenskap-og-ikt-studenter.',
        359, id])
    
    # Brukere og kaffesmakinger

    self.insert_bruker(['magneet@ntnu.no', 
        'Password123', 'Magne ErlendsĆønn Tenstad', 'Norge'])
    self.insert_kaffesmaking(['magneet@ntnu.no',
        'Jacobsen & Svart', 'Vinterkaffe 2022',
        'Hadde en rar bismak.', 3, '2022.03.16'])
    self.insert_kaffesmaking(['magneet@ntnu.no',
        'Jacobsen & Svart', 'La Palma',
        'Forfriskende og floral!', 8, '2022.03.17'])
    self.insert_kaffesmaking(['magneet@ntnu.no',
        'Jacobsen & Svart', 'Diamond Santos',
        'God kaffe for prisen.', 7, '2022.03.18'])
    self.insert_kaffesmaking(['magneet@ntnu.no',
        'Realfagsbrenneriet', 'Data-kaffe',
        'Beste kaffen jeg har smakt!', 10, '2022.03.20'])
    self.insert_kaffesmaking(['magneet@ntnu.no',
        'Realfagsbrenneriet', 'Kyb-kaffe',
        'Litt robotisk.', 4, '2022.03.21'])
    self.insert_kaffesmaking(['magneet@ntnu.no',
        'Realfagsbrenneriet', 'I&IKT-kaffe',
        'Ikke det verste jeg har smakt.', 6, '2022.03.22'])
    self.insert_kaffesmaking(['magneet@ntnu.no',
        'Realfagsbrenneriet', 'IndĆøk-kaffe',
        'Fysj og fy, dette var dĆ„rlig.', 2, '2022.03.24'])

    self.insert_bruker(['kslie@ntnu.no', 
        'mobil123', 'Karin Syversveen Lie','Norge'])
    self.insert_kaffesmaking(['kslie@ntnu.no',
        'Jacobsen & Svart', 'Vinterkaffe 2022',
        'Smakte godt.', 8, '2022.01.12'])
    self.insert_kaffesmaking(['kslie@ntnu.no',
        'Jacobsen & Svart', 'La Palma',
        'Floral er den i hvertfall!', 8, '2022.03.10'])
    self.insert_kaffesmaking(['kslie@ntnu.no',
        'Jacobsen & Svart', 'Diamond Santos',
        'Hadde rar ettersmak.', 3, '2022.03.18'])
    self.insert_kaffesmaking(['kslie@ntnu.no',
        'Realfagsbrenneriet', 'Data-kaffe',
        'Den var fruktig, men litt bitter!', 8, '2022.03.20'])
    self.insert_kaffesmaking(['kslie@ntnu.no',
        'Realfagsbrenneriet', 'Kyb-kaffe',
        'Passer kanskje ikke for alle.', 4, '2022.03.21'])
    self.insert_kaffesmaking(['kslie@ntnu.no',
        'Realfagsbrenneriet', 'I&IKT-kaffe',
        'Smaker nesten som butterbeer', 9, '2022.03.22'])
    self.insert_kaffesmaking(['kslie@ntnu.no',
        'Realfagsbrenneriet', 'IndĆøk-kaffe',
        'Not my cup of coffee.', 3, '2022.03.24'])
    
    self.insert_bruker(['karoliys@ntnu.no', 
        'Passord1', 'Karoline Stabell', 'Norge'])
    self.insert_kaffesmaking(['karoliys@ntnu.no',
        'Jacobsen & Svart', 'Vinterkaffe 2022', 
        'Rund og god kaffe, litt bitter', 5, '2022.03.02'])
    self.insert_kaffesmaking(['karoliys@ntnu.no',
        'Jacobsen & Svart', 'Diamond Santos',
        'God kaffe for prisen.', 7, '2021.03.16'])
    self.insert_kaffesmaking(['karoliys@ntnu.no',
        'Realfagsbrenneriet', 'Data-kaffe',
        'Bitter med et hint av appelsin', 4, '2021.05.20'])
    self.insert_kaffesmaking(['karoliys@ntnu.no',
        'Realfagsbrenneriet', 'Kyb-kaffe',
        'Besk med hint av metall', 3, '2022.02.27'])
    self.insert_kaffesmaking(['karoliys@ntnu.no',
        'Realfagsbrenneriet', 'I&IKT-kaffe',
        'En sĆøt og god blandingskaffe med hint av karamell', 8, '2022.03.23'])
    self.insert_kaffesmaking(['karoliys@ntnu.no',
        'Realfagsbrenneriet', 'IndĆøk-kaffe',
        'Beste kaffen pĆ„ GlĆøs!', 9, '2022.02.24'])
    
    print('\nā Inserted defaults.\n')
    self.verbose = True
