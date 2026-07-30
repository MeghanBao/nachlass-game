#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Selbsttest für NACHLASS / self-test for NACHLASS.

Ren'Py wird nicht benötigt: dieses Skript zieht die reinen Datenliterale
(``TXT`` und ``OBJECTS``) aus ``game/script.rpy`` und prüft sie ohne Engine.

No Ren'Py needed: this script extracts the plain data literals (``TXT`` and
``OBJECTS``) from ``game/script.rpy`` and validates them without the engine.

Aufruf / run:  python3 selftest.py
Beendet mit Code 0, wenn alles besteht; sonst 1.
"""

import ast
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "game", "script.rpy")

VALID_TONE = {"warm", "hart", "unvollendet"}
BILINGUAL_FIELDS = ("name", "fragment", "nachruf", "epilogue")
LANGS = ("de", "en")
ROOM_W, ROOM_H = 1280, 720


def _extract_literal(source, marker, open_ch, close_ch):
    """Return the balanced literal that follows ``marker`` in ``source``.

    String- and comment-aware: brackets inside ``"..."`` (e.g. the ``{min}``
    format placeholders) or after ``#`` are ignored, so only structural
    brackets move the depth counter.
    """
    start = source.index(marker) + len(marker)
    while source[start] != open_ch:
        start += 1
    depth = 0
    in_str = False
    in_comment = False
    i = start
    while i < len(source):
        c = source[i]
        if in_comment:
            if c == "\n":
                in_comment = False
        elif in_str:
            if c == "\\":
                i += 1          # skip escaped char
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "#":
            in_comment = True
        elif c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return source[start:i + 1]
        i += 1
    raise ValueError("unbalanced %r ... %r after %r" % (open_ch, close_ch, marker))


def load_data():
    with open(SCRIPT, encoding="utf-8") as fh:
        src = fh.read()
    txt = ast.literal_eval(_extract_literal(src, "TXT =", "{", "}"))
    objects = ast.literal_eval(_extract_literal(src, "OBJECTS =", "[", "]"))
    return src, txt, objects


def coda_key(kept, by_id):
    """Reimplementation of coda_key() from script.rpy — must stay in sync."""
    tones = [by_id[oid]["ton"] for oid in kept]
    h = tones.count("hart")
    u = tones.count("unvollendet")
    w = tones.count("warm")
    if h >= 2:
        return "coda_hart"
    elif u >= 2:
        return "coda_unvollendet"
    elif w >= 2 and h == 0:
        return "coda_warm"
    return "coda_gemischt"


def main():
    errors = []

    def check(cond, msg):
        if not cond:
            errors.append(msg)

    src, TXT, OBJECTS = load_data()

    # --- OBJECTS -----------------------------------------------------------
    check(len(OBJECTS) == 9, "expected 9 objects, found %d" % len(OBJECTS))
    ids = [o["id"] for o in OBJECTS]
    check(len(ids) == len(set(ids)), "duplicate object ids: %r" % ids)

    for o in OBJECTS:
        oid = o.get("id", "<no id>")
        check(o.get("ton") in VALID_TONE,
              "%s: invalid ton %r" % (oid, o.get("ton")))
        pos = o.get("pos")
        check(isinstance(pos, tuple) and len(pos) == 2,
              "%s: pos must be an (x, y) tuple, got %r" % (oid, pos))
        if isinstance(pos, tuple) and len(pos) == 2:
            x, y = pos
            check(0 <= x <= ROOM_W and 0 <= y <= ROOM_H,
                  "%s: pos %r outside 1280x720 room" % (oid, pos))
        for field in BILINGUAL_FIELDS:
            val = o.get(field)
            check(isinstance(val, dict), "%s: missing field %r" % (oid, field))
            if isinstance(val, dict):
                for lang in LANGS:
                    check(val.get(lang, "").strip() != "",
                          "%s.%s: empty or missing %r text" % (oid, field, lang))
        if "sound" in o:
            check(o["sound"].startswith("audio/"),
                  "%s: sound path should live under audio/, got %r"
                  % (oid, o["sound"]))

    # --- TXT ---------------------------------------------------------------
    for key, val in TXT.items():
        check(isinstance(val, dict), "TXT[%r] is not a {de,en} dict" % key)
        if isinstance(val, dict):
            for lang in LANGS:
                check(val.get(lang, "").strip() != "",
                      "TXT[%r]: empty or missing %r" % (key, lang))

    # Every key the script narrates via erz()/erzf() must exist in TXT.
    referenced = set(re.findall(r'erzf?\("([^"]+)"', src))
    for key in sorted(referenced):
        check(key in TXT, "script narrates TXT[%r] but it is not defined" % key)

    # Format placeholders in "entruempelung" must match the erzf() call.
    if "entruempelung" in TXT:
        for lang in LANGS:
            fields = set(re.findall(r"\{(\w+)\}", TXT["entruempelung"][lang]))
            check(fields == {"min", "zeit"},
                  "entruempelung[%s] placeholders %r != {min, zeit}"
                  % (lang, fields))

    # --- Coda logic: every branch must be reachable and land in TXT --------
    by_id = {o["id"]: o for o in OBJECTS}
    warm = [o["id"] for o in OBJECTS if o["ton"] == "warm"]
    hart = [o["id"] for o in OBJECTS if o["ton"] == "hart"]
    unv = [o["id"] for o in OBJECTS if o["ton"] == "unvollendet"]
    check(len(warm) >= 2 and len(hart) >= 2 and len(unv) >= 2,
          "need >=2 objects of each tone to reach every coda; "
          "warm=%d hart=%d unvollendet=%d" % (len(warm), len(hart), len(unv)))

    scenarios = {
        "coda_hart": hart[:2],
        "coda_unvollendet": unv[:2],
        "coda_warm": warm[:2],
        "coda_gemischt": [warm[0], hart[0], unv[0]],
    }
    for expected, kept in scenarios.items():
        got = coda_key(kept, by_id)
        check(got == expected,
              "coda scenario %r produced %r (kept=%r)" % (expected, got, kept))
        check(got in TXT, "coda key %r not defined in TXT" % got)

    # --- Report ------------------------------------------------------------
    if errors:
        print("FAIL — %d problem(s):" % len(errors))
        for e in errors:
            print("  - " + e)
        return 1

    print("OK — %d objects, %d narration keys, all DE+EN complete, "
          "coda branches reachable." % (len(OBJECTS), len(TXT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
