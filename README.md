# TDT4145-project

## Kriterier (TODO: FJERN DETTE)
DB1
1. Bruk av entiteter, relasjoner og attributter. Disse konseptene skal anvendes på en 
hensiktsmessig måte, og antallet entiteter og relasjoner skal være rimelig
2. Bruk av nøkler, herunder naturlige og genererte.
3. Bruk av restriksjoner, f.eks. kardinaliteter, i modellen. Er disse anvendt på korrekt vis?
4. Oversetting til SQL-tabeller. Korrekt bruk av SQL, herunder attributtdomener, (fremmed-
)nøkkelrestriksjoner og UNIQUE. Forståelse av normalformer, inkludert 4NF.
5. Beskrivelsen av hvordan brukerhistoriene passer inn med tabellene, hvilke tabeller som 
brukes i hvilke brukerhistorier. Inneholder tabellene all nødvendig informasjon?
6. Dokumentene skal være konsise og figurene enkle å forstå.

## ER-modell
![](images/er.png)

### Antakelser
- Forskjellige kaffegårder kan ikke ha samme navn.
- Forskjellige kaffebrennerier kan ikke ha samme navn.
- FerdigbrentKaffe: Flere kaffebrennerier kan navngi kaffen sin likt, derfor er FerdigBrentKaffe en svak klasse.

## Relasjonsdatabasemodeller
- **Kaffebønne** (<ins>Art</ins>)
- **Kaffegård** (<ins>Navn</ins>, HøydeOverHavet, Land, Region)
- **Kaffeparti** (<ins>ID</ins>, Innhøstingsår, Kilopris, KaffegårdNavn, ForedlingsmetodeNavn)
  *KaffegårdNavn er fremmednøkkel mot Kaffegård (ProdusertAv)*
  *ForedlingsmetodeNavn er fremmednøkkel mot Foredlingsmetode (ForedletMed)*
- **FerdigbrentKaffe** (<ins>Navn</ins>, <ins>Dato</ins>, Brenningsgrad, Beskrivelse, Kilopris, KaffebrenneriNavn, KaffepartiID)
  *Kaffebrennerinavn er fremmednøkkel mot Kaffebrenneri (BrentAv)*
  *KaffepartiID er fremmednøkkel mot Kaffeparti (FremstillesAv)*
- **Kaffebrenneri** (<ins>Navn</ins>)
- **Bruker**(<ins>Epost</ins>, Passord, FulltNavn, Land)
- **Foredlingsmetode**(<ins>Navn</ins>, Beskrivelse)
- **Kaffesmaking** (<ins>Epost</ins>, <ins>KaffebrenneriNavn</ins>, <ins>FerdigbrentNavn</ins>, <ins>FerdigbrentDato</ins>, Smaksnotater, Poeng, Dato)
  *KaffebrenneriNavn, FerdigbrentNavn og KaffeDato er fremmednøkler mot FerdigbrentKaffe*
  *Epost er fremmednøkkel mot Bruker*
- **DyrketAv** (<ins>KaffebønneArt</ins>, <ins>KaffegårdNavn</ins>)
  *KaffebønneArt er fremmednøkkel mot Kaffebønne*
  *KaffegårdNavn er fremmednøkkel mot Kaffegård*
- **PartiBestårAv** (<ins>KaffebønneArt</ins>, <ins>KaffepartiID</ins>)
  *KaffebønneArt er fremmednøkkel mot Kaffebønne*
  *KaffepartiID er fremmednøkkel mot Kaffeparti*

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

Oppfyller 2NF fordi ingen ikke-nøkkel attributter er delvis avhengig av en (kandidat-)nøkkel. 
Oppfyller også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter.
Oppfyller ikke 4NF fordi Land ikke er en supernøkkel.

### Kaffeparti
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- ID $\rightarrow$ Innhøstingsår, KaffegårdNavn, ForedlingsmetodeNavn

Supernøkler: (ID)

Oppfyller 2NF fordi ingen ikke-nøkkel attributter er delvis avhengig av en (kandidat-)nøkkel. 
Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter.
4NF oppfylles fordi det er ingen fler-verdi-avhengigheter.

### FerdigbrentKaffe
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- KaffebrenneriNavn, Navn, Dato $\rightarrow$ Brenningsgrad, Beskrivelse, Kilopris, KaffepartiID

Supernøkler: (KaffebrenneriNavn, Navn, Dato)

Oppfyller 2NF fordi ingen ikke-nøkkel attributter er delvis avhengig av en (kandidat-)nøkkel. 
Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter.
4NF oppfylles fordi det er ingen fler-verdi-avhengigheter.

### Kaffebrenneri
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Ingen, kun ett attributt

Supernøkler: (Navn)

Oppfyller 4NF fordi det ikke er noen ikke-trivielle funksjonelle avhengigheter eller fler-verdi-avhengigheter.

### Bruker
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Epost $\rightarrow$ Passord, FulltNavn, Land

Supernøkkel: (Epost)

