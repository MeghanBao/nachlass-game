## NACHLASS — Die letzte Stunde / The Last Hour
## Ein entfremdeter, verstorbener Verwandter; eine Wohnung; eine Stunde.
##
## Zweisprachig (DE/EN) über eine Sprachvariable — keine Ren'Py-tl-Hashes nötig.
## Bild & Ton sind über renpy.loadable() abgesichert: fehlen die Assets, fällt
## das Spiel sauber auf die Textliste bzw. Stille zurück. Siehe ASSETS.md.

define narr = Character(None)
image raum = "images/raum.png"    # optional; wird nur gezeigt, wenn vorhanden
image titel = "images/titel.png"  # optionale Titelkarte beim Start

## --- Zustand -------------------------------------------------------------
default lang = "de"           # "de" | "en"
default time_budget = 60      # gewählte Dauer in Minuten (20 / 30 / 60)
default time_spent = 0        # verbrauchte Aufmerksamkeit
default examined = []         # ids der angesehenen Stücke
default kept = []             # ids der mitgenommenen Stücke (max. 3)
default uhrzeit = "15:00"     # Anzeige der Standuhr im Raum
default deadline = "16:00"    # wann die Entrümpelung kommt

init python:
    COST = 8          # Minuten, die jedes Erinnerungsstück kostet
    START_MIN = 900   # 15:00 Uhr — Beginn der letzten Stunde

    # Eigener, geloopter Kanal für das Ticken der Uhr.
    renpy.music.register_channel("uhr", mixer="sfx", loop=True)

    def hhmm(total_min):
        h, m = divmod(total_min, 60)
        return "%02d:%02d" % (h, m)

    def L(d):
        # aktuelle Sprache wählen, sonst Deutsch
        return d.get(lang, d["de"])

    def erz(key):
        renpy.say(narr, L(TXT[key]))

    def erzf(key, **kw):
        renpy.say(narr, L(TXT[key]).format(**kw))

    def obj(oid):
        for o in OBJECTS:
            if o["id"] == oid:
                return o
        return None

    def zeig_objekt(oid):
        o = obj(oid)
        snd = o.get("sound")
        if snd and renpy.loadable(snd):
            if renpy.loadable("audio/piep.wav"):
                renpy.sound.play("audio/piep.wav")
            renpy.sound.play(snd, channel="voice")
        renpy.say(narr, L(o["name"]))
        renpy.say(narr, L(o["fragment"]))

    def coda_key():
        # Die drei behaltenen Dinge: welche Fassung von ihm hast du bewahrt?
        tones = [obj(oid)["ton"] for oid in kept]
        h = tones.count("hart"); u = tones.count("unvollendet"); w = tones.count("warm")
        if h >= 2:
            return "coda_hart"
        elif u >= 2:
            return "coda_unvollendet"
        elif w >= 2 and h == 0:
            return "coda_warm"
        return "coda_gemischt"

    # --- Erzähltexte ----------------------------------------------------
    TXT = {
        "tot": {"de": "Dein Großvater ist tot.",
                "en": "Your grandfather is dead."},
        "jahre": {"de": "Ihr habt seit Jahren nicht mehr gesprochen. Jetzt räumst du seine Wohnung — es gibt sonst niemanden.",
                  "en": "You hadn't spoken in years. Now you're clearing out his flat — there's no one else."},
        "zeit_frage": {"de": "Wie viel Zeit gibst du ihm?",
                       "en": "How much time will you give him?"},
        "entruempelung": {"de": "In {min} Minuten — um {zeit} Uhr — kommt die Entrümpelung. Danach ist die Wohnung leer.",
                          "en": "In {min} minutes — at {zeit} — the clearance crew arrives. After that the flat is empty."},
        "raum1": {"de": "Die Wohnung riecht nach kaltem Rauch und Bohnerwachs. Die Standuhr geht noch.",
                  "en": "The flat smells of cold smoke and floor wax. The grandfather clock is still ticking."},
        "raum2": {"de": "Auf allem liegt eine dünne Schicht Staub. Ein paar leere Umzugskartons warten schon. Du hast nicht lange. Fang an.",
                  "en": "A thin film of dust lies over everything. A few empty moving boxes are already waiting. You don't have long. Begin."},
        "verlassen": {"de": "(Die Wohnung verlassen)",
                      "en": "(Leave the flat)"},
        "autotuer": {"de": "Draußen schlägt eine Autotür.",
                     "en": "Outside, a car door slams."},
        "klingelt": {"de": "Es klingelt. Die Entrümpelung ist da.",
                     "en": "The doorbell rings. The clearance crew is here."},
        "nichts_gesehen": {"de": "Du hast nichts angesehen. Gleich ist alles weg.",
                           "en": "You looked at nothing. Soon it will all be gone."},
        "drei_dinge": {"de": "Du darfst mitnehmen, was du tragen kannst. Höchstens drei Dinge.",
                       "en": "You may take what you can carry. Three things at most."},
        "genug": {"de": "(Genug. Gehen.)",
                  "en": "(Enough. Leave.)"},
        "was_mitnimmst": {"de": "Was du mitnimmst:",
                          "en": "What you take with you:"},
        "leere_haende": {"de": "Du gehst mit leeren Händen. Es gibt nichts zu behalten — und nichts zu sagen.",
                         "en": "You leave empty-handed. Nothing to keep — and nothing to say."},
        "nachruf1": {"de": "Später sollst du für die Zeitung ein paar Zeilen aufsetzen. Eine Traueranzeige.",
                     "en": "Later you're to write a few lines for the paper. A death notice."},
        "nachruf2": {"de": "Alles, was du über ihn sagen kannst, steht in dem, was du mitgenommen hast. Der Rest bleibt leer.",
                     "en": "Everything you can say about him is in what you took. The rest stays blank."},
        "anzeige_kopf": {"de": "In stillem Gedenken",
                         "en": "In quiet remembrance"},
        "anzeige_fuss": {"de": "Was von ihm bleibt, passt in einen Schuhkarton.",
                         "en": "What remains of him fits in a shoebox."},
        # Coda — reagiert darauf, welche Fassung von ihm du bewahrt hast
        "coda_warm": {"de": "Du hast dir den sanften Großvater aufgehoben. Vielleicht darfst du das. Vielleicht ist das genug.",
                      "en": "You kept the gentle grandfather. Maybe you're allowed to. Maybe that's enough."},
        "coda_hart": {"de": "Du hast nichts beschönigt. Er war auch der, der er war — das schuldest du wenigstens der Wahrheit.",
                      "en": "You sugar-coated nothing. He was also the man he was — you owe the truth at least that much."},
        "coda_unvollendet": {"de": "Du hast die halben Sätze mitgenommen. Das Gespräch, das nie zu Ende ging — jetzt trägst du es allein weiter.",
                             "en": "You took the half-sentences. The conversation that never finished — now you carry it on alone."},
        "coda_gemischt": {"de": "Zärtlich, schwierig, unfertig — du hast ihn ganz mitgenommen, im Widerspruch. So, wie er war.",
                          "en": "Tender, difficult, unfinished — you took all of him, contradiction and all. As he was."},
        # Reflexion nach gewählter Dauer
        "refl_60": {"de": "Du hast dir eine Stunde genommen. Das erste Mal seit Jahren.",
                    "en": "You gave yourself an hour. The first time in years."},
        "refl_30": {"de": "Dreißig Minuten. Mehr, als ihr in den letzten Jahren je füreinander hattet.",
                    "en": "Thirty minutes. More than you ever had for each other in those last years."},
        "refl_20": {"de": "Zwanzig Minuten. Mehr wolltest du ihm nie geben.",
                    "en": "Twenty minutes. You never wanted to give him more."},
        "tuer_schloss": {"de": "Die Tür fällt ins Schloss.",
                         "en": "The door falls shut."},
        "credits1": {"de": "NACHLASS — Die letzte Stunde",
                     "en": "NACHLASS — The Last Hour"},
        "credits2": {"de": "Inspiriert von »The Last Hour of Pal« von FoxEcho.\nEin Spiel von Meghan Bao.",
                     "en": "Inspired by 'The Last Hour of Pal' by FoxEcho.\nA game by Meghan Bao."},
    }

    # --- Der Nachlass: 9 Stücke, ein roter Faden --------------------------
    # ton: "warm" (stille Zuneigung) | "hart" (seine Schuld/Schroffheit) |
    #      "unvollendet" (das nie zu Ende Gebrachte). Steuert die Coda am Ende.
    # pos = (x, y) für die anklickbare Raumgrafik (1280x720).
    OBJECTS = [
        {
            "id": "sparbuch", "pos": (180, 430), "ton": "warm",
            "name": {"de": "Das Sparbuch", "en": "The savings book"},
            "fragment": {
                "de": "Jeden Monat zwanzig Mark. Seit 1994, auf deinen Namen. Du hast nie davon gewusst.\nDie letzte Einzahlung war im März — der Monat, in dem du aufgehört hast, ans Telefon zu gehen.",
                "en": "Twenty marks every month. Since 1994, in your name. You never knew.\nThe last deposit was in March — the month you stopped picking up the phone."},
            "nachruf": {"de": "Er sparte dreißig Jahre für ein Kind, das nicht mehr anrief.",
                        "en": "He saved for thirty years for a child who no longer called."},
            "epilogue": {"de": "Das Sparbuch hast du behalten.",
                         "en": "You kept the savings book."},
        },
        {
            "id": "anrufbeantworter", "pos": (980, 300), "ton": "unvollendet",
            "sound": "audio/nachricht.ogg",   # seine Stimme — echtes VO kommt später
            "name": {"de": "Der Anrufbeantworter", "en": "The answering machine"},
            "fragment": {
                "de": "Eine ungehörte Nachricht. Das Datum: dein letzter Geburtstag. Seine Stimme, mitten im Satz abgebrochen.\nDein Daumen liegt auf der Taste. Draußen hält ein Transporter.",
                "en": "One unheard message. The date: your last birthday. His voice, breaking off mid-sentence.\nYour thumb rests on the button. Outside, a van pulls up."},
            "nachruf": {"de": "Er hinterließ eine Nachricht, die nie beantwortet wurde.",
                        "en": "He left a message that was never answered."},
            "epilogue": {"de": "Die Nachricht hast du mitgenommen. Ob du sie je abhörst, weißt du nicht.",
                         "en": "You took the message. Whether you'll ever play it, you don't know."},
        },
        {
            "id": "fotoalbum", "pos": (520, 520), "ton": "warm",
            "name": {"de": "Das Fotoalbum", "en": "The photo album"},
            "fragment": {
                "de": "Seite um Seite du als Kind. Dann, ab einem bestimmten Jahr, nur noch leere Ecken — die Bilder herausgenommen, nicht weggeworfen.\nIn einem Umschlag hinten: genau diese Fotos. Er konnte sie weder ansehen noch wegwerfen.",
                "en": "Page after page of you as a child. Then, from a certain year on, only empty corners — the photos removed, not thrown away.\nIn an envelope at the back: exactly those photos. He could neither look at them nor throw them out."},
            "nachruf": {"de": "Er konnte die Bilder weder ansehen noch wegwerfen.",
                        "en": "He could neither look at the pictures nor throw them away."},
            "epilogue": {"de": "Das Album war zu schwer. Du hast nur den Umschlag mitgenommen.",
                         "en": "The album was too heavy. You took only the envelope."},
        },
        {
            "id": "flaschen", "pos": (300, 600), "ton": "hart",
            "name": {"de": "Die leeren Flaschen", "en": "The empty bottles"},
            "fragment": {
                "de": "Im Keller, in Reih und Glied, sauber gestapelt. Es beginnt in dem Jahr, in dem Mama starb — dasselbe Jahr, in dem im Album die Ecken leer werden.\nEr hat auch das aufgehoben. Ordentlich. Als wollte er nichts vergessen, was er sich vorzuwerfen hatte.",
                "en": "In the cellar, lined up, neatly stacked. It starts the year Mum died — the same year the album's corners go empty.\nHe kept this too. Tidily. As if he didn't want to forget anything he had to blame himself for."},
            "nachruf": {"de": "Nach dem Tod seiner Tochter trank er. Auch das ist wahr.",
                        "en": "After his daughter's death, he drank. That is also true."},
            "epilogue": {"de": "Die Flaschen lässt du stehen. Aber du vergisst sie nicht.",
                         "en": "You leave the bottles. But you don't forget them."},
        },
        {
            "id": "hoergeraet", "pos": (760, 440), "ton": "unvollendet",
            "name": {"de": "Das Hörgerät", "en": "The hearing aid"},
            "fragment": {
                "de": "In der Nachttischschublade, die Batterie längst leer. Nie getragen — aus Sturheit, aus Stolz.\nDu erinnerst dich an das letzte Telefonat. Du hast geschrien, er hat geschwiegen. Du dachtest, er ignoriert dich. Er hat dich nur nicht gehört.",
                "en": "In the nightstand drawer, its battery long dead. Never worn — out of stubbornness, out of pride.\nYou remember the last phone call. You shouted, he said nothing. You thought he was ignoring you. He simply couldn't hear you."},
            "nachruf": {"de": "Am Ende hörte er dich nicht mehr. Nicht einmal, wenn du riefst.",
                        "en": "In the end he could no longer hear you. Not even when you called out."},
            "epilogue": {"de": "Das Hörgerät steckst du ein. Zu spät, aber du steckst es ein.",
                         "en": "You pocket the hearing aid. Too late, but you pocket it."},
        },
        {
            "id": "rueckbrief", "pos": (140, 250), "ton": "hart",
            "name": {"de": "Der zurückgeschickte Brief", "en": "The returned letter"},
            "fragment": {
                "de": "Ein Brief von ihm an dich, ungeöffnet. Quer über den Umschlag, in deiner eigenen Handschrift: »Annahme verweigert«.\nDer Poststempel ist elf Jahre alt. Er hat den zurückgeschickten Brief aufbewahrt — deine Abfuhr, schwarz auf weiß.",
                "en": "A letter from him to you, unopened. Across the envelope, in your own hand: 'Return to sender.'\nThe postmark is eleven years old. He kept the returned letter — your refusal, in black and white."},
            "nachruf": {"de": "Er schrieb. Du schicktest es zurück. Ihr habt beide geschwiegen.",
                        "en": "He wrote. You sent it back. You were both silent."},
            "epilogue": {"de": "Den Brief nimmst du mit — immer noch ungeöffnet.",
                         "en": "You take the letter — still unopened."},
        },
        {
            "id": "foto_mutter", "pos": (620, 200), "ton": "warm",
            "name": {"de": "Das Foto deiner Mutter", "en": "The photo of your mother"},
            "fragment": {
                "de": "Das einzige Bild, das er offen stehen ließ: seine Tochter. Deine Mutter. Die Ränder abgegriffen von Daumen.\nZwischen euch stand immer sie. Er hat sie verloren. Dir hat sie gefehlt. Keiner von euch konnte darüber reden.",
                "en": "The only picture he left out on display: his daughter. Your mother. The edges worn smooth by thumbs.\nShe always stood between you. He lost her. You missed her. Neither of you could talk about it."},
            "nachruf": {"de": "Zwischen ihnen stand immer sie — die er verlor und die dir fehlte.",
                        "en": "She always stood between them — the one he lost and the one you missed."},
            "epilogue": {"de": "Das Foto deiner Mutter nimmst du mit. Das war nie die Frage.",
                         "en": "You take the photo of your mother. That was never in question."},
        },
        {
            "id": "gartenschluessel", "pos": (1050, 560), "ton": "warm",
            "name": {"de": "Der Schrebergartenschlüssel", "en": "The allotment key"},
            "fragment": {
                "de": "Ein rostiger Schlüssel am Bast. Der Garten, in dem du jeden Sommer warst, bevor alles kaputtging. Johannisbeeren, seine Schultern, du obendrauf.\nJetzt ist er verwildert. Aber es gab ihn: einen Garten, einen Sommer, bevor Mama starb.",
                "en": "A rusty key on a raffia string. The garden where you spent every summer, before everything broke. Currants, his shoulders, you up on top.\nIt's overgrown now. But it existed: a garden, a summer, before Mum died."},
            "nachruf": {"de": "Es gab einen Garten, einen Sommer, ein Kind auf seinen Schultern.",
                        "en": "There was a garden, a summer, a child on his shoulders."},
            "epilogue": {"de": "Den Schlüssel behältst du. Vielleicht fährst du mal raus.",
                         "en": "You keep the key. Maybe you'll drive out there someday."},
        },
        {
            "id": "ungesendet", "pos": (860, 180), "ton": "unvollendet",
            "name": {"de": "Der ungesendete Brief", "en": "The unsent letter"},
            "fragment": {
                "de": "In der Schublade, unter dem Hörgerät. An dich gerichtet, nie abgeschickt.\n»Ich wollte dir sagen, dass —« Hier bricht er ab. Der Rest der Seite ist leer.\nEr hat die Worte gefunden. Er hat sie nur nie losgeschickt.",
                "en": "In the drawer, under the hearing aid. Addressed to you, never sent.\n'I wanted to tell you that —' Here it breaks off. The rest of the page is blank.\nHe found the words. He just never sent them."},
            "nachruf": {"de": "Er fand die Worte. Er schickte sie nie ab.",
                        "en": "He found the words. He never sent them."},
            "epilogue": {"de": "Den ungesendeten Brief nimmst du mit. Du wirst zu Ende lesen, was nicht dasteht.",
                         "en": "You take the unsent letter. You'll finish reading what isn't there."},
        },
    ]


