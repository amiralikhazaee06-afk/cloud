"""YouTube metadata + thumbnail spec for the 15 service-page videos (written brand: Silversiding)."""
EEAT = ("Silversiding is a West Vancouver cladding contractor, founded in 2015 by Mahmoud Ardeshiri. "
        "100+ completed projects · WorkSafeBC registered · fully insured · 5-year workmanship warranty.")
CONTACT = "📞 (778) 522-1384 · ✉ info@silversiding.ca · Free on-site estimates across Metro Vancouver"

S = {}
def svc(key, num, slug, title, alts, hook, bullets, tags, hashtags, thumb):
    S[key] = dict(num=num, slug=slug, zipname=f"S{num:02d}-{slug}", url=f"https://silversiding.ca/services/{slug}/",
                  title=title, alt_titles=alts, hook=hook, bullets=bullets, tags=tags, hashtags=hashtags, thumb=thumb)

svc("svc01_allura", 1, "allura-siding", "Allura Siding: Colours, Cost & Allura vs James Hardie (Vancouver)",
    ["Allura Fibre Cement Siding: Spectrum Colours & Honest Review", "Allura vs James Hardie: Which Fibre Cement Siding?"],
    "Allura fibre cement siding explained by a Vancouver installer: the 25 Spectrum colours, primed vs pre-finished, how it compares with James Hardie, and how it should be installed in a wet climate.",
    ["What Allura siding is made of, and the four profiles", "Spectrum colours: 25 factory-applied finishes", "Primed or pre-finished: which makes sense here",
     "Allura vs James Hardie, honestly", "How we install fibre cement, step by step", "Cost factors, lifespan and maintenance"],
    ["allura siding", "allura siding colors", "allura spectrum colors", "allura vs hardie", "allura fiber cement siding", "fibre cement siding vancouver",
     "allura siding cost", "allura siding canada", "fiber cement siding", "james hardie vs allura", "siding vancouver"],
    "#AlluraSiding #FiberCement #VancouverHomes",
    dict(photo="Allura-Siding-Burnaby.webp", lines=["ALLURA", "SIDING"], accent="COLOURS & COST", pill="vs HARDIE?"))

svc("svc02_acm", 2, "acm-panels", "ACM Panels Explained: Fire Rating, Cost & Installation (Vancouver)",
    ["ACM Cladding: What It Is, Fire Safety & Proper Installation", "Aluminum Composite Panels: Before You Choose Them"],
    "ACM (aluminum composite) panels explained by a Vancouver cladding contractor: what they're made of, where they make sense, the fire-rating question, and where installations go wrong.",
    ["What ACM cladding is made of", "Where ACM makes sense: commercial, strata and homes", "Is ACM fire safe? Polyethylene vs fire-rated cores",
     "Our installation process and panel layout", "Cost, lifespan and maintenance"],
    ["acm panels", "acm cladding", "aluminum composite panel", "acm panel installation", "acm fire rating", "acm panels vancouver",
     "acm exterior panels", "acm cladding contractor", "composite panel siding", "metal panel facade"],
    "#ACMPanels #Cladding #Architecture",
    dict(photo="ACM-Panel-Vancouver.webp", lines=["ACM", "PANELS"], accent="FIRE SAFE?", pill="BEFORE YOU BUY"))

svc("svc03_soffit", 3, "soffit-installation-and-soffit-re-place", "Soffit and Fascia: Repair or Replace? Materials That Last in BC Rain",
    ["Soffit vs Fascia Explained (and When to Replace Them)", "Vented or Solid Soffit? Soffit & Fascia Guide for Vancouver Homes"],
    "Soffit and fascia explained: what each one does, vented vs solid soffit, which materials last in a wet climate, and how to tell whether yours needs a repair or a replacement.",
    ["Soffit vs fascia: what each one does", "Do you need vented soffit?", "Aluminum, fibre cement, vinyl or cedar", "Repair or replace: check what's behind it",
     "On its own, or with new siding?", "Our three-step process"],
    ["soffit and fascia", "soffit replacement", "soffit vs fascia", "vented soffit", "aluminum soffit", "fascia replacement", "soffit repair",
     "metal soffit vancouver", "soffit installation", "fascia installation vancouver"],
    "#Soffit #Fascia #HomeMaintenance",
    dict(photo="soffit-vancouver.webp", lines=["SOFFIT &", "FASCIA"], accent="REPAIR OR REPLACE?", pill="BC RAIN"))

