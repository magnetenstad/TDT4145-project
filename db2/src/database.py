

class Database:

  def __init__(self, cursor) -> None:
    self.cursor = cursor
    self.build_tables()
    self.insert_defaults()
  
  def build_tables(self):
    with open('db2/src/tables.sql', 'r') as file:
      for i, statement in enumerate(file.read().split(';')):
        try:
          self.cursor.execute(statement)
        except Exception as e:
          print(f'[ERROR] in create table {i}: {statement}')
          print(str(e))
      print('\nSuccessfully build tables!\n')

  def insert_defaults(self):
    # oppretter alle kaffebønnetypene

    self.insert_kaffebonne(['Coffea arabica'])
    self.insert_kaffebonne(['Coffea liberica'])
    self.insert_kaffebonne(['Coffea robusta'])

    # oppretter to foredlingsmetoder, vasket og bærtørket
    
    self.insert_foredlingsmetode(['vasket', None])
    self.insert_foredlingsmetode(['bærtørket', None])
    
    # Brukerhistorie 1:

    self.insert_kaffegard(['Nombre Dios', 1500, 'El Salvador', 'Santa Ana'])
    self.insert_kaffeparti([1, 2021, 72, 'Nombre Dios', 'bærtørket'])
    self.insert_kaffe(['Vinterkaffe', '20.01.2022', 'lysbrent', 'En velsmakende og kompleks kaffe for mørketiden', 600, 'Jacobsen & Svart', 1])
    self.insert_kaffebrenneri(['Jacobsen & Svart'])
    self.insert_bruker(['ola@nordmann.no', 'Passord', 'Ola Nordmann', 'Norge'])
    self.insert_kaffesmaking(['ola@nordmann.no', 'Jacobsen & Svart', 'Vinterkaffe', 'Wow - en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!', 10, '20.1.2022'])
    self.insert_dyrketAv(['Coffea arabica', 'Nombre de Dios'])
    self.insert_partiBestarAv(['Coffea arabica', 1])

    # Brukerhistorie 4:

    self.insert_kaffegard(['Akageragården', 1990, 'Rwanda', 'Akagera'])
    self.insert_kaffeparti([2, 2021, 72, 'Akageragården', 'bærtørket'])
    self.insert_kaffe(['Sommerkaffe', '10.02.2022', 'mørkbrent', 'God om sommeren.', 400, 'Jacobsen & Svart', 2])

    self.insert_kaffegard(['Bogotagården', 1990, 'Columbia', 'Bogota'])
    self.insert_kaffeparti([3, 2019, 10, 'Bogotagården', 'vasket'])
    self.insert_kaffe(['Bogotakaffe', '10.02.2020', 'mørkbrent', 'God i Bogota.', 300, 'Jacobsen & Svart', 2])

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

  def insert_kaffeparti(self, attributes):
    self.cursor.execute('''
    INSERT INTO Kaffeparti
      (ID, Innhøstingsår, Kilopris, KaffegårdNavn, ForedlingsmetodeNavn)
    VALUES
      (?, ?, ?, ?, ?)
    ''', attributes)
    
  def insert_kaffebonne(self, attributes):
    self.cursor.execute('''
    INSERT INTO Kaffebønne
      ('Art')
    VALUES
      (?)
    ''', attributes)

  def insert_kaffegard(self, attributes):
    self.cursor.execute('''
    INSERT INTO Kaffegård
      (Navn, HøydeOverHavet, Land, Region)
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
      (KaffebønneArt, KaffegårdNavn)
    VALUES
      (?, ?)
    ''', attributes)

  def insert_partiBestarAv(self, attributes):
    self.cursor.execute('''
    INSERT INTO PartiBestårAv
      (KaffebønneArt, KaffepartiId)
    VALUES
      (?,?)
    ''', attributes)

  ### Selects ###

  def get_kaffe(self):
    self.cursor.execute('''
    SELECT * FROM Kaffe
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
    FROM Kaffe INNER JOIN Kaffesmaking
    ON Kaffe.KaffebrenneriNavn = KaffeSmaking.KaffebrenneriNavn
      AND Kaffe.Navn = KaffeSmaking.KaffeNavn 
    WHERE Kaffe.Beskrivelse LIKE '%floral%'
      OR Kaffesmaking.Smaksnotater LIKE '%floral%'
    ''')
    return self.cursor.fetchall()

  def get_not_washed_rwanda_colombia(self):
    self.cursor.execute('''
    SELECT Kaffe.Navn, Kaffe.KaffebrenneriNavn
    FROM (Kaffe INNER JOIN Kaffeparti) INNER JOIN Kaffegård
    ON Kaffe.KaffepartiID = Kaffeparti.ID AND Kaffeparti.KaffegårdNavn = Kaffegård.Navn
    WHERE (Kaffegård.Land='Rwanda' OR Kaffegård.Land='Colombia') 
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
