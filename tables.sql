DROP TABLE IF EXISTS Kaffebønne;
DROP TABLE IF EXISTS Kaffegård;
DROP TABLE IF EXISTS Kaffeparti;
DROP TABLE IF EXISTS FerdigbrentKaffe;
DROP TABLE IF EXISTS Kaffebrenneri;
DROP TABLE IF EXISTS Bruker;
DROP TABLE IF EXISTS Foredlingsmetode;
DROP TABLE IF EXISTS Kaffesmaking;
DROP TABLE IF EXISTS DyrketAv;
DROP TABLE IF EXISTS PartiBestårAv;

CREATE TABLE Kaffebønne
(Art TEXT PRIMARY KEY);

CREATE TABLE Kaffegård
(Navn TEXT PRIMARY KEY, HøydeOverHavet TEXT, Land TEXT, Region TEXT);

CREATE TABLE Kaffeparti
(ID TEXT PRIMARY KEY, Innhøstingsår TEXT, Kilopris REAL, KaffegårdNavn TEXT, ForedlingsmetodeNavn TEXT,
CONSTRAINT Foredlingsmetode_FK FOREIGN KEY (ForedlingsmetodeNavn) REFERENCES Foredlingsmetode(Navn));

CREATE TABLE FerdigbrentKaffe
(KaffebrenneriNavn TEXT, Navn TEXT, Dato TEXT, Brenningsgrad TEXT, Kilopris REAL, KaffePartiID TEXT,
CONSTRAINT FerdigbrentKaffe_PK PRIMARY KEY (KaffebrenneriNavn, Navn, Dato),
CONSTRAINT Kaffebrenneri_FK FOREIGN KEY (KaffebrenneriNavn) REFERENCES Kaffebrenneri(Navn));

CREATE TABLE Kaffebrenneri
(Navn TEXT PRIMARY KEY);

CREATE TABLE Bruker
(Epost TEXT PRIMARY KEY, Passord TEXT, FulltNavn TEXT, Land TEXT);

CREATE TABLE Foredlingsmetode
(Navn TEXT PRIMARY KEY, Beskrivelse TEXT);

CREATE TABLE Kaffesmaking
(Epost TEXT, KaffebrenneriNavn TEXT, FerdigbrentNavn TEXT, FerdigbrentDato TEXT, Smaksnotater TEXT, Poeng INTEGER, Dato TEXT,
CONSTRAINT Kaffesmaking_PK PRIMARY KEY (Epost, KaffebrenneriNavn, FerdigbrentNavn, FerdigbrentDato),
CONSTRAINT FerdigbrentKaffe_FK FOREIGN KEY (KaffebrenneriNavn, FerdigbrentNavn, FerdigbrentDato) REFERENCES FerdigbrentKaffe(KaffebrenneriNavn, Navn, Dato),
CONSTRAINT Bruker_FK FOREIGN KEY (Epost) REFERENCES Bruker(Epost));

CREATE TABLE DyrketAv
(KaffebønneArt TEXT, KaffegårdNavn TEXT,
CONSTRAINT DyrketAv_PK PRIMARY KEY (KaffebønneArt, KaffegårdNavn),
CONSTRAINT Kaffebønne_FK FOREIGN KEY (KaffebønneArt) REFERENCES Kaffebønne(Art),
CONSTRAINT Kaffegård_FK FOREIGN KEY (KaffegårdNavn) REFERENCES Kaffegård(Navn));

CREATE TABLE PartiBestårAv
(KaffebønneArt TEXT, KaffepartiID TEXT,
CONSTRAINT DyrketAv_PK PRIMARY KEY (KaffebønneArt, KaffepartiID),
CONSTRAINT Kaffebønne_FK FOREIGN KEY (KaffebønneArt) REFERENCES Kaffebønne(Art),
CONSTRAINT Kaffeparti_FK FOREIGN KEY (KaffepartiID) REFERENCES Kaffeparti(ID));
