
# TDT4145 - DB1 Gruppe 109

## ER-modell
![](assets/er.png)

### Antakelser
- Forskjellige kaffegårder kan ikke ha samme navn.
- Forskjellige kaffebrennerier kan ikke ha samme navn.
- Flere kaffebrennerier kan navngi kaffen sin likt, derfor er Kaffe en svak klasse.
- Alle kilopriser konverteres til samme valuta, NOK, før de lagres i databasen.
  - For å sørge for at kaffer og kaffepartier kan sorteres riktig på pris.
- En bruker kan ikke lagre flere anmeldelser av samme kaffe.
- En kaffegård kan være en kaffegård uten å ha begynt å produsere kaffe ennå.
- Kaffebrenneri kan være et kaffebrenneri før den har begynt å brenne kaffe.  
- Det finnes bare tre kaffebønnearter: Coffea arabica, Coffea liberica og Coffea robusta.
- Kaffeparti krever en generert nøkkel.

<div style="page-break-after: always;"></div>

## Relasjonsdatabasemodeller
- **Kaffebønne** (<ins>Art</ins>) 
  *Navn på arten er nøkkel til Kaffebønne. Hver art har et unikt navn.*
- **Kaffegård** (<ins>Navn</ins>, HøydeOverHavet, Land, Region)
  *Navn er nøkkel til Kaffegård, og vi antar dermed at ingen kaffegårder har samme navn.* 
- **Kaffeparti** (<ins>ID</ins>, Innhøstingsår, Kilopris, KaffegårdNavn, ForedlingsmetodeNavn)
  *ID er en generert nøkkel til Kaffeparti.*
  *KaffegårdNavn er fremmednøkkel mot Kaffegård (ProdusertAv).*
  *ForedlingsmetodeNavn er fremmednøkkel mot Foredlingsmetode (ForedletMed).*
- **Kaffe** (<ins>Navn</ins>, <ins>Dato</ins>, Brenningsgrad, Beskrivelse, Kilopris, KaffebrenneriNavn, KaffepartiID)
  *Navn og Dato er svake nøkler for Kaffe.*
  *Kaffebrennerinavn er identifiserende fremmednøkkel mot Kaffebrenneri (BrentAv).*
  *KaffepartiID er fremmednøkkel mot Kaffeparti (FremstiltAv).*
- **Kaffebrenneri** (<ins>Navn</ins>)
  *Navn er nøkkel til Kaffebrenneri, og det er antatt at ingen Kaffebrenneri har samme navn.*
- **Bruker**(<ins>Epost</ins>, Passord, FulltNavn, Land)
  *Epost er nøkkel til bruker.*
- **Foredlingsmetode**(<ins>Navn</ins>, Beskrivelse)
  *Navn på foredlingsmetode er nøkkel til Foredlingsmetode.*
- **Kaffesmaking** (<ins>Epost</ins>, <ins>KaffebrenneriNavn</ins>, <ins>KaffeNavn</ins>, <ins>KaffeDato</ins>, Smaksnotater, Poeng, Dato)
  *KaffebrenneriNavn, KaffeNavn og KaffeDato er fremmednøkler mot Kaffe.*
  *Epost er fremmednøkkel mot Bruker.*
  *Epost, KaffebrenneriNavn, KaffeNavn og KaffeDato utgjør nøkkelen til Kaffesmaking.*
- **DyrketAv** (<ins>KaffebønneArt</ins>, <ins>KaffegårdNavn</ins>)
  *KaffebønneArt er fremmednøkkel mot Kaffebønne.*
  *KaffegårdNavn er fremmednøkkel mot Kaffegård.*
  *Sammen utgjør de nøkkelen til DyrketAv.*
- **PartiBestårAv** (<ins>KaffebønneArt</ins>, <ins>KaffepartiID</ins>)
  *KaffebønneArt er fremmednøkkel mot Kaffebønne.*
  *KaffepartiID er fremmednøkkel mot Kaffeparti.*
  *Sammen utgjør de nøkkelen til PartiBestårAv.*

<div style="page-break-after: always;"></div>

## Normalformer

### Kaffebønne
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Ingen.

Supernøkler: (Art)

Oppfyller 4NF fordi det ikke er noen ikke-trivielle funksjonelle avhengigheter eller fler-verdi-avhengigheter.

### Kaffegård
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Navn $\rightarrow$ HøydeOverHavet, Land, Region
- Land $\twoheadrightarrow$ Region

