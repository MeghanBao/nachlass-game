## NACHLASS — Die letzte Stunde
## Game-Jam-Skelett. Ein entfremdeter, verstorbener Verwandter; eine Wohnung;
## eine Stunde, bevor die Entrümpelung kommt.
##
## Erweitern: neue Erinnerungsstücke einfach der OBJECTS-Liste hinzufügen.
## Jedes Objekt kostet Zeit — bei 20 Minuten schaffst du nicht alles. Das ist Absicht.

define narr = Character(None)

## --- Zustand -------------------------------------------------------------
default time_budget = 60      # gewählte Dauer in Minuten (20 / 30 / 60)
default time_spent = 0        # bereits "verbrauchte" Aufmerksamkeit
default examined = []         # ids der angesehenen Stücke
default kept = []             # ids der mitgenommenen Stücke (max. 3)

init python:
    COST = 8  # Minuten, die jedes Erinnerungsstück kostet

    # Die Erinnerungsstücke. Frei erweiterbar — Reihenfolge = Reihenfolge im Menü.
    OBJECTS = [
        {
            "id": "sparbuch",
            "name": "Das Sparbuch",
            "fragment":
                "Jeden Monat zwanzig Mark. Seit 1994. Auf deinen Namen.\n"
                "Du hast nie davon gewusst. Die letzte Einzahlung war im März — "
                "der Monat, in dem du aufgehört hast, ans Telefon zu gehen.",
            "epilogue":
                "Das Sparbuch hast du behalten. Dreißig Jahre, zwanzig Mark im "
                "Monat, für ein Kind, das nicht mehr anrief.",
            "nachruf":
                "Er sparte dreißig Jahre für ein Kind, das nicht mehr anrief.",
        },
        {
            "id": "anrufbeantworter",
            "name": "Der Anrufbeantworter",
            "fragment":
                "Eine ungehörte Nachricht. Das Datum: dein letzter Geburtstag.\n"
                "Dein Daumen liegt auf der Taste. Draußen hält ein Transporter.",
            "epilogue":
                "Die Nachricht hast du mitgenommen. Ob du sie je abhörst, "
                "weißt du noch nicht.",
            "nachruf":
                "Er hob eine Nachricht auf, die nie beantwortet wurde.",
        },
        {
            "id": "fotoalbum",
            "name": "Das Fotoalbum",
            "fragment":
                "Seite um Seite du als Kind. Dann, ab einem bestimmten Jahr, nur "
                "noch leere Ecken — die Bilder herausgenommen, nicht weggeworfen.\n"
                "In einem Umschlag hinten: genau diese Fotos. Er konnte sie weder "
                "ansehen noch wegwerfen.",
            "epilogue":
                "Das Album war zu schwer. Du hast nur den Umschlag mitgenommen.",
            "nachruf":
                "Er konnte die Bilder weder ansehen noch wegwerfen.",
        },
    ]

    def obj(oid):
        for o in OBJECTS:
            if o["id"] == oid:
                return o
        return None


## --- Start ---------------------------------------------------------------
label start:
    scene black
    narr "Dein Großvater ist tot."
    narr "Ihr habt seit Jahren nicht mehr gesprochen. Jetzt räumst du seine Wohnung — es gibt sonst niemanden."

    narr "Wie viel Zeit gibst du ihm?"
    menu:
        "20 Minuten":
            $ time_budget = 20
        "30 Minuten":
            $ time_budget = 30
        "Eine Stunde":
            $ time_budget = 60

    narr "In [time_budget] Minuten kommt die Entrümpelung. Danach ist die Wohnung leer."
    jump room


## --- Der Raum ------------------------------------------------------------
label room:
    scene black
    while time_spent < time_budget and len(examined) < len(OBJECTS):
        python:
            remaining = time_budget - time_spent
            options = [(o["name"], o["id"]) for o in OBJECTS if o["id"] not in examined]
            options.append(("(Die Wohnung verlassen)", "_leave"))
            _choice = renpy.display_menu(options)

        if _choice == "_leave":
            jump movers

        $ examined.append(_choice)
        $ time_spent += COST
        $ _name = obj(_choice)["name"]
        $ _frag = obj(_choice)["fragment"]
        narr "[_name]"
        narr "[_frag]"

        if time_spent >= time_budget:
            narr "Draußen schlägt eine Autotür."

    jump movers


## --- Die Entrümpelung kommt ---------------------------------------------
label movers:
    scene black
    narr "Es klingelt. Die Entrümpelung ist da."
    if len(examined) == 0:
        narr "Du hast nichts angesehen. Gleich ist alles weg."
        jump ending

    narr "Du darfst mitnehmen, was du tragen kannst. Höchstens drei Dinge."
    while len(kept) < 3 and len(kept) < len(examined):
        python:
            opts = [(obj(oid)["name"], oid) for oid in examined if oid not in kept]
            opts.append(("(Genug. Gehen.)", "_done"))
            _pick = renpy.display_menu(opts)
        if _pick == "_done":
            jump ending
        $ kept.append(_pick)

    jump ending


## --- Ende: die Traueranzeige --------------------------------------------
## Die drei behaltenen Dinge werden zum Nachruf. Was du nicht mitgenommen hast,
## bleibt als "—" leer: das, was du nie über ihn erfahren wirst.
label ending:
    scene black
    if not kept:
        narr "Du gehst mit leeren Händen. Es gibt nichts zu behalten — und nichts zu sagen."
        jump ending_schluss

    narr "Was du mitnimmst:"
    python:
        for oid in kept:
            renpy.say(narr, obj(oid)["epilogue"])

    narr "Später sollst du für die Zeitung ein paar Zeilen aufsetzen. Eine Traueranzeige."
    narr "Alles, was du über ihn sagen kannst, steht in dem, was du mitgenommen hast. Der Rest bleibt leer."

    python:
        _zeilen = [(o["nachruf"] if o["id"] in kept else "—") for o in OBJECTS]
        anzeige = "\n".join(_zeilen)

    narr "{i}✝  In stillem Gedenken{/i}\n\n[anzeige]\n\nWas von ihm bleibt, passt in einen Schuhkarton."

label ending_schluss:
    # Reflexion nach gewählter Dauer — die Zeit, die du ihm gegeben hast.
    if time_budget == 60:
        narr "Du hast dir eine Stunde genommen. Das erste Mal seit Jahren."
    elif time_budget == 30:
        narr "Dreißig Minuten. Mehr, als ihr in den letzten Jahren je füreinander hattet."
    else:
        narr "Zwanzig Minuten. Mehr wolltest du ihm nie geben."

    narr "Die Tür fällt ins Schloss."
    return
