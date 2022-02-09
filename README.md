
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