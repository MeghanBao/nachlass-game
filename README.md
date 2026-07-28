# NACHLASS — *Die letzte Stunde*

Ein kurzes, textbasiertes Erinnerungsspiel auf Deutsch. / A short German-language
memory game.

Eine Stunde, bevor die Entrümpelung kommt, räumst du die Wohnung eines
Verwandten, mit dem du seit Jahren nicht mehr gesprochen hast — und der jetzt
tot ist. Du kannst nicht mehr mit ihm reden. Du kannst nur noch herausfinden,
wer er war, aus dem, was er zurückgelassen hat.

> One hour before the clearance company arrives, you empty the flat of a relative
> you hadn't spoken to in years — one who is now dead. You can't talk to them.
> You can only work out who they were from what they left behind.

---

## Was das anders macht / What makes it different

Inspiriert von [*The Last Hour of Pal*](https://foxechoo.itch.io/the-last-hour-of-pal),
aber mit umgedrehtem Kern:

- **Kein Freund, sondern ein entfremdeter, verstorbener Verwandter.** Das Gespräch
  ist einseitig. Du *rekonstruierst* einen Menschen, statt dich von ihm zu
  verabschieden — näher kommst du ihm nie wieder.
- **Kein Dialogbaum, sondern Nachlass.** Gegenstände tragen die Erinnerung; manche
  erklären neu, *warum* der Kontakt abbrach.
- **Du kannst nicht alles retten.** Am Ende darfst du nur **drei Dinge** mitnehmen.
  Der Rest wird für immer entsorgt.
- **Die gewählte Dauer ist selbst eine Aussage.** 20 / 30 / 60 Minuten — wie viel
  Zeit gibst du ihm? Am kürzesten Ende siehst du nicht alles. Das ist Absicht, und
  das Ende weiß es.

## Spielzeit / Playtime

Beim Start wählbar: **20 · 30 · 60 Minuten.** Jedes Erinnerungsstück kostet Zeit;
bei 20 Minuten reicht sie nicht für alles.

## Ausführen / Run it

Dieses Repo enthält das **Spiel-Skript**, nicht die Ren'Py-Engine.

1. [Ren'Py SDK](https://www.renpy.org/latest.html) herunterladen (kostenlos).
2. Im Launcher **„Neues Projekt erstellen"** → Name `nachlass`.
3. Die generierte Datei `game/script.rpy` durch die aus diesem Repo ersetzen
   (`game/script.rpy`).
4. **„Starten"** klicken.

> Die vom Launcher erzeugten Vorlagendateien (`options.rpy`, `gui.rpy`,
> `screens.rpy`) liefern das Menü- und Textfenster-GUI und werden hier bewusst
> nicht mitgetrackt — nur das Spiel selbst.

## Erweitern / Extend

Neue Erinnerungsstücke: einen Eintrag zur Liste `OBJECTS` in `game/script.rpy`
hinzufügen (`id`, `name`, `fragment`, `epilogue`). Sonst nichts nötig — Menü,
Timing und Endauswahl passen sich automatisch an.

## Status / Roadmap

- [x] Kern-Skelett: Zeitwahl → Nachlass durchsehen → Zeit läuft ab → drei Dinge behalten → Ende
- [x] Drei Beispiel-Objekte mit deutschen Fragmenten (u. a. der Anrufbeantworter — die einzige „Stimme" des Verstorbenen)
- [ ] Vollständiger Nachlass (8–10 Stücke) + der rote Faden der Entfremdung
- [ ] Raum als anklickbares Bild (imagemap) statt Menüliste
- [ ] Ton: Zimmeratmosphäre, Uhr, die Nachricht auf dem Anrufbeantworter
- [ ] Englische Sprachfassung (Ren'Py `translate`)

---

*Inspiriert von „The Last Hour of Pal" von FoxEcho. Eigenständiges Werk, kein Fork.*