## --- Anklickbarer Raum (nur aktiv, wenn images/raum.png vorhanden) --------
screen raum_screen():
    add "raum"
    for o in OBJECTS:
        if o["id"] not in examined:
            textbutton L(o["name"]):
                xpos o["pos"][0]
                ypos o["pos"][1]
                action Return(o["id"])
    textbutton L(TXT["verlassen"]):
        align (0.5, 0.98)
        action Return("_leave")

## --- Standuhr-Anzeige (in beiden Modi sichtbar) --------------------------
screen uhr_hud():
    text "[uhrzeit]":
        align (0.98, 0.02)
        size 30
        outlines [(2, "#000000", 0, 0)]


## --- Start ---------------------------------------------------------------
label start:
    scene black
    # Optionale Titelkarte — nur wenn images/titel.png vorhanden ist.
    if renpy.loadable("images/titel.png"):
        scene titel with fade
        pause
        scene black with fade

    # Zustand für einen sauberen (Neu-)Start zurücksetzen
    $ time_spent = 0
    $ examined = []
    $ kept = []

    $ renpy.say(narr, "Sprache — Language")
    python:
        lang = renpy.display_menu([("Deutsch", "de"), ("English", "en")])

    $ erz("tot")
    $ erz("jahre")

    $ erz("zeit_frage")
    python:
        time_budget = int(renpy.display_menu([
            (u"20 Minuten" if lang == "de" else u"20 minutes", "20"),
            (u"30 Minuten" if lang == "de" else u"30 minutes", "30"),
            (u"Eine Stunde" if lang == "de" else u"One hour", "60"),
        ]))
        deadline = hhmm(START_MIN + time_budget)

    $ erzf("entruempelung", min=time_budget, zeit=deadline)
    jump room


