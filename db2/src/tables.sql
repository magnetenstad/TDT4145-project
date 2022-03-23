
CREATE TABLE IF NOT EXISTS Kaffeboenne(
Art   TEXT NOT NULL,
CONSTRAINT Kaffeboenne_PK PRIMARY KEY (Art)
);

CREATE TABLE IF NOT EXISTS Kaffegaard(
Navn            TEXT NOT NULL,
HoeydeOverHavet  REAL,
Land            TEXT,
Region          TEXT,
CONSTRAINT Kaffegaard_PK PRIMARY KEY (Navn)
);

CREATE TABLE IF NOT EXISTS Kaffeparti(
Id                    INTEGER NOT NULL,
Innhoestingsaar       INTEGER,
Kilopris              REAL,
KaffegaardNavn        TEXT,
ForedlingsmetodeNavn  TEXT,
CONSTRAINT Kaffeparti_PK PRIMARY KEY (Id)
CONSTRAINT Foredlingsmetode_FK FOREIGN KEY (ForedlingsmetodeNavn) REFERENCES Foredlingsmetode(Navn)
  ON UPDATE CASCADE
  ON DELETE RESTRICT
-- Vil oppdatere fremmednøkkel dersom Foredlingsmetode(Navn) endres
-- Vi tillater ikke å slette foredlingsmetoder
);

CREATE TABLE IF NOT EXISTS Kaffe(
KaffebrenneriNavn   TEXT NOT NULL,
Navn                TEXT NOT NULL,
Dato                TEXT,
Brenningsgrad       TEXT,
Beskrivelse         TEXT,
Kilopris            REAL,
KaffePartiId        TEXT,
CONSTRAINT Kaffe_PK PRIMARY KEY (KaffebrenneriNavn, Navn),
CONSTRAINT Kaffebrenneri_FK FOREIGN KEY (KaffebrenneriNavn) REFERENCES Kaffebrenneri(Navn)
  ON UPDATE CASCADE
  ON DELETE RESTRICT
-- Vil oppdatere fremmednøkkel dersom Kaffebrenneri endres 
-- Vi tillater ikke sletting av kaffebrennerier
);

CREATE TABLE IF NOT EXISTS Kaffebrenneri(
Navn  TEXT NOT NULL,
CONSTRAINT Kaffebrenneri_PK PRIMARY KEY (Navn)
);

CREATE TABLE IF NOT EXISTS Bruker(
Epost       TEXT NOT NULL,
Passord     TEXT,
FulltNavn   TEXT,
Land        TEXT,
CONSTRAINT Bruker_PK PRIMARY KEY (Epost)
);

CREATE TABLE IF NOT EXISTS Foredlingsmetode(
Navn          TEXT NOT NULL,
Beskrivelse   TEXT,
CONSTRAINT Foredlingsmetode_PK PRIMARY KEY (Navn)
);

CREATE TABLE IF NOT EXISTS Kaffesmaking(
Epost               TEXT NOT NULL,
KaffebrenneriNavn   TEXT NOT NULL,
KaffeNavn           TEXT NOT NULL,
Smaksnotater        TEXT,
Poeng               INTEGER,
Dato                TEXT,
CONSTRAINT Kaffesmaking_PK PRIMARY KEY (Epost, KaffebrenneriNavn, KaffeNavn),
CONSTRAINT Kaffe_FK FOREIGN KEY (KaffebrenneriNavn, KaffeNavn) REFERENCES Kaffe(KaffebrenneriNavn, Navn)
  ON UPDATE CASCADE
  ON DELETE RESTRICT,
-- Vil oppdatere fremmednøkkel dersom en kaffe endres
-- Vi tillater ikke å slette kaffer
CONSTRAINT Bruker_FK FOREIGN KEY (Epost) REFERENCES Bruker(Epost)
  ON UPDATE CASCADE
  ON DELETE CASCADE
-- Vil oppdatere fremmednøkkel dersom en bruker endrer epost
-- Hvis en bruker slettes, så slettes også alle tilhørende kaffesmakinger
);

CREATE TABLE IF NOT EXISTS DyrketAv(
KaffeboenneArt   TEXT NOT NULL,
KaffegaardNavn   TEXT NOT NULL,
CONSTRAINT DyrketAv_PK PRIMARY KEY (KaffeboenneArt, KaffegaardNavn),
CONSTRAINT Kaffeboenne_FK FOREIGN KEY (KaffeboenneArt) REFERENCES Kaffeboenne(Art)
  ON UPDATE RESTRICT
  ON DELETE RESTRICT,
-- Vi tillater ikke endring av Kaffeboenneart, da disse er gitt en av 3 (total og disjunkt Kaffeboenne) 
-- Vi tillater ikke sletting av kaffebrennerier
CONSTRAINT Kaffegaard_FK FOREIGN KEY (KaffegaardNavn) REFERENCES Kaffegaard(Navn)
  ON UPDATE CASCADE
  ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS PartiBestaarAv(
KaffeboenneArt   TEXT NOT NULL,
KaffepartiId    TEXT NOT NULL,
CONSTRAINT DyrketAv_PK PRIMARY KEY (KaffeboenneArt, KaffepartiId),
CONSTRAINT Kaffeboenne_FK FOREIGN KEY (KaffeboenneArt) REFERENCES Kaffeboenne(Art)
  ON UPDATE RESTRICT
  ON DELETE RESTRICT,
-- Vi tillater ikke at Kaffeboenne(Art) endres eller slettes
CONSTRAINT Kaffeparti_FK FOREIGN KEY (KaffepartiId) REFERENCES Kaffeparti(Id)
  ON UPDATE RESTRICT
  ON DELETE RESTRICT
-- Vi tillater ikke at Kaffeparti(Id) endres eller slettes
);