svc("svc04_metal", 4, "metal-siding", "Metal Siding in Vancouver: Steel vs Aluminum, Rust, Cost & Install",
    ["Steel vs Aluminum Siding: Which Is Better on the Coast?", "Metal Siding Pros & Cons: Rust, Fading, Dents (Honest Answers)"],
    "Metal siding for a wet coastal climate: aluminum vs steel, profiles and finishes, honest answers on rust, fading and dents, how it compares with vinyl and fibre cement, and what a good installation looks like.",
    ["Aluminum or steel?", "Profiles: lap, vertical, board-and-batten, corrugated, standing seam", "Will metal siding rust, fade or dent?",
     "Metal vs vinyl vs fibre cement", "Why panel layout matters", "Cost factors and lifespan"],
    ["metal siding", "metal siding vancouver", "steel vs aluminum siding", "aluminum siding", "steel siding", "metal siding cost",
     "does metal siding rust", "corrugated metal siding", "standing seam siding", "metal cladding vancouver"],
    "#MetalSiding #ModernHomes #Vancouver",
    dict(photo="metal-siding-in-west-vancouver-by-silver-siding-exterior.webp", lines=["METAL", "SIDING"], accent="STEEL OR ALUMINUM?", pill="RUST? DENTS?"))

svc("svc05_lux", 5, "lux-panels", "LUX Panels Installation: Finishes, Warranty & Cost (Vancouver)",
    ["LUX Siding: Steel Wood-Look Panels Explained by an Installer", "LUX Panels: Profiles, Soffit, Warranty & Installation"],
    "LUX steel panels explained by a Vancouver installer: what they are, the four finish families, horizontal, vertical and soffit profiles, what the 25-year warranty covers, and how they should be installed.",
    ["What LUX panels are made of", "Woodgrain, knotty, metallic and textured finishes", "Horizontal, vertical or vented soffit", "What the warranty covers (and what it doesn't)",
     "Why not to install it yourself", "LUX vs Longboard, vinyl and wood", "Cost factors"],
    ["lux panels", "lux siding", "lux panel installation", "lux siding installation", "lux metal siding", "lux soffit", "lux panel colours",
     "wood look steel siding", "lux siding vancouver", "lux vs longboard"],
    "#LUXPanels #MetalSiding #WoodLook",
    dict(photo="LUX-Panels-vs.-Other-Metal-Siding-1.webp", crop=(0, 0, 1, 0.74), lines=["LUX", "PANELS"], accent="INSTALLED RIGHT", pill="25-YR FINISH"))

svc("svc06_stone", 6, "stone-siding", "Stone Veneer Siding: Cultured vs Natural, Cost & Installation",
    ["Cultured Stone vs Natural Stone Veneer: What to Know", "Stone Veneer on a Rainy Coast: Done Right"],
    "Stone veneer siding explained: natural, cultured, faux panels and stacked stone, where it works best, when it isn't the right choice, and why the wall behind it decides whether it lasts.",
    ["Four types of stone veneer", "Where stone veneer works best", "When it isn't the right call", "Does stone veneer handle our rain?", "Our installation process", "Cost, home value and lifespan"],
    ["stone veneer siding", "cultured stone", "stone veneer installation", "cultured stone vs natural stone", "stone veneer cost", "stacked stone veneer",
     "stone veneer vancouver", "faux stone siding", "stone cladding", "exterior stone veneer"],
    "#StoneVeneer #CulturedStone #CurbAppeal",
    dict(photo="IMG_8434.jpeg", lines=["STONE", "VENEER"], accent="CULTURED OR NATURAL?", pill="DONE RIGHT"))

svc("svc07_longboard", 7, "longboard-siding", "Longboard Siding: Wood-Look Aluminum Explained (Cost & Install)",
    ["Longboard Siding Review: Wood Grain Without the Upkeep", "Longboard vs Wood, Vinyl & LUX: Where It Earns Its Premium"],
    "Longboard wood-grain aluminum siding explained: what it is, the finishes, where it's used, how it compares with wood, vinyl and LUX, and how it's installed with concealed clips.",
    ["What Longboard siding is", "Finishes and where it's used", "Longboard vs wood, vinyl and LUX steel", "Concealed-clip installation", "Cost and lifespan"],
    ["longboard siding", "longboard aluminum siding", "wood look aluminum siding", "longboard siding cost", "longboard cladding", "longboard soffit",
     "woodgrain siding", "longboard vs lux", "aluminum siding vancouver", "longboard installation"],
    "#Longboard #WoodLookSiding #Aluminum",
    dict(photo="Aluminum-long-board-vancouver.webp", lines=["LONGBOARD", "SIDING"], accent="WOOD LOOK, NO UPKEEP", pill="ALUMINUM"))