## --- Der Raum ------------------------------------------------------------
label room:
    scene black
    if renpy.loadable("images/raum.png"):
        scene raum
    if renpy.loadable("audio/raum.ogg"):
        play music "audio/raum.ogg" fadein 2.0
    if renpy.loadable("audio/uhr.wav"):
        play uhr "audio/uhr.wav"

    $ erz("raum1")
    $ erz("raum2")
    show screen uhr_hud

    while time_spent < time_budget and len(examined) < len(OBJECTS):
        python:
            uhrzeit = hhmm(START_MIN + time_spent)
            if renpy.loadable("images/raum.png"):
                _choice = renpy.call_screen("raum_screen")
            else:
                opts = [(L(o["name"]), o["id"]) for o in OBJECTS if o["id"] not in examined]
                opts.append((L(TXT["verlassen"]), "_leave"))
                _choice = renpy.display_menu(opts)

        if _choice == "_leave":
            jump movers

        $ examined = examined + [_choice]   # rollback-sicher (neue Liste)
        $ time_spent += COST
        $ zeig_objekt(_choice)

        if time_spent >= time_budget:
            $ erz("autotuer")

    jump movers


## --- Die Entrümpelung kommt ---------------------------------------------
label movers:
    hide screen uhr_hud
    scene black
    if renpy.loadable("audio/uhr.wav"):
        stop uhr fadeout 1.0
    $ erz("klingelt")
    if len(examined) == 0:
        $ erz("nichts_gesehen")
        jump ending

    $ erz("drei_dinge")
    while len(kept) < 3 and len(kept) < len(examined):
        python:
            opts = [(L(obj(oid)["name"]), oid) for oid in examined if oid not in kept]
            opts.append((L(TXT["genug"]), "_done"))
            _pick = renpy.display_menu(opts)
        if _pick == "_done":
            jump ending
        $ kept = kept + [_pick]   # rollback-sicher

    jump ending


## --- Ende: die Traueranzeige --------------------------------------------
## Die behaltenen Dinge werden zum Nachruf; was du nicht mitnahmst, bleibt "—".
## Die Coda reagiert darauf, welche Fassung von ihm du bewahrt hast.
label ending:
    scene black
    if not kept:
        $ erz("leere_haende")
        jump ending_schluss

    $ erz("was_mitnimmst")
    python:
        for oid in kept:
            renpy.say(narr, L(obj(oid)["epilogue"]))

    $ erz("nachruf1")
    $ erz("nachruf2")
    python:
        zeilen = [(L(o["nachruf"]) if o["id"] in kept else u"—") for o in OBJECTS]
        anzeige = u"{i}✝  " + L(TXT["anzeige_kopf"]) + u"{/i}\n\n" + u"\n".join(zeilen) + u"\n\n" + L(TXT["anzeige_fuss"])
        renpy.say(narr, anzeige)

    $ erz(coda_key())

label ending_schluss:
    if time_budget == 60:
        $ erz("refl_60")
    elif time_budget == 30:
        $ erz("refl_30")
    else:
        $ erz("refl_20")

    $ erz("tuer_schloss")

    # Abspann
    scene black with fade
    $ erz("credits1")
    $ erz("credits2")
    return
