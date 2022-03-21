
# TDT4145 - DB2 Gruppe 109

| Etternavn  | Fornavn                | E-post                |
| ---------- | ---------------------- | --------------------- |
| Lie        | Karin Sofie Syversveen | kslie@stud.ntnu.no    |
| Stabell    | Karoline Ytreeide      | karoliys@stud.ntnu.no |
| Tenstad    | Magne Erlendsønn       | magneet@stud.ntnu.no  |

## Sjekkliste
- [ ] Brukerhistorie 1
- [ ] Brukerhistorie 2 med SQL-spørring og data for å teste spørringen
- [ ] Brukerhistorie 3 med SQL-spørring og data for å teste spørringen
- [ ] Brukerhistorie 4 med SQL-spørring og data for å teste spørringen
- [ ] Brukerhistorie 5 med SQL-spørring og data for å teste spørringen
- [ ] Notere alle endringer som er gjort fra DB1 (se git history)
- [ ] Skrive og begrunne antakelser
- [ ] Forklare hvordan programmet kjøres og brukes

## Evalueringskriterier
- [ ] En oversikt over hvordan brukerhistoriene er løst.
- [ ] Korrekt bruk av SQL i Python.
- [ ] Forståelig og lesbar kode.
- [ ] Konsise og tydelige beskrivelser i dokumentet
- [ ] Det skal være mulig å reprodusere de leverte resultatene ved hjelp av programmet og databasen som er levert.

## Applikasjonsbeskrivelse

TODO: Registrere og logge inn som bruker eller admin.

```mermaid
flowchart LR
  main(Velkommen.)

  logged_in(Innlogget \n Hva vil du gjøre?)
  
  select(Hva vil du gjøre spørring på?)
  insert(Hva vil du sette inn?)
  update(Hva vil du oppdatere?)
  exit(Avslutter applikasjonen)

  select_1(Antall unike kaffer per bruker)
  select_2(Gjennomsnittlig poeng per kaffe)
  select_3(Kaffer beskrevet som 'floral')
  select_4(Ikke-vaskede kaffer fra Rwanda eller Colombia)

  main -->|login| logged_in
  main -->|register| logged_in

  logged_in -->|insert| insert
  logged_in -->|select| select
  logged_in -->|update| update
  logged_in -->|exit| exit
  logged_in -->|sign out| main

  select -->|1| select_1
  select -->|2| select_2
  select -->|3| select_3
  select -->|4| select_4
```

## Avhengigheter

```mermaid
flowchart TD
  Kaffebønne
  Kaffegård
  Kaffeparti
  Kaffe
  Bruker
  Kaffesmaking
  Kaffebrenneri

  Kaffe --> Kaffebrenneri
  Kaffe --> Kaffeparti
  Kaffeparti --> Kaffebønne
  Kaffeparti --> Kaffegård
  Kaffesmaking --> Bruker
  Kaffesmaking --> Kaffe
  Kaffegård --> Kaffebønne
```
