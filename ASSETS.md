# Asset-Anforderungen / Asset Requirements — *NACHLASS*

Der Code ist fertig und wartet auf diese Dateien. Jede ist über
`renpy.loadable()` abgesichert: Solange sie fehlt, läuft das Spiel weiter
(Textliste statt Raum, Stille statt Ton). Legt man sie ins richtige Verzeichnis,
schaltet sich das Feature automatisch scharf.

> The code is finished and waiting on these files. Each is guarded by
> `renpy.loadable()`, so the game runs without them and activates the feature the
> moment the file is dropped into the right folder.

| File | Where | Type | Status |
|---|---|---|---|
| `raum.png` | `game/images/` | Bild / image | **fehlt / needed** → aktiviert den anklickbaren Raum |
| `raum.ogg` | `game/audio/` | Ton / audio | **fehlt / needed** → Zimmeratmosphäre |
| `nachricht.ogg` | `game/audio/` | Ton / voice | **fehlt / needed** → die Stimme des Verstorbenen |
| `uhr.wav` | `game/audio/` | Ton / audio | Platzhalter vorhanden, ersetzen für „echt" |
| `piep.wav` | `game/audio/` | Ton / audio | Platzhalter vorhanden, ersetzen für „echt" |

---

## 1. Raumgrafik / Room graphic — `game/images/raum.png`

**Technical**
- **1280 × 720 px** (das Spiel rendert auf 1280×720). Für schärfere Displays gern
  @2x, also **2560 × 1440**, herunterskaliert liefern oder Ren'Py skalieren lassen.
- PNG, keine Transparenz nötig (Vollbild-Hintergrund).
- Optional zusätzlich: `raum_hover.png` (dieselbe Szene, jedes Objekt leicht
  hervorgehoben/umrandet) für Hover-Rückmeldung — schön, aber nicht erforderlich.

**Konzept / concept.** Die Wohnung eines ~80-jährigen Mannes am Tag der
Räumung. Westdeutsch, kleinbürgerlich, seit Jahrzehnten unverändert: dunkle
**Schrankwand**, Spitzengardinen/Store, abgewohnter Teppich, eine **Standuhr**
(sie liefert das Ticken). Ein paar **halb gepackte Umzugskartons** am Rand. Es ist
später Nachmittag; Staub in einem schrägen Lichtstrahl. Kein Mensch im Bild — nur
die Dinge, die er hinterlassen hat.

**Stimmung / mood.** Still, angehalten, würdevoll. Nicht gruselig, nicht kitschig
— *leise*. Das Licht einer zu Ende gehenden Biografie.

**Palette.** Gedämpfte Brauntöne, Ocker, vergilbtes Weiß, ein kühler Rest
Tageslicht am Fenster. Entsättigt, aber warm.

**Komposition & Hotspots.** Die 9 Objekte müssen sichtbar und ungefähr an ihren
Koordinaten platziert sein — dort liegen die klickbaren Flächen (aus
`script.rpy`, Bezugsrahmen 1280×720, Ankerpunkt oben-links des Objekt-Labels):

| Objekt | id | pos (x, y) | grobe Lage im Raum | wie es aussehen soll |
|---|---|---|---|---|
| Foto der Mutter | `foto_mutter` | 620, 200 | Mitte oben, auf einem Sideboard | gerahmtes SW-Foto einer jungen Frau, abgegriffen |
| Ungesendeter Brief | `ungesendet` | 860, 180 | rechts oben, offene Schublade | halb beschriebenes Blatt, Füller daneben |
| Anrufbeantworter | `anrufbeantworter` | 980, 300 | rechts, Telefontischchen | alter Kassetten-AB, rote „1" blinkt |
| Zurückgeschickter Brief | `rueckbrief` | 140, 250 | links oben | Umschlag, quer beschriftet, ungeöffnet |
| Hörgerät | `hoergeraet` | 760, 440 | Mitte-rechts, Nachttisch | winziges Hörgerät in offener Schublade |
| Sparbuch | `sparbuch` | 180, 430 | links Mitte | schmales Sparbuch, DDR/BRD-Ästhetik |
| Fotoalbum | `fotoalbum` | 520, 520 | Mitte unten, Couchtisch | dickes Album, ein Umschlag ragt heraus |
| Leere Flaschen | `flaschen` | 300, 600 | unten links, am Boden | Reihe leerer Flaschen, ordentlich |
| Schrebergartenschlüssel | `gartenschluessel` | 1050, 560 | rechts unten, am Haken | rostiger Schlüssel an Bastschnur |

Grobe Verteilung (1280×720):

```
 rueckbrief        foto_mutter       ungesendet
 (140,250)         (620,200)         (860,180)
                                      anrufbeantworter
 sparbuch                             (980,300)
 (180,430)               hoergeraet
            fotoalbum    (760,440)
            (520,520)                 gartenschluessel
 flaschen                             (1050,560)
 (300,600)
```

> Die Objekte dürfen frei umkomponiert werden — dann bitte die `pos`-Werte in
> `game/script.rpy` an die finale Grafik anpassen (eine Zahl pro Objekt). Die
> Klickfläche ist aktuell das Text-Label; wer will, ersetzt später `textbutton`
> durch `imagebutton` mit echten Objekt-Sprites.

**Optional weitere Bilder / optional extras**
- `titel.png` (1280×720) — Titelbild für das Startmenü.
- `endkarte.png` — schlichter Hintergrund hinter der Traueranzeige (z. B. eine
  Zeitungs-Traueranzeigenseite). Sonst bleibt Schwarz, was ebenfalls trägt.