Supernøkler: (Navn)

Oppfyller 2NF fordi ingen ikke-nøkkelattributter er delvis avhengig av en (kandidat-)nøkkel. 
Oppfyller også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter.
Oppfyller ikke 4NF fordi Land ikke er en supernøkkel.

*Konklusjon: Tabellen er på BCNF.*

### Kaffeparti
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- ID $\rightarrow$ Innhøstingsår, Kilopris, KaffegårdNavn, ForedlingsmetodeNavn

Supernøkler: (ID)

Oppfyller 2NF fordi ingen ikke-nøkkelattributter er delvis avhengig av en (kandidat-)nøkkel. 
Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter.
4NF oppfylles fordi det er ingen fler-verdi-avhengigheter.

*Konklusjon: Tabellen er på 4NF.*

### Kaffe
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- KaffebrenneriNavn, Navn $\rightarrow$ Dato, Brenningsgrad, Beskrivelse, Kilopris, KaffepartiID

Supernøkler: (KaffebrenneriNavn, Navn)

Oppfyller 2NF fordi ingen ikke-nøkkelattributter er delvis avhengig av en (kandidat-)nøkkel. 
Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter.
4NF oppfylles fordi det er ingen fler-verdi-avhengigheter.

*Konklusjon: Tabellen er på 4NF.*

### Kaffebrenneri
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Ingen, kun ett attributt

Supernøkler: (Navn)

Oppfyller 4NF fordi det ikke er noen ikke-trivielle funksjonelle avhengigheter eller fler-verdi-avhengigheter.

*Konklusjon: Tabellen er på 4NF.*

### Bruker
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Epost $\rightarrow$ Passord, FulltNavn, Land

Supernøkkel: (Epost)

Oppfyller 2NF fordi ingen ikke-nøkkelattributter er delvis avhengig av en (kandidat-)nøkkel. Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter. Oppfyller 4NF fordi det ikke er noen ikke-trivielle fler-verdi-avhengigheter.

*Konklusjon: Tabellen er på 4NF.*

### Kaffesmaking
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Epost, KaffebrenneriNavn, KaffeNavn $\rightarrow$ Smaksnotater, Poeng, Dato

Supernøkler: (Epost, KaffebrenneriNavn, KaffeNavn)

Oppfyller 2NF fordi ingen ikke-nøkkelattributter er delvis avhengig av en (kandidat-)nøkkel. Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter. Oppfyller 4NF fordi det ikke er noen ikke-trivielle fler-verdi-avhengigheter.

*Konklusjon: Tabellen er på 4NF.*

### DyrketAv
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Ingen.

Supernøkkel: (KaffebønneArt, KaffegårdNavn)

Oppfyller 2NF fordi ingen ikke-nøkkelattributter er delvis avhengig av en (kandidat-)nøkkel. Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter. Oppfyller 4NF fordi det ikke er noen ikke-trivielle funksjonelle avhengigheter eller fler-verdi-avhengigheter.

*Konklusjon: Tabellen er på 4NF.*

### PartiBestårAv
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Ingen funksjonelle avhengigheter.

Oppfyller 2NF fordi ingen ikke-nøkkelattributter er delvis avhengig av en (kandidat-)nøkkel. Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter. Oppfyller 4NF fordi det ikke er noen ikke-trivielle funksjonelle avhengigheter eller fler-verdi-avhengigheter.

*Konklusjon: Tabellen er på 4NF.*

<div style="page-break-after: always;"></div>

## Hvordan brukerhistoriene tilfredsstilles

### Brukerhistorie 1 kan implementeres slik i systemet:

**Kaffe** ('Vinterkaffe', '20.01.2022', 'lysbrent', 'En velsmakende og kompleks kaffe for mørketiden', 600, 'Jacobsen & Svart', 1)

**Kaffebrenneri** ('Jacobsen & Svart')

**Kaffeparti** (1, 2021, 72, 'Bærtørket')

**Kaffebønne** ('Coffea arabica')

**Kaffegård** ('Nombre Dios', 1500, 'Santa Ana', 'El Salvador')

**Bruker** ('ola@nordmann.no', 'Passord', 'Ola Nordmann', 'Norge')

**Kaffesmaking** ('ola@nordmann.no', 'Jacobsen & Svart', 'Vinterkaffe', '20.01.2022', 'Wow - en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!', 10, null)
*Brukerhistorien sier ingenting om smaksdato --> null*

