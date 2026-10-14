# Voice-over script + scene specs for the North Vancouver siding guide video.
# "say" = text sent to TTS (pronunciation-friendly); "sub" = on-screen subtitle (Canadian spelling).
# Tokens wrapped in *...* inside kinetic lines are the red accent words.

SCENES = [
    # ---------------- HOOK ----------------
    dict(chap="", sub="Your siding is the first thing people see.",
         kind="photo_text", img=3, lines=["Your siding is the", "*first thing*", "people see"]),
    dict(chap="", sub="And in North Vancouver, it's also your home's first line of defence.",
         say="And in North Vancouver, it's also your home's first line of defense.",
         kind="kinetic", bg="dark", lines=["And in North Vancouver,", "your first line of *defence*"]),
    dict(chap="", sub="Choose the wrong material, or install it the wrong way, and the rain will find every mistake.",
         kind="kinetic", bg="dark", lines=["Choose the wrong material,", "or install it the wrong way,", "and the rain will find *every mistake*"]),
    dict(chap="", sub="In this guide, we'll walk through how siding works on the North Shore, which materials hold up best, what a proper installation looks like, and how to know when it's time to replace yours.",
         kind="card", head="In this guide", style="list",
         items=[("dot", "Why the North Shore is different", "how siding works"),
                ("dot", "Which materials hold up best", "which materials"),
                ("dot", "What a proper install looks like", "proper installation"),
                ("dot", "When to replace your siding", "how to know")],
         kicker="NORTH VANCOUVER SIDING GUIDE"),

    # ---------------- 01 CLIMATE ----------------
    dict(chap="01 · Climate", sub="North Vancouver sits right against the mountains. Moist Pacific air hits the slopes and falls as rain, so the North Shore gets noticeably more rain than most of Metro Vancouver.",
         kind="chapter", num="01", lines=["Why North Vancouver", "is *different*"]),
    dict(chap="01 · Climate", sub="Add long, grey winters, salt air near the water, and shade from tall evergreens, and you get walls that stay damp for months.",
         kind="trio", bg="dark", words=[("Long, grey winters", "grey winters"), ("Salt air", "salt air"), ("Deep shade", "shade")],
         tail=("Walls that stay *damp*", "you get walls")),
    dict(chap="01 · Climate", sub="That's why, here in coastal B.C., the building code calls for a rainscreen on new wood-frame walls: a small air gap behind the siding that lets water drain out and the wall dry out.",
         say="That's why, here in coastal B C, the building code calls for a rainscreen on new wood-frame walls: a small air gap behind the siding that lets water drain out, and the wall dry out.",
         kind="rainscreen"),
    dict(chap="01 · Climate", sub="Siding alone doesn't keep water out. The system behind it does.",
         kind="kinetic", bg="dark", lines=["Siding alone doesn't keep water out.", "The *system* behind it does."], split_at="The system"),

    # ---------------- 02 MATERIALS ----------------
    dict(chap="02 · Materials", sub="So which material should you choose? Let's go through the main options.",
         kind="chapter", num="02", lines=["Choosing the right", "*material*"]),
    dict(chap="02 · Materials", sub="Fibre cement is the most popular choice on the North Shore. It's rot-proof, it won't burn, and it holds paint well. It's heavier and needs careful cutting, but it handles our wet climate very well.",
         say="Fiber cement is the most popular choice on the North Shore. It's rot-proof, it won't burn, and it holds paint well. It's heavier and needs careful cutting, but it handles our wet climate very well.",
         kind="card", head="Fibre cement", kicker="OPTION 1", badge="Best all-rounder",
         items=[("ok", "Rot-proof", "rot-proof"), ("ok", "Won't burn", "won't burn"), ("ok", "Holds paint well", "holds paint"),
                ("no", "Heavy, needs careful cutting", "heavier")]),
    dict(chap="02 · Materials", sub="Vinyl is the budget option. It's light and low-maintenance, but it can crack in the cold, fade in the sun, and it rarely matches the look of higher-end homes.",
         kind="card", head="Vinyl", kicker="OPTION 2", badge="Budget pick",
         items=[("ok", "Light, low-maintenance", "light and"), ("no", "Can crack in the cold", "crack"), ("no", "Fades in the sun", "fade"),
                ("no", "Looks less premium", "rarely matches")]),
    dict(chap="02 · Materials", sub="Engineered wood gives you a real wood look at a lower cost. Just keep in mind that every cut edge has to be sealed, or moisture will get in.",
         kind="card", head="Engineered wood", kicker="OPTION 3", badge="Wood look, lower cost",
         items=[("ok", "Real wood look", "real wood look"), ("ok", "Lower cost than cedar", "lower cost"), ("no", "Every cut edge must be sealed", "every cut edge")]),
    dict(chap="02 · Materials", sub="Natural cedar is beautiful, and a West Coast classic. But it needs regular staining or sealing, or it will grey, split, and rot.",
         kind="card", head="Natural cedar", kicker="OPTION 4", badge="West Coast classic",
         items=[("ok", "Beautiful, natural look", "beautiful"), ("no", "Needs regular stain or sealer", "regular staining"), ("no", "Can grey, split and rot", "split")]),
    dict(chap="02 · Materials", sub="Metal and composite panels give you the clean, modern look you see on new builds. They're durable and very low-maintenance, but the joints and corners have to be detailed perfectly.",
         kind="card", head="Metal & panels", kicker="OPTION 5", badge="Modern look",
         items=[("ok", "Clean, modern lines", "clean, modern"), ("ok", "Durable, low-maintenance", "durable"), ("no", "Joints must be perfect", "joints and corners")]),
    dict(chap="02 · Materials", sub="And for many modern homes, the best answer is a mix: brick or stucco in one area, and panels or lap siding in another.",
         kind="photo_side", img=4, lines=["Often, the best", "answer is a *mix*"], tags=["Stucco", "Metal panels", "Wood-tone soffits"]),

    # ---------------- 03 OUR WORK ----------------
    dict(chap="03 · Our work", sub="Here's what that looks like in real life.",
         kind="chapter", num="03", lines=["Real projects,", "real *results*"], grid=True),
    dict(chap="03 · Our work", sub="On this townhome project, warm brick is paired with dark lap siding on the upper floors. The black window boxes and trim tie it all together, and the darker top makes the building feel lighter and lower.",
         kind="showcase", imgs=[3, 2, 1], label="Townhome project", detail="Brick + dark lap siding"),
    dict(chap="03 · Our work", sub="On this duplex, smooth white stucco is combined with dark panels and warm wood-tone soffits. Clean lines, strong contrast, and every joint detailed to shed water.",
         kind="showcase", imgs=[4, 5], label="Duplex project", detail="Stucco + dark panels + wood-tone soffits"),

    # ---------------- 04 INSTALLATION ----------------
    dict(chap="04 · Installation", sub="Whatever material you pick, the installation decides how long it lasts. Here's what to look for.",
         kind="chapter", num="04", lines=["Installation is", "*everything*"]),
    dict(chap="04 · Installation", sub="A weather barrier lapped the right way. A drained rainscreen gap. Flashing above every window, door and deck. Sealed cut edges. And proper clearance from the ground and the roof.",
         kind="card", head="Install checklist", kicker="WHAT TO LOOK FOR", style="check",
         items=[("ok", "Weather barrier lapped correctly", "weather barrier"), ("ok", "Drained rainscreen gap", "drained"),
                ("ok", "Flashing above openings", "flashing"), ("ok", "Sealed cut edges", "sealed"), ("ok", "Ground & roof clearance", "clearance")]),
    dict(chap="04 · Installation", sub="If a contractor can't explain these details, keep looking.",
         kind="kinetic", bg="dark", lines=["Can't explain the details?", "*Keep looking.*"], split_at="keep looking"),

    # ---------------- 05 WARNING SIGNS ----------------
    dict(chap="05 · Warning signs", sub="So how do you know if your siding needs attention? Watch for soft or swollen boards, peeling paint that keeps coming back, mould or green staining, gaps and cracks, and stains on your inside walls.",
         say="So how do you know if your siding needs attention? Watch for soft or swollen boards, peeling paint that keeps coming back, mold or green staining, gaps and cracks, and stains on your inside walls.",
         kind="card", head="Time to check?", kicker="WARNING SIGNS", style="warn",
         items=[("warn", "Soft or swollen boards", "soft or swollen"), ("warn", "Paint that keeps peeling", "peeling"),
                ("warn", "Mould or green staining", "green staining"), ("warn", "Gaps and cracks", "gaps and"), ("warn", "Stains on inside walls", "stains on")]),
    dict(chap="05 · Warning signs", sub="Small problems are cheap to fix. Hidden water damage behind the siding is not.",
         kind="kinetic", bg="dark", lines=["Small problems are cheap to fix.", "Hidden water damage *is not.*"], split_at="Hidden"),

    # ---------------- 06 MAINTENANCE ----------------
    dict(chap="06 · Maintenance", sub="To help any siding last longer: wash it once a year, keep your gutters clean, trim plants back from the walls, and recheck the caulking around windows every couple of years.",
         kind="card", head="Make it last", kicker="MAINTENANCE", style="check",
         items=[("ok", "Wash it once a year", "wash"), ("ok", "Keep gutters clean", "gutters"), ("ok", "Trim plants back", "trim plants"), ("ok", "Recheck window caulking", "recheck")]),

    # ---------------- CTA ----------------
    dict(chap="", sub="Planning a new build, a renovation, or a siding replacement in North Vancouver? We'd be happy to help you choose the right material, and install it the right way.",
         kind="photo_text", img=5, lines=["Planning a project in", "*North Vancouver?*"]),
    dict(chap="", sub="Visit silversiding.ca to see more of our work and request a quote.",
         say="Visit silver siding dot C A, to see more of our work, and request a quote.",
         kind="end"),
    dict(chap="", sub="Thanks for watching. We'll see you on the North Shore.",
         kind="end", thanks=True),
]
