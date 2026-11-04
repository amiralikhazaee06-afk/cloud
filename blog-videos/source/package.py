"""Assemble one zip per blog post: video, thumbnail, title, caption (description), SRT, blog-update brief."""
import json, os, shutil, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
PKG = os.path.join(HERE, "..", "packages")
PKG_SVC = os.path.join(HERE, "..", "..", "service-videos", "packages")   # service-page videos live in their own folder

META = {
    "rainscreen": dict(
        zipname="01-what-is-a-rainscreen-wall",
        url="https://silversiding.ca/what-is-a-rainscreen-wall/",
        title="What Is a Rainscreen Wall? Is It Required in BC? (9.5 mm Rule)",
        alt_titles=["Rainscreen Wall Explained: How It Works & When BC Code Requires It",
                    "Rainscreen vs House Wrap: Does Your House Need a Rainscreen?"],
        hook="Your siding isn't waterproof. No siding is. A rainscreen wall gives the water that gets behind it a way out, and it's required on most siding along the BC coast.",
        bullets=["What a rainscreen wall is, and how the drained gap works",
                 "Rainscreen vs house wrap: is Tyvek a rainscreen?",
                 "How deep the gap must be (BC Building Code: 9.5 mm)",
                 "Is a rainscreen required in BC, and does vinyl, fibre cement or stucco need one?",
                 "Warning signs of a wall with no drainage path",
                 "Adding a rainscreen to an existing house, plus 3 questions to ask your contractor"],
        tags=["rainscreen", "rainscreen wall", "what is a rainscreen", "rain screen siding", "rainscreen system",
              "rainscreen vs house wrap", "is rainscreen required in bc", "bc building code rainscreen", "rainscreen gap",
              "furring strips", "capillary break", "leaky condo", "vancouver siding", "fibre cement rainscreen", "stucco rainscreen"],
        hashtags="#Rainscreen #BuildingScience #VancouverHomes"),
    "wetclimate": dict(
        zipname="02-metal-vs-vinyl-vs-fibre-cement-wet-climate",
        url="https://silversiding.ca/siding-for-wet-coastal-climate/",
        title="Metal vs Vinyl vs Fiber Cement Siding: Best for Rainy Climates?",
        alt_titles=["Best Siding for Wet Climates: Metal vs Vinyl vs Fibre Cement",
                    "Which Siding Survives Coastal Rain? Metal, Vinyl or Fibre Cement"],
        hook="Metal, vinyl or fibre cement (fiber cement): which siding actually lasts through months of coastal rain? Here's the short answer, and the wall detail that matters more than the material.",
        bullets=["The short answer for each material",
                 "Six forces that damage siding in a wet, coastal climate",
                 "Why strapping must run vertically (a red flag on quotes)",
                 "Does metal siding rust near the ocean?",
                 "Is vinyl siding waterproof? Does it need a rainscreen?",
                 "Does fibre cement need a rainscreen, even over taped sheathing?",
                 "Relative cost, which lasts longest, and how to choose"],
        tags=["best siding for wet climates", "metal vs vinyl siding", "fiber cement vs vinyl siding", "fibre cement siding",
              "fiber cement vs metal siding", "does metal siding rust", "is vinyl siding waterproof", "best siding for rainy climate",
              "coastal siding", "hardie board vs vinyl", "siding vancouver", "rainscreen", "siding comparison", "steel siding", "vinyl siding"],
        hashtags="#Siding #FiberCement #HomeExterior"),
    "lux": dict(
        zipname="03-lux-vs-longboard-vs-al13",
        url="https://silversiding.ca/lux-panels-vs-other-metal-siding/",
        title="LUX vs Longboard vs AL13 Siding: Steel or Aluminum? (Honest Comparison)",
        alt_titles=["LUX Panels vs Longboard: Steel vs Aluminum Wood-Look Siding",
                    "LUX Siding Review: How It Compares to Longboard and AL13"],
        hook="LUX, Longboard and AL13 get quoted side by side as if they were the same product. They're not: one is a steel plank, one an aluminum extrusion, one a composite panel system.",
        bullets=["What each product is made of, and why that decides everything",
                 "LUX vs Longboard: where steel wins, where aluminum wins",
                 "Warranties: what the 25, 15 and 20 years actually cover",
                 "Will hail dent metal siding? Does steel siding rust near the ocean?",
                 "LUX vs AL13: plank or panel?",
                 "The cost order, and how to use metal as a feature to save money",
                 "Maintenance, installation, and which one to choose"],
        tags=["lux siding", "lux panels", "lux metal siding", "longboard siding", "lux vs longboard", "al13 siding",
              "steel vs aluminum siding", "wood look metal siding", "woodgrain siding", "aluminum siding", "steel siding",
              "metal siding vancouver", "lux siding price", "longboard siding cost", "metal soffit"],
        hashtags="#MetalSiding #WoodLookSiding #HomeExterior"),
    "trends": dict(
        zipname="04-siding-design-ideas-2026",
        url="https://silversiding.ca/modern-custom-home-siding-trends/",
        title="Siding Design Ideas 2026: 10 Trends on Real Homes",
        alt_titles=["10 Siding Trends for 2026 (Colours, Board & Batten, Wood Look)",
                    "What Colour Is Replacing Grey? 10 Siding Ideas for 2026"],
        hook="Ten siding design ideas shaping homes in 2026, shown on real houses, plus how each one holds up when it rains for half the year.",
        bullets=["What colour is replacing grey: warm neutrals and earthy greens",
                 "High contrast, and bold, dark colours used with intent",
                 "Wide panels and minimalist flat panels",
                 "Is board-and-batten still in style?",
                 "The wood look without real wood: which material looks best",
                 "Mixed materials and accent-driven design",
                 "The lowest-maintenance modern siding",
                 "Follow a trend, or go timeless?"],
        tags=["siding design ideas 2026", "siding trends 2026", "siding colors 2026", "modern siding ideas", "house siding ideas",
              "board and batten siding", "vertical siding", "what color is replacing gray", "wood look siding", "dark siding",
              "two tone siding", "exterior house colors 2026", "modern house exterior", "siding ideas", "home exterior trends"],
        hashtags="#SidingIdeas #ExteriorDesign #HomeTrends"),
}


