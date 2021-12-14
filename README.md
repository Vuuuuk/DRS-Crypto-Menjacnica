Predlog formatiranja GitHub repozitorijuma:
    - Svaki od članova tima je dužan da kreira svoju "granu" na samom repozitorijumu.
    - Ime grane sledećeg formata, broj indeksa-godina (PR-158-2018)
    - Prilikom kreiranja COMMIT poruka predlažen sledeću alteraciju Karma konvencije:

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

* Main grana će biti inicijalizovana sa tekstom zadatka, konvencijom kreiranja Commit-poruka, dijagramom dizajna sistema...
* Pull request-ove kreiramo posle završavanja svake od celine za koju se dogovorimo da je neko zadužen (ko kako završi dok celine međusobno nisu povezane).

Predlog formatiranja samog koda:
    - camelCase notacija, kapitalizacija prvog slova druge reči.
    - Pridržavanje pravilnika ocenjivanja (broja klasa u skripti itd..).