svc("svc08_tyvek", 8, "tyvek-air-barrier", "Is Tyvek a Vapour Barrier? Tyvek Air Barrier Installation Explained",
    ["Tyvek Air Barrier: What It Does and Where It Fails", "House Wrap vs Air Barrier vs Vapour Barrier (Tyvek Explained)"],
    "The layer behind your siding you'll never see: what a Tyvek air barrier does, air barrier vs vapour barrier, why stapled-up house wrap isn't an air barrier, and where installations fail.",
    ["What a Tyvek air barrier does", "Is Tyvek a vapour barrier?", "House wrap vs a true air barrier", "Where air barriers fail: the details", "DIY or professional?", "When it gets installed"],
    ["tyvek", "tyvek house wrap", "is tyvek a vapor barrier", "tyvek air barrier", "air barrier vs vapor barrier", "house wrap installation",
     "weather resistive barrier", "tyvek installation", "building envelope", "tyvek vs zip"],
    "#Tyvek #BuildingScience #HouseWrap",
    dict(photo="IMG-20250926-WA0006.jpg", lines=["TYVEK"], accent="VAPOUR BARRIER?", pill="NO, AND THAT'S GOOD", size=170))

svc("svc09_al13", 9, "al13-panels", "AL13 Panels vs Plank: Fire Rating, Cost & How It's Installed",
    ["AL13 Siding Explained: Panel and Plank Systems", "AL13 Cladding: Cut on Site, Snap-Locked, Rainscreen Built In"],
    "AL13 aluminum cladding explained: the Panel and Plank systems, how the snap-lock frame and built-in pressure-equalized rainscreen work, fire-rated cores, and how it compares with ACM, LUX and vinyl.",
    ["Panel System vs Plank System", "What makes AL13 different", "Fire rating: PE vs FR core", "AL13 vs ACM, LUX and vinyl", "Our installation process", "Cost and lifespan"],
    ["al13", "al13 panels", "al13 siding", "al13 plank", "aluminum panel siding", "al13 vs acm", "pressure equalized rainscreen",
     "al13 installation", "architectural panels", "modern siding"],
    "#AL13 #MetalPanels #Architecture",
    dict(photo="AL13-panelSystem-Vancouver.jpeg", lines=["AL13"], accent="PANEL OR PLANK?", pill="RAINSCREEN BUILT IN", size=200))

svc("svc10_hardie", 10, "james-hardie-siding", "James Hardie Siding: Cost, Lifespan, Asbestos & Proper Installation",
    ["James Hardie Fibre Cement: What Vancouver Homeowners Should Know", "Hardie Board Siding: Only as Good as the Install"],
    "James Hardie fibre cement siding explained by a Vancouver contractor: Plank, Panel and Trim, who it suits, lifespan, asbestos and repainting questions, comparisons, and how it must be installed.",
    ["The James Hardie range: Plank, Panel, Trim", "Who James Hardie suits", "Lifespan, asbestos and repainting", "Hardie vs vinyl, stucco and Allura", "Installed to Hardie's details", "What sets the cost"],
    ["james hardie siding", "hardie board", "fiber cement siding", "hardie board cost", "james hardie vancouver", "hardie plank", "hardie panel",
     "does hardie board contain asbestos", "hardie vs vinyl", "fibre cement siding installer"],
    "#JamesHardie #FiberCement #Siding",
    dict(photo="james-hardie-coquitlam.jpeg", lines=["JAMES", "HARDIE"], accent="ONLY AS GOOD AS THE INSTALL", pill="COST & LIFESPAN"))

svc("svc11_repair", 11, "siding-repair", "Siding Repair or Replacement? How to Tell (Vancouver Contractor)",
    ["Damaged Siding: Repair or Replace? 3 Things Decide It", "Signs of Water Damage Behind Your Siding"],
    "Can your siding be repaired, or does it need replacing? Three things decide it. Plus the warning signs of water behind siding, why small holes matter, matching, and how a proper repair is done.",
    ["Repair or replace: the three deciding factors", "Warning signs of water behind siding", "Why small repairs still need an assessment", "How each material fails",
     "Will the repair match?", "Our four-step repair process", "Storm damage, insurance and warranty"],
    ["siding repair", "siding repair vancouver", "siding replacement", "repair or replace siding", "water damage behind siding", "vinyl siding repair",
     "fiber cement siding repair", "metal siding repair", "storm damage siding", "siding contractor vancouver"],
    "#SidingRepair #HomeRepair #Vancouver",
    dict(photo="moisture-damaged-sheathing-behind-siding.webp", crop=(0, 0, 1, 0.88), lines=["REPAIR", "OR REPLACE?"], accent="DAMAGED SIDING", pill="HOW TO TELL"))

