
# DRS - Crypto menjačnica

Implementirati projekat koji simulira Crypto menjačnicu I on-line crypto 
račun za lične uplate.
Implementacija treba da sadrži 3 komponente:
1. Korisnički interfejs (UI)
2. Servis za obradu zahteva I podataka (Engine)
3. Bazu podataka (DB)

## Dizajn sistema

![DRS - Crypto menjačnica](https://i.ibb.co/qJ3D8cL/Dizajn-servisa-DRS.png)

## Formatiranje GitHub repozitorijuma
 
1. Svaki od članova tima je dužan da kreira svoju "granu" na samom repozitorijumu. 
2. Ime grane sledećeg formata, broj indeksa-godina (PR-158-2018)
3. Posle rada na projektu, ukoliko je došlo do uključivanja novih biblioteka obavezno ažurirati requirements.txt.
4. Prilikom kreiranja COMMIT poruka pratiti sledeću alteraciju Karma konvencije:

        <type>: <subject>
            <body>

        Dozvoljenje <type> vrednosti:
            - feat for a new feature.
            - fix for a bug fix for the user or a fix to a build script.
            - perf for performance improvements.
            - docs for changes to the documentation.
            - style for code formatting changes or UI changes.
            - refactor for refactoring production code.

        <subject> predstavlja kratak opis rešenog problema ili implementacije koja se commit-uje.
            * obavezan deo svakog commit-a

        <body> predstavlja detaljniji opis samo koda ili promena koje su potrebne kako bi se neki problem rešio 
            * možda će biti korisno kasnije, nije obavezno.

        Primer commit-a (bez tela) - perf: added parallelization for taking in requests in the Engine

5. Pull request-ove kreiramo posle završavanja svake od celine za koju se dogovorimo da je neko zadužen (ko kako završi dok celine međusobno nisu povezane).

## Formatiranje koda
1. camelCase notacija, kapitalizacija prvog slova druge reči.
2. Pridržavanje pravilnika ocenjivanja (broja klasa u skripti itd...).

## Pravilnik ocenjivanja

1. Više od 3 klase u jednoj skripti -5 bodova.
2. Zamrzavanje aplikacije prilikom prezentovanja -2 boda.
3. Pojedina ima manje od 3 commit-a -5 bodova.
4. Pojedinac nema commit-ove - pao.
5. Usmeni 4/5 pitanja odgovoreno tačno -1 bod.
6. Usmeni 3/5 pitanja odgovoreno tačno -3 boda.
7. Usmeni 2/5 pitanja odgovoreno tačno -6 bodova.
8. Usmeni 1/5 pitanja odgovoreno tačno -pao.
9. Nepoznavanje koda -5 bodova.
10. Naknadna odbrana -15 bodova.

## Bodovanje

1. Aplikacija je funkcionalna I postoji Flask aplikacija – 51 poen.
2. Implementiran Engine kao posebna Flask aplikacija gde UI komunicira sa Engine-om
putem API-a – 10 poena.
3. Implementirana je baza sa kojom komunicira Engine – 9 poena.
4. Koriscenje niti prilikom implementacije – 10 poena.
5. Koriscenje procesa prilikom implementacije – 10 poena.
6. Dokerizacija aplikacije I pokretanje na vise racunara (distribuiran sistem) – 10 poena.
7. Deploy aplikacije na Heroku – gratis 5 poena (moguce samo ako je svih 6 tacaka
implementirano).