Oppfyller 2NF fordi ingen ikke-nøkkel attributter er delvis avhengig av en (kandidat-)nøkkel. Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter. Oppfyller 4NF fordi det ikke er noen ikke-trivielle fler-verdi-avhengigheter.

### Kaffesmaking
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Epost, Kaffebrenneri, FerdigbrentNavn, FerdigbrentDato $\rightarrow$ Smaksnotater, Poeng

> DATO???

Supernøkler: (Epost, FerdigbrentNavn)

Oppfyller 2NF fordi ingen ikke-nøkkel attributter er delvis avhengig av en (kandidat-)nøkkel. Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter. Oppfyller 4NF fordi det ikke er noen ikke-trivielle fler-verdi-avhengigheter.


### DyrketAv
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Ingen.

Supernøkkel: (KaffebønneArt, KaffegårdNavn)

Oppfyller 2NF fordi ingen ikke-nøkkel attributter er delvis avhengig av en (kandidat-)nøkkel. Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter. Oppfyller 4NF fordi det ikke er noen ikke-trivielle funksjonelle avhengigheter eller fler-verdi-avhengigheter.

### PartiBestårAv
Ikke-trivielle funksjonelle avhengigheter og fler-verdi-avhengigheter:
- Ingen funksjonelle avhengigheter.

Oppfyller 2NF fordi ingen ikke-nøkkel attributter er delvis avhengig av en (kandidat-)nøkkel. Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter.Oppfyller 4NF fordi det ikke er noen ikke-trivielle funksjonelle avhengigheter eller fler-verdi-avhengigheter.

## Hvordan brukerhistoriene tilfredsstilles

### Brukerhistorie 1 kan implementeres slik i systemet:

**FerdigbrentKaffe** ('Vinterkaffe', '20.01.2022', 'lysbrent', 'En velsmakende og kompleks kaffe for mørketiden', 600kr, 'Jacobsen & Svart', 1)
  TODO: Pris og valuta?

**Kaffebrenneri** ('Jacobsen & Svart')

**Kaffeparti** (1, 2021, 8 USD, 'Bærtørket')
  TODO: Pris og valuta?

**Kaffebønne** ('Coffea arabica')

**Kaffegård** ('Nombre Dios', 1500, 'Santa Ana', 'El Salvador')

**Bruker** ('ola@nordmann.no', 'Passord', 'Ola Nordmann', 'Norge')

**Kaffesmaking** ('ola@nordmann.no', 'Jacobsen & Svart', 'Vinterkaffe', '20.01.2022', 'Wow - en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!', 10, null)
  *Brukerhistorien sier ingenting om smaksdato --> null

**DyrketAv** ('Coffea arabica , 'Nombre de Dios')

**PartiBestårAv** ('Coffea arabica', 1)

**Foredlingsmetode** ('Bærtørket', null)

Her er hele brukerhistorien lagt til i tabellene våre. Vi kan da se at modellen vår tilfredsstiller brukerhistorie 1.

### Brukerhistorie 2
I systemet vårt kan man få en liste over hvilke brukere som har smakt flest unike kaffer så langt i år ved å gruppere kaffesmakinger etter bruker-epost, hvor dato er i 2022. Deretter sjekker man hvor mange smakinger de har på unike ferdigbrente kaffer ved å telle unike fremmednøkler til FerdigbrentKaffe. Til slutt sorterer du på antall synkende, og returnerer brukerens fulle navn og antallet kaffer de har smakt.
```sql
SELECT FulltNavn, COUNT(*) AS Antall -- TODO: er stjerne riktig?
FROM Kaffesmaking INNER JOIN Bruker USING (Epost)
WHERE Dato LIKE '%2022'
GROUP BY Epost
ORDER BY Antall DESC
```

### Brukerhistorie 3
Vi joiner Kaffesmaking med FerdigbrentKaffe naturlig (på FerdigbrentKaffes nøkkelattributter). Deretter finner vi gjennomsnitt av Poeng i KaffeSmaking (og kaller dette gjennomsnittsscore), gruppert utifra ulike ferdigbrente kaffer. Returnerer KaffebrenneriNavn, FerdigbrentKaffe navn, pris og gjennomsnittsscore.
```sql
```


### Brukerhistorie 4
Vi joiner FerdigbrentKaffe og KaffeSmaking naturlig. Deretter velger vi ut alle kaffer hvor beskrivelsen inneholder 'floral' eller smaksnotater inneholder 'floral'. Returnerer FerdigbrentKaffe.KaffebrenneriNavn og FerdigbrentKaffe.Navn.
```sql
```

### Brukerhistorie 5
Vi joiner FerdigbrentKaffe og Kaffeparti på KaffepartiID=ID. Deretter joiner vi dette med Kaffegård der Kaffeparti.KaffegårdNavn = Kaffegård.Navn. Nå velger vi ut de gårder hvor land er enten 'Rwanda' eller 'Columbia'. Avslutningsvis velger man de radene der Kaffeparti.ForedlingsmetodeNavn ikke er lik 'vasket', før man joiner disse med FerdigbrentKaffe og returnerer FerdigbrentKaffe.Navn og KaffebrenneriNavn.
```sql
```