svc("svc12_windows", 12, "windows-preparation", "Window Flashing Before New Siding: Why Walls Leak at Windows",
    ["Window & Door Prep Before Siding (The Step That Stops Leaks)", "Replace Windows Before Siding? How Openings Should Be Prepared"],
    "Most walls leak at the windows, not in the middle. What preparing a window or door opening involves before new siding, what happens when it's skipped, and whether to replace windows first.",
    ["What window and door preparation involves", "What happens when it's skipped", "Windows or siding first?", "Openings we prepare", "Proof to ask any contractor for"],
    ["window flashing", "window installation siding", "flashing a window", "window prep", "should you replace windows before siding",
     "window sill pan", "window leaks", "building envelope", "siding installation", "window head flashing"],
    "#WindowFlashing #BuildingEnvelope #Siding",
    dict(photo="Tyvek_Air-Barrier-1.jpeg", lines=["WINDOWS", "LEAK FIRST"], accent="PREP BEFORE SIDING", pill="FLASHING"))

svc("svc13_vinyl", 13, "vinyl-siding", "Vinyl Siding Pros & Cons: Lifespan, Cost & How It Should Be Installed",
    ["Vinyl Siding: The Honest Version (Vancouver Contractor)", "Vinyl vs Fibre Cement vs Metal: When Vinyl Makes Sense"],
    "Vinyl siding, honestly: profiles, who it suits and who it doesn't, lifespan, fire and painting questions, comparisons with fibre cement, metal and aluminum, and the installation detail that matters most.",
    ["Three main profiles", "Who vinyl suits, and who it doesn't", "How long it lasts; fire; painting", "Vinyl vs fibre cement, metal and aluminum", "Hung loose, never nailed tight", "Repair or replace"],
    ["vinyl siding", "vinyl siding pros and cons", "vinyl siding lifespan", "vinyl siding vancouver", "insulated vinyl siding", "vinyl vs hardie",
     "vinyl siding installation", "vinyl siding repair", "can vinyl siding be painted", "vinyl siding cost"],
    "#VinylSiding #HomeExterior #Siding",
    dict(photo="Vinyl-Siding-Surrey.jpg", lines=["VINYL", "SIDING"], accent="THE HONEST VERSION", pill="PROS & CONS"))

svc("svc14_brickstone", 14, "brick-and-stone-siding", "Brick Veneer & Stone Siding: Options, Cost & Installation",
    ["Brick and Stone on One Wall: How to Combine Them", "Brick Veneer vs Thin Brick vs Stone: What's the Difference?"],
    "Brick and stone siding explained: veneer vs structural masonry, manufactured stone, brick veneer, thin brick and natural stone, how to combine them on one facade, and how it should be installed.",
    ["Veneer, not structural masonry", "Four options, light to heavy", "Combining brick and stone", "Honest trade-offs: weight, time, joints", "Our installation process"],
    ["brick veneer", "brick siding", "thin brick", "stone veneer", "brick and stone exterior", "brick veneer cost", "brick veneer vs brick",
     "manufactured stone", "natural stone veneer", "mixed material facade"],
    "#BrickVeneer #StoneSiding #CurbAppeal",
    dict(photo="brick-siding-north-vancouver-1.webp", lines=["BRICK &", "STONE"], accent="ON ONE WALL", pill="DONE RIGHT"))

svc("svc15_rainscreen", 15, "rainscreen", "Rainscreen Installation: Ventilated vs Drainscreen, Cost & Retrofit",
    ["Installing a Rainscreen Behind Siding: What It Takes", "Rainscreen vs Air Barrier: How They Work Together"],
    "Installing a rainscreen behind siding: how the drained gap works, ventilated vs drainscreen, which siding needs which, how it works with the air barrier, our installation steps, and BC code and retrofits.",
    ["How a rainscreen works", "Ventilated or drainscreen?", "Which siding benefits most", "Rainscreen vs air barrier", "Our installation process", "Code, retrofits and lifespan"],
    ["rainscreen", "rainscreen installation", "rain screen siding", "rainscreen retrofit", "ventilated rainscreen", "drainscreen", "rainscreen vancouver",
     "furring strips", "rainscreen contractor", "bc building code rainscreen"],
    "#Rainscreen #BuildingScience #Vancouver",
    dict(photo="DD6A9214-1.jpg", lines=["RAIN", "SCREEN"], accent="INSTALLED RIGHT", pill="RETROFIT?", diagram=True))
