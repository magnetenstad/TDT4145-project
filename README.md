# TDT4145-project

## ER-modell
![](images/er.png)

## Relasjonsdatabasemodeller
**Entiteter**
- Kaffebønne(<ins>Art</ins>)
- Kaffegård(<ins>Navn</ins>, HøydeOverHavet, Land, Region)
- Kaffeparti(<ins>ID</ins>, Innhøstingsår, KaffegårdNavn, ForedlingsmetodeNavn)
  *KaffegårdNavn er fremmednøkkel mot Kaffegård (ProdusertAv)*
  *ForedlingsmetodeNavn er fremmednøkkel mot Foredlingsmetode (ForedletMed)*
- FerdigbrentKaffe(<ins>Navn</ins>, <ins>Dato</ins>, Brenningsgrad, Kilopris, KaffebrenneriNavn, KaffepartiID)
  *Kaffebrennerinavn er fremmednøkkel mot Kaffebrenneri (BrentAv)*
  *KaffepartiID er fremmednøkkel mot Kaffeparti (FremstillesAv)*
- Kaffebrenneri(<ins>Navn</ins>)
- Bruker(<ins>Epost</ins>, Passord, FulltNavn, Land)

**Relasjoner**
- Kaffesmaking(<ins>Epost</ins>, <ins>FerdigbrentNavn</ins>, Smaksnotater, Poeng)
  *FerdigbrentNavn er fremmednøkkel mot FerdigbrentKaffe*
  *Epost er fremmednøkkel mot Bruker*
- DyrketAv(<ins>KaffebønneArt</ins>, <ins>KaffegårdNavn</ins>)
  *KaffebønneArt er fremmednøkkel mot Kaffebønne*
  *KaffegårdNavn er fremmednøkkel mot Kaffegård*
- PartiBestårAv(<ins>KaffebønneArt</ins>, <ins>KaffepartiID</ins>)
  *KaffebønneArt er fremmednøkkel mot Kaffebønne*
  *KaffepartiID er fremmednøkkel mot Kaffeparti*

## Normalformer

### Kaffebønne
4NF fordi det kun er en attributt

### Kaffegård
Funksjonelle avhengigheter:
- Navn $\rightarrow$ HøydeOverHavet, Land, Region
- Land $\twoheadrightarrow$ Region 

Oppfyller 2NF fordi ingen ikke-nøkkel attributter er delvis avhengig av en (kandidat)-nøkkel. 
Oppfyller også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av andre ikke-nøkkelattributter.

### Kaffeparti
Funksjonelle avhengigheter:
- ID $\rightarrow$ Innhøstingsår, KaffegårdNavn, ForedlingsmetodeNavn

Oppfyller 2NF fordi ingen ikke-nøkkel attributter er delvis avhengig av en (kandidat)-nøkkel. 
Videre oppfylles også 3NF og BCNF fordi ingen ikke-nøkkelattributter er avhengig av ander ikke-nøkkelattributter.

### FerdigbrentKaffe
Funksjonelle avhengigheter:
- Navn, Dato $\rightarrow$ Brenningsgrad, Kilopris, KaffebrenneriNavn, KaffepartiID

Kan kanskje hevde at dato --> kaffepartiID?


### Kaffebrenneri
Funksjonelle avhengigheter:
- Ingen, kun ett attributt

4NF fordi det kun er ett attributt, nøkkelattributtet.

### Bruker
Funksjonelle avhengigheter:

### Kaffesmaking
Funksjonelle avhengigheter:

### DyrketAv
Funksjonelle avhengigheter:

### PartiBestårAv
Funksjonelle avhengigheter:


## Hvordan brukerhistoriene tilfredsstilles
### Brukerhistorie 1