**DyrketAv** ('Coffea arabica', 'Nombre de Dios')

**PartiBestårAv** ('Coffea arabica', 1)

**Foredlingsmetode** ('Bærtørket', null)

Her er hele brukerhistorien lagt til i tabellene våre. Vi kan da se at modellen vår tilfredsstiller brukerhistorie 1. Merk at USD er konvertert til NOK.

### Brukerhistorie 2
Informasjonen som trengs i denne brukerhistorien finnes i tabellene KaffeSmaking og Bruker.
I systemet vårt kan man få en liste over hvilke brukere som har smakt flest unike kaffer så langt i år ved å gruppere kaffesmakinger etter bruker-epost, hvor dato er i 2022. Deretter sjekker man hvor mange smakinger de har på unike kaffer ved å telle unike fremmednøkler til Kaffe. Til slutt sorterer du på antall synkende, og returnerer brukerens fulle navn og antallet kaffer de har smakt.
```sql
SELECT FulltNavn, COUNT(*) AS Antall
FROM Kaffesmaking INNER JOIN Bruker USING (Epost)
WHERE Dato LIKE '%2022'
GROUP BY Epost
ORDER BY Antall DESC
```

### Brukerhistorie 3
Informasjonen som trengs i denne brukerhistorien finnes i tabellene KaffeSmaking og Kaffe.
Vi joiner Kaffesmaking med Kaffe på Kaffes nøkkelattributter. Deretter finner vi gjennomsnitt av Poeng i KaffeSmaking (og kaller dette gjennomsnittspoeng), gruppert utifra ulike kaffer. Returnerer KaffebrenneriNavn, Kaffe navn, pris og gjennomsnittspoeng, sortert synkende etter gjennomsnittspoeng.
```sql
SELECT Kaffe.KaffebrenneriNavn, Kaffe.Kilopris, AVG(Poeng) AS GjPoeng  
FROM Kaffe INNER JOIN Kaffesmaking
ON Kaffe.KaffebrenneriNavn = KaffeSmaking.KaffebrenneriNavn
  AND Kaffe.Navn = KaffeSmaking.KaffeNavn 
GROUP BY Kaffe.KaffebrenneriNavn, Kaffe.Navn
ORDER BY GjPoeng DESC
```

### Brukerhistorie 4
Informasjonen som trengs i denne brukerhistorien finnes i tabellene KaffeSmaking og Kaffe.
Vi joiner Kaffe og Kaffesmaking på KaffebrenneriNavn og KaffeNavn. Deretter velger vi ut alle kaffer hvor beskrivelsen inneholder 'floral' eller smaksnotater inneholder 'floral'. Returnerer Kaffe.KaffebrenneriNavn og Kaffe.Navn.
```sql
SELECT Kaffe.KaffebrenneriNavn, Kaffe.Navn
FROM Kaffe INNER JOIN Kaffesmaking
ON Kaffe.KaffebrenneriNavn = KaffeSmaking.KaffebrenneriNavn
  AND Kaffe.Navn = KaffeSmaking.KaffeNavn 
WHERE Kaffe.Beskrivelse LIKE '%floral%'
  OR Kaffesmaking.Smaksnotater LIKE '%floral%'
```

### Brukerhistorie 5
Informasjonen som trengs i denne brukerhistorien finnes i tabellene Kaffe, Kaffeparti og Kaffegård.
Vi joiner Kaffe og Kaffeparti på KaffepartiID=ID. Deretter joiner vi dette med Kaffegård der Kaffeparti.KaffegårdNavn = Kaffegård.Navn. Nå velger vi ut de gårder hvor land er enten 'Rwanda' eller 'Columbia'. Avslutningsvis velger man de radene der Kaffeparti.ForedlingsmetodeNavn ikke er lik 'vasket', før man joiner disse med Kaffe og returnerer Kaffe.Navn og KaffebrenneriNavn.
```sql
SELECT Kaffe.Navn, FerigbrentKaffe.KaffebrenneriNavn
FROM (Kaffe INNER JOIN Kaffeparti) INNER JOIN Kaffegård
ON Kaffe.KaffepartiID = Kaffeparti.ID AND Kaffeparti.KaffegårdNavn = Kaffegård.Navn
WHERE (Kaffegård.Land='Rwanda' OR Kaffegård.Land='Colombia') 
  AND Kaffeparti.ForedlingsmetodeNavn != 'vasket'
```
