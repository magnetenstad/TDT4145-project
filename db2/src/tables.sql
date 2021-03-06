
CREATE TABLE Kaffeboenne(
Art   TEXT NOT NULL,
CONSTRAINT Kaffeboenne_PK PRIMARY KEY (Art)
);

CREATE TABLE Kaffegaard(
Navn            TEXT NOT NULL,
HoeydeOverHavet  REAL,
Land            TEXT,
Region          TEXT,
CONSTRAINT Kaffegaard_PK PRIMARY KEY (Navn)
);

CREATE TABLE Kaffeparti(
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
-- Vi tillater ikke å slette foredlingsmetoder som er referert til
);

CREATE TABLE Kaffe(
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
-- Vi tillater ikke sletting av kaffebrennerier som er referert til
);

CREATE TABLE Kaffebrenneri(
Navn  TEXT NOT NULL,
CONSTRAINT Kaffebrenneri_PK PRIMARY KEY (Navn)
);

CREATE TABLE Bruker(
Epost       TEXT NOT NULL,
Passord     TEXT,
FulltNavn   TEXT,
Land        TEXT,
CONSTRAINT Bruker_PK PRIMARY KEY (Epost)
);

CREATE TABLE Foredlingsmetode(
Navn          TEXT NOT NULL,
Beskrivelse   TEXT,
CONSTRAINT Foredlingsmetode_PK PRIMARY KEY (Navn)
);

CREATE TABLE Kaffesmaking(
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
-- Vi tillater ikke å slette kaffer som er referert
CONSTRAINT Bruker_FK FOREIGN KEY (Epost) REFERENCES Bruker(Epost)
  ON UPDATE CASCADE
  ON DELETE CASCADE
-- Vil oppdatere fremmednøkkel dersom en bruker endrer epost
-- Hvis en bruker slettes, så slettes også alle tilhørende kaffesmakinger
);

CREATE TABLE DyrketAv(
KaffeboenneArt   TEXT NOT NULL,
KaffegaardNavn   TEXT NOT NULL,
CONSTRAINT DyrketAv_PK PRIMARY KEY (KaffeboenneArt, KaffegaardNavn),
CONSTRAINT Kaffeboenne_FK FOREIGN KEY (KaffeboenneArt) REFERENCES Kaffeboenne(Art)
  ON UPDATE RESTRICT
  ON DELETE RESTRICT,
-- Vi tillater ikke endring av Kaffeboenneart, da disse er gitt en av 3 (total og disjunkt Kaffeboenne) 
-- Vi tillater ikke sletting av kaffebrennerier som er referert til
CONSTRAINT Kaffegaard_FK FOREIGN KEY (KaffegaardNavn) REFERENCES Kaffegaard(Navn)
  ON UPDATE CASCADE
  ON DELETE RESTRICT
-- Vil oppdatere fremmednøkkel dersom en kaffegård endrer navn
-- Vi tillater ikke sletting av kaffegårder som er referert til
);

CREATE TABLE PartiBestaarAv(
KaffeboenneArt   TEXT NOT NULL,
KaffepartiId    TEXT NOT NULL,
CONSTRAINT DyrketAv_PK PRIMARY KEY (KaffeboenneArt, KaffepartiId),
CONSTRAINT Kaffeboenne_FK FOREIGN KEY (KaffeboenneArt) REFERENCES Kaffeboenne(Art)
  ON UPDATE RESTRICT
  ON DELETE RESTRICT,
-- Vi tillater ikke at Kaffeboenne(Art) som er referert til endres eller slettes
CONSTRAINT Kaffeparti_FK FOREIGN KEY (KaffepartiId) REFERENCES Kaffeparti(Id)
  ON UPDATE RESTRICT
  ON DELETE RESTRICT
-- Vi tillater ikke at Kaffeparti(Id) som er referert til endres eller slettes
);