def mmss(t):
    t = int(t); return f"{t // 60}:{t % 60:02d}"


def chapters(name):
    raw = json.load(open(os.path.join(OUT, name, "chapters.json")))
    out = [(0.0, "Intro")]
    for c in raw:
        if c["chapter"] == out[-1][1]: continue
        if c["t"] - out[-1][0] < 10: out[-1] = (out[-1][0], c["chapter"]) if out[-1][1] != "Intro" else out[-1]; continue
        out.append((c["t"], c["chapter"]))
    return out


def caption(name, m):
    ch = "\n".join(f"{mmss(t)} {n}" for t, n in chapters(name))
    b = "\n".join(f"✔ {x}" for x in m["bullets"])
    if m.get("service"):
        import service_meta as SM
        return f"""{m['hook']}

In this video:
{b}

🔗 Service page (photos, FAQ and free estimate):
{m['url']}

Chapters:
{ch}

👷 Who we are: {SM.EEAT}
{SM.CONTACT}

{m['hashtags']}
"""
    return f"""{m['hook']}

In this video:
{b}

📖 Read the full guide (sources, tables and FAQ):
{m['url']}

Chapters:
{ch}

🏠 Planning new siding in Metro Vancouver? Send us a few photos of your house for a straight recommendation:
https://silversiding.ca/contact-us/

{m['hashtags']}
"""


def main(names):
    import service_meta as SM
    for k, v in SM.S.items():
        META[k] = dict(v, service=True)
    os.makedirs(PKG, exist_ok=True)
    for name in names:
        m = META[name]
        src = os.path.join(OUT, name)
        mp4 = os.path.join(src, f"{name}.mp4")
        assert os.path.exists(mp4), mp4
        pkg = PKG_SVC if m.get("service") else PKG
        os.makedirs(pkg, exist_ok=True)
        stage = os.path.join(pkg, m["zipname"])
        if os.path.exists(stage): shutil.rmtree(stage)
        os.makedirs(stage)
        shutil.copy(mp4, os.path.join(stage, "video.mp4"))
        shutil.copy(os.path.join(src, "thumbnail.jpg"), os.path.join(stage, "thumbnail.jpg"))
        shutil.copy(os.path.join(src, "subtitles.srt"), os.path.join(stage, "subtitles.srt"))
        if m.get("service"):
            shutil.copy(os.path.join(HERE, "briefs", "services", f"{m['num']:02d}-{m['slug']}.md"), os.path.join(stage, "page-update.md"))
            shutil.copy(os.path.join(HERE, "briefs", "services", "00-sitewide-eeat.md"), os.path.join(stage, "sitewide-eeat.md"))
        else:
            shutil.copy(os.path.join(HERE, "briefs", f"{name}.md"), os.path.join(stage, "blog-update.md"))
        open(os.path.join(stage, "title.txt"), "w").write(
            m["title"] + "\n\nAlternative titles (A/B test):\n" + "\n".join("- " + x for x in m["alt_titles"]) + "\n")
        open(os.path.join(stage, "caption.txt"), "w").write(caption(name, m))
        open(os.path.join(stage, "tags.txt"), "w").write(", ".join(m["tags"]) + "\n")
        z = os.path.join(pkg, m["zipname"] + ".zip")
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(os.listdir(stage)):
                ct = zipfile.ZIP_STORED if f.endswith((".mp4", ".jpg")) else zipfile.ZIP_DEFLATED
                zf.write(os.path.join(stage, f), os.path.join(m["zipname"], f), compress_type=ct)
        shutil.rmtree(stage)
        print(z, os.path.getsize(z) // (1024 * 1024), "MB")
        print(caption(name, m).split("Chapters:")[1].split("🏠")[0])


if __name__ == "__main__":
    main(sys.argv[1:] or [k for k in META])