---

## 2. Zimmeratmosphäre / Room tone — `game/audio/raum.ogg`

- **Format** OGG Vorbis, Stereo, 44.1 kHz. **Nahtloser Loop, 30–60 s.**
- **Pegel** sehr leise, Bett-Charakter: ca. **−30 bis −24 LUFS**. Es soll *unter*
  allem liegen, nie auffallen.
- **Inhalt.** Gedämpfte Ferne einer alten Wohnung: entfernter Straßenlärm hinter
  Doppelfenster, ein leises Kühlschrank-/Heizungsbrummen, gelegentliches Knacken
  von altem Holz/Parkett. **Kein** Ticken hier (das kommt separat aus `uhr.wav`,
  eigener Kanal), **keine** Stimmen, keine Musik.
- **Ziel** das akustische Gefühl von *Stille in einem Raum, in dem gerade niemand
  mehr wohnt.*

---

## 3. Die Stimme auf dem Anrufbeantworter / The answering-machine voice — `game/audio/nachricht.ogg`

Das emotionale Zentrum: das **einzige Mal**, dass der Verstorbene „spricht". Er
hat diese Nachricht an deinem **letzten Geburtstag** hinterlassen; du hast sie nie
abgehört. Sie **bricht mitten im Satz ab** — bei genau dem Satz, den er auch im
*ungesendeten Brief* nicht zu Ende bringt: „Ich wollte dir sagen, dass —".

- **Format** OGG Vorbis, Mono, 44.1 kHz. **Länge ~30–45 s.**
- **Stimme** männlich, ca. 80, müde, behutsam. Diese Generation sagt „ich hab dich
  lieb" nicht — die Zuneigung steckt im Zögern, nicht in den Worten. Leicht
  schwerhörig: ungleichmäßige Lautstärke, mal zu laut. Räuspern, lange Pausen.
  Kein starker Dialekt nötig (leichtes Ruhrgebiet/norddeutsch ist stimmig).
- **Processing** wie ein alter Kassetten-Anrufbeantworter: Telefonband
  **300–3400 Hz** (dünn, mittig), leichte Kompression, feines **Bandrauschen** und
  minimales Wow/Flutter, ein mechanisches **Klicken** am Anfang. (Der *Beep* davor
  ist separat: `piep.wav`.)

### Sprechtext (DE) — genau so einsprechen

```
[Klick des Bandes]

Ja... ähm. Ich bin's.
Dein... na ja. Du weißt schon.

[Pause, ein Räuspern]

Heute ist ja dein Geburtstag. Fünfunddreißig.
Mein Gott. Fünfunddreißig.

Ich hab dir was überwiesen. Aufs alte Konto.
Falls's das noch gibt. Das Konto, mein ich.

[Pause]

Es ist... hier ist es sehr ruhig geworden.
Ich wollte dir nur sagen, dass —

[langes Zögern, ein Atemzug]

Ach. Ist ja dumm. Ruf nicht zurück, wenn du nicht willst.
Ich weiß ja. Ich weiß.

Pass auf dich auf. Ja? Pass auf dich —

[Klick — das Band ist zu Ende]
```

### Translation (EN) — for subtitles only, **not** to be recorded

```
[tape click]

Yeah... um. It's me.
Your... well. You know.

[pause, a throat clear]

It's your birthday today. Thirty-five.
My God. Thirty-five.

I transferred you something. To the old account.
If it still exists. The account, I mean.

[pause]

It's... it's gotten very quiet here.
I just wanted to tell you that —

[long hesitation, a breath]

Ah. It's silly. Don't call back if you don't want to.
I know. I know.

Take care of yourself. Yeah? Take care of your—

[click — the tape runs out]
```

> **Verknüpfung / throughline.** Der abgebrochene Satz „Ich wollte dir (nur) sagen,
> dass —" ist bewusst identisch mit dem *ungesendeten Brief*. Zweimal findet er den
> Anfang, zweimal nie das Ende. Wer beide Objekte behält, hört/liest denselben
> Bruch — das ist die Absicht.

---

## 4. Uhr / Clock — `game/audio/uhr.wav` (Platzhalter ersetzen)

- **Genau 1,000 s**, nahtloser Loop (läuft auf eigenem Loop-Kanal `uhr`).
- Ein **trockenes, mechanisches Ticken** einer Wanduhr/Standuhr, nah, hölzern.
  Ein Tick pro Sekunde. Kein Hall.
- Mono, 44.1 kHz, WAV oder OGG. Pegel ca. −20 LUFS.
- *Motiv:* die Uhr ist der Countdown. Sie tickt die Stunde herunter, die du ihm gibst.

## 5. Beep — `game/audio/piep.wav` (Platzhalter ersetzen)

- **0,3–0,5 s**, ein einzelner **Anrufbeantworter-Beep** mit echtem Gerätecharakter
  (leicht verstimmt, nicht klinisch rein). Spielt direkt vor `nachricht.ogg`.
- Mono, 44.1 kHz.

---

## Integration

1. Datei ins genannte Verzeichnis legen (`game/images/` bzw. `game/audio/`).
2. Bei `raum.png`: einmal starten und prüfen, ob die Klickflächen auf den Objekten
   liegen. Falls nicht, die `pos`-Werte in `game/script.rpy` anpassen.
3. Ton startet automatisch beim Betreten des Raums (`raum.ogg`, `uhr.wav`);
   `nachricht.ogg` + `piep.wav` spielen beim Ansehen des Anrufbeantworters.

*Alle Assets optional zuschaltbar — das Spiel bricht nie ab, wenn eines fehlt.*
