# Voice-over script + scene specs (v2: faster, fact-checked, photo-heavy).
# "say" = text sent to TTS; "sub" = caption text (Canadian spelling). *...* = red accent words.

SCENES = [
    # ---------------- HOOK ----------------
    dict(chap="", sub="North Vancouver is hard on siding.",
         kind="photo_text", img=3, lines=["North Vancouver is", "*hard on siding*"]),
    dict(chap="", sub="Parts of the North Shore get close to double the rain of Vancouver Airport.",
         kind="photo_text", img=1, lines=["Close to", "*double the rain*", "of Vancouver Airport"]),
    dict(chap="", sub="Choose the wrong siding, and that rain finds every weak spot.",
         kind="photo_text", img=2, lines=["Choose the wrong siding", "and that rain finds *every weak spot*"]),
    dict(chap="", sub="Here's what actually works.",
         kind="kinetic", bg="light", lines=["Here's what", "*actually works*"]),

    # ---------------- RAINSCREEN ----------------
    dict(chap="01 · Rainscreen", sub="Start with the rainscreen: a drained air gap behind the siding, so water runs out and the wall can dry.",
         kind="rainscreen"),
    dict(chap="01 · Rainscreen", sub="In wet coastal areas like ours, B.C.'s building code requires it on new wood-frame walls.",
         say="In wet coastal areas like ours, B C's building code requires it on new wood-frame walls.",
         kind="photo_text", img=5, lines=["B.C.'s building code", "*requires it*"]),

    # ---------------- MATERIALS ----------------
    dict(chap="02 · Materials", sub="Now, the materials.",
         kind="chapter", num="02", lines=["The", "*materials*"]),
    dict(chap="02 · Materials", sub="Fibre cement won't rot, won't burn, and handles our wet climate well. It's heavier, and needs proper cutting tools.",
         say="Fiber cement won't rot, won't burn, and handles our wet climate well. It's heavier, and needs proper cutting tools.",
         kind="card", head="Fibre cement", kicker="OPTION 1", badge="Non-combustible",
         items=[("ok", "Won't rot", "won't rot"), ("ok", "Won't burn", "won't burn"), ("ok", "Handles wet climates", "handles"),
                ("no", "Heavier, needs proper tools", "heavier")]),
    dict(chap="02 · Materials", sub="Vinyl is the budget option. But it can crack on impact in the cold, and fade over time in direct sun.",
         kind="card", head="Vinyl", kicker="OPTION 2", badge="Budget",
         items=[("ok", "Lowest cost", "budget"), ("no", "Can crack in the cold", "crack"), ("no", "Fades in direct sun", "fade")]),
    dict(chap="02 · Materials", sub="Engineered wood gives you a wood look for less, but every cut edge has to be sealed.",
         kind="card", head="Engineered wood", kicker="OPTION 3",
         items=[("ok", "Wood look for less", "wood look"), ("no", "Every cut edge must be sealed", "every cut")]),
    dict(chap="02 · Materials", sub="Cedar is a West Coast classic, but without regular stain or sealer, it greys and weathers.",
         kind="card", head="Cedar", kicker="OPTION 4",
         items=[("ok", "Natural West Coast look", "west coast"), ("no", "Needs regular stain or sealer", "regular stain"), ("no", "Greys without upkeep", "greys")]),
    dict(chap="02 · Materials", sub="Metal siding is sleek, modern and low-maintenance. The key is clean detailing at every joint.",
         kind="card", head="Metal siding", kicker="OPTION 5", img=6,
         items=[("ok", "Sleek, modern look", "sleek"), ("ok", "Low maintenance", "low-maintenance"), ("dot", "Needs precise joint detailing", "clean detailing")]),
    dict(chap="02 · Materials", sub="Brick and stone last for decades, but they need a drainage gap and weep holes behind them.",
         kind="card", head="Brick & stone", kicker="OPTION 6", img=1,
         items=[("ok", "Lasts for decades", "last for"), ("dot", "Needs a drainage gap", "drainage gap"), ("dot", "Needs weep holes", "weep holes")]),

    # ---------------- OUR WORK ----------------
    dict(chap="03 · Our work", sub="Here's some of our recent work.",
         kind="chapter", num="03", lines=["Our", "*recent work*"], grid=True),
    dict(chap="03 · Our work", sub="Brick and stone on a townhome development: warm, solid, and built to last.",
         kind="showcase", imgs=[3, 2, 1], label="Brick & stone", detail="Townhome development", tail=1.0),
    dict(chap="03 · Our work", sub="And metal siding on a modern home: crisp lines and strong contrast.",
         kind="showcase", imgs=[6, 4, 5], label="Metal siding", detail="Modern home", tail=1.0),

    # ---------------- INSTALLATION ----------------
    dict(chap="04 · Installation", sub="Whatever you choose, installation decides how long it lasts.",
         kind="photo_text", img=5, lines=["*Installation*", "decides how long it lasts"]),
    dict(chap="04 · Installation", sub="Look for a properly lapped weather barrier, a drained gap, flashing over windows and doors, sealed cut edges, and clearance from the ground.",
         kind="card", head="Install checklist", kicker="WHAT TO LOOK FOR",
         items=[("ok", "Lapped weather barrier", "weather barrier"), ("ok", "Drained gap", "drained gap"),
                ("ok", "Flashing over openings", "flashing"), ("ok", "Sealed cut edges", "sealed"), ("ok", "Ground clearance", "clearance")]),

    # ---------------- WARNING SIGNS ----------------
    dict(chap="05 · Warning signs", sub="Time to replace? Watch for soft or swollen boards, peeling paint, mould, cracks, and stains on inside walls.",
         say="Time to replace? Watch for soft or swollen boards, peeling paint, mold, cracks, and stains on inside walls.",
         kind="card", head="Time to replace?", kicker="WARNING SIGNS",
         items=[("warn", "Soft or swollen boards", "soft or swollen"), ("warn", "Peeling paint", "peeling"),
                ("warn", "Mould", "mould"), ("warn", "Cracks", "cracks"), ("warn", "Stains on inside walls", "stains")]),
    dict(chap="05 · Warning signs", sub="Small fixes are cheap. Hidden water damage isn't.",
         kind="photo_text", img=4, lines=["Small fixes are *cheap.*", "Hidden water damage *isn't.*"]),

    # ---------------- CTA ----------------
    dict(chap="", sub="Building or renovating in North Vancouver?",
         kind="photo_text", img=6, lines=["Building or renovating in", "*North Vancouver?*"]),
    dict(chap="", sub="Visit silversiding.ca for a quote.",
         say="Visit silver siding dot C A, for a quote.",
         kind="end", tail=4.0),
]
