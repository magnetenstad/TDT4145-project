DROP TABLE IF EXISTS Kaffebønne;
DROP TABLE IF EXISTS Kaffegård;
DROP TABLE IF EXISTS Kaffeparti;
DROP TABLE IF EXISTS Kaffe;
DROP TABLE IF EXISTS Kaffebrenneri;
DROP TABLE IF EXISTS Bruker;
DROP TABLE IF EXISTS Foredlingsmetode;
DROP TABLE IF EXISTS Kaffesmaking;
DROP TABLE IF EXISTS DyrketAv;
DROP TABLE IF EXISTS PartiBestårAv;

CREATE TABLE Kaffebønne(
Art   TEXT NOT NULL,
CONSTRAINT Kaffebønne_PK PRIMARY KEY (Art)
);

CREATE TABLE Kaffegård(
Navn            TEXT NOT NULL,
HøydeOverHavet  TEXT,
Land            TEXT,
Region          TEXT,
CONSTRAINT Kaffegård_PK PRIMARY KEY (Navn)
);

CREATE TABLE Kaffeparti(
ID                    TEXT NOT NULL,
Innhøstingsår         TEXT,
Kilopris              REAL,
KaffegårdNavn         TEXT,
ForedlingsmetodeNavn  TEXT,
CONSTRAINT Kaffeparti_PK PRIMARY KEY (ID)
CONSTRAINT Foredlingsmetode_FK FOREIGN KEY (ForedlingsmetodeNavn) REFERENCES Foredlingsmetode(Navn)
  ON UPDATE CASCADE
  ON DELETE RESTRICT
-- Vil oppdatere fremmednøkkel dersom Foredlingsmetode(Navn) endres
-- Vi tillater ikke å slette foredlingsmetoder
);

CREATE TABLE Kaffe(
KaffebrenneriNavn   TEXT NOT NULL,
Navn                TEXT NOT NULL,
Dato                TEXT,
Brenningsgrad       TEXT,
Kilopris            REAL,
KaffePartiID        TEXT,
CONSTRAINT Kaffe_PK PRIMARY KEY (KaffebrenneriNavn, Navn),
CONSTRAINT Kaffebrenneri_FK FOREIGN KEY (KaffebrenneriNavn) REFERENCES Kaffebrenneri(Navn)
  ON UPDATE CASCADE
  ON DELETE RESTRICT
-- Vil oppdatere fremmednøkkel dersom Kaffebrenneri endres 
-- Vi tillater ikke sletting av kaffebrennerier
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
-- Vi tillater ikke å slette kaffer
CONSTRAINT Bruker_FK FOREIGN KEY (Epost) REFERENCES Bruker(Epost)
  ON UPDATE CASCADE
  ON DELETE CASCADE
-- Vil oppdatere fremmednøkkel dersom en bruker endrer epost
-- Hvis en bruker slettes, så slettes også alle tilhørende kaffesmakinger
);

CREATE TABLE DyrketAv(
KaffebønneArt   TEXT NOT NULL,
KaffegårdNavn   TEXT NOT NULL,
CONSTRAINT DyrketAv_PK PRIMARY KEY (KaffebønneArt, KaffegårdNavn),
CONSTRAINT Kaffebønne_FK FOREIGN KEY (KaffebønneArt) REFERENCES Kaffebønne(Art)
  ON UPDATE RESTRICT
  ON DELETE RESTRICT,
-- Vi tillater ikke endring av kaffebønneart, da disse er gitt en av 3 (total og disjunkt kaffebønne) 
-- Vi tillater ikke sletting av kaffebrennerier
CONSTRAINT Kaffegård_FK FOREIGN KEY (KaffegårdNavn) REFERENCES Kaffegård(Navn)
  ON UPDATE CASCADE
  ON DELETE RESTRICT
);

CREATE TABLE PartiBestårAv(
KaffebønneArt   TEXT NOT NULL,
KaffepartiID    TEXT NOT NULL,
CONSTRAINT DyrketAv_PK PRIMARY KEY (KaffebønneArt, KaffepartiID),
CONSTRAINT Kaffebønne_FK FOREIGN KEY (KaffebønneArt) REFERENCES Kaffebønne(Art)
  ON UPDATE RESTRICT
  ON DELETE RESTRICT,
-- Vi tillater ikke at Kaffebønne(Art) endres eller slettes
CONSTRAINT Kaffeparti_FK FOREIGN KEY (KaffepartiID) REFERENCES Kaffeparti(ID)
  ON UPDATE RESTRICT
  ON DELETE RESTRICT
-- Vi tillater ikke at Kaffeparti(ID) endres eller slettes
);
