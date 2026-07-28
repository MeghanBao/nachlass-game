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
- **Aus den drei Dingen wird sein Nachruf.** Die behaltenen Gegenstände setzen sich
  zu einer **Traueranzeige** zusammen; was du zurückgelassen hast, bleibt darin als
  „—" leer. Du, der ihm zuletzt nur Minuten gab, definierst öffentlich, wer er war —
  in drei Zeilen.
- **Die gewählte Dauer ist selbst eine Aussage.** 20 / 30 / 60 Minuten — wie viel
  Zeit gibst du ihm? Am kürzesten Ende siehst du nicht alles. Das ist Absicht, und
  das Ende weiß es.

## Spielzeit / Playtime

Beim Start wählbar: **20 · 30 · 60 Minuten.** Jedes Erinnerungsstück kostet Zeit;
bei 20 Minuten reicht sie nicht für alles.

## Ausführen / Run it

Dieses Repo enthält das **Spiel** (`game/` mit Skript, Platzhalter-Ton), nicht
die Ren'Py-Engine.

1. [Ren'Py SDK](https://www.renpy.org/latest.html) herunterladen (kostenlos).
2. Im Launcher **„Neues Projekt erstellen"** → Name `nachlass`.
3. Den Inhalt von `game/` aus diesem Repo in den `game/`-Ordner des neuen
   Projekts kopieren — `script.rpy` **ersetzen**, die Ordner `audio/` und
   `images/` dazulegen. Die generierten `options.rpy`, `gui.rpy`, `screens.rpy`
   (Menü- und Textfenster-GUI) **behalten**.
4. **„Starten"** klicken. Beim Start wählst du **Sprache (DE/EN)** und **Dauer**.

> Ohne SDK hier nicht ausführbar; die Spiellogik und alle Texte sind aber per
> Python-Selbsttest geprüft (9 Objekte, alle DE+EN vollständig).

## Sprache / Language

Zweisprachig **Deutsch / Englisch** über eine Sprachvariable (Auswahl beim Start),
ohne Ren'Py-`translate`-Hashes — Texte liegen als `{"de": …, "en": …}` in den Daten.

## Erweitern / Extend

Neues Erinnerungsstück: einen Eintrag zur Liste `OBJECTS` in `game/script.rpy`
hinzufügen. Felder: `id`, `pos` (x, y für die Raumgrafik), und je zweisprachig
`name`, `fragment`, `nachruf` (Zeile für die Traueranzeige), `epilogue`. Optional
`sound`. Menü, Timing, Traueranzeige und Endauswahl passen sich automatisch an.

## Assets noch offen / Assets still needed

Der Code ist fertig und über `renpy.loadable()` abgesichert — fehlt eine Datei,
läuft das Spiel sauber weiter (Textliste statt Raumbild, Stille statt Ton). Zum
„echten" Look/Sound noch einzulegen:

- `game/images/raum.png` — Raumgrafik (1280×720). Vorhanden → der Raum wird
  **anklickbar** (Hotspots liegen schon auf den `pos`-Koordinaten der Objekte);
  fehlt sie → automatische Menüliste.
- `game/audio/raum.ogg` — Zimmeratmosphäre (Loop).
- `game/audio/nachricht.ogg` — **die Stimme des Verstorbenen** auf dem
  Anrufbeantworter (das einzige Mal, dass er „spricht").
- Enthalten sind bereits **Platzhalter**: `game/audio/uhr.wav` (Ticken der Uhr)
  und `game/audio/piep.wav` (Beep des Anrufbeantworters).

## Status / Roadmap

- [x] Kern-Skelett: Zeitwahl → Nachlass durchsehen → Zeit läuft ab → drei Dinge behalten → Traueranzeige
- [x] Vollständiger Nachlass: **9 Stücke** mit rotem Faden der Entfremdung (Schuld, das nicht mehr gehörte Telefonat, das gegenseitige Schweigen, die tote Tochter dazwischen, das Unausgesprochene)
- [x] Raum als anklickbares Bild — Code fertig, aktiviert sich mit `raum.png` *(Grafik ausstehend)*
- [x] Ton: Uhr + Anrufbeantworter-Beep als Platzhalter, Atmosphäre & Stimme abgesichert verdrahtet *(echte Assets ausstehend)*
- [x] Zweisprachig Deutsch / Englisch
- [ ] Echte Raumgrafik, Raumton und die Stimme auf dem Anrufbeantworter
- [ ] Playtest im Ren'Py-SDK

---

*Inspiriert von „The Last Hour of Pal" von FoxEcho. Eigenständiges Werk, kein Fork.*
