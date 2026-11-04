"""Shared scenes for the service-page videos.

E-E-A-T facts below are taken only from silversiding.ca (About page and founder page, Nov 2026):
- registered 2015 by founder Mahmoud Ardeshiri, who started in BC cladding as an hourly labourer
- 100+ completed projects; Mahmoud prices and walks every job and sets out panel layouts himself
- five-year workmanship warranty; WorkSafeBC registered; full liability insurance;
  documented site safety plan per project; silica dust controlled at source
- based in West Vancouver; works across Metro Vancouver
Written brand: "Silversiding" (spoken as "Silverside" via build.PRON).
"""
INKC, REDC, GREYC = (22, 22, 24), (222, 34, 40), (90, 90, 96)
G = "From our project gallery"


def who(chapter, img, service_line, variant=0, label=G, **kw):
    """EEAT intro: who is talking, and why they know this material."""
    openers = [
        "This is Silversiding, a cladding contractor based in West Vancouver.",
        "We're Silversiding, an exterior cladding team working across Metro Vancouver.",
        "I'm speaking for Silversiding, a West Vancouver cladding contractor.",
    ]
    d = dict(kind="photo", chapter=chapter, img=img, side="right", label=label,
             kicker="Who's talking", title="Silversiding, *since 2015*",
             items=[dict(t="Founded by Mahmoud Ardeshiri", s="started on BC job sites as an hourly labourer", at=0.5, k="check"),
                    dict(t="100+ completed projects", at=1, k="check"),
                    dict(t="Every job priced and walked by Mahmoud", at=1.5, k="check"),
                    dict(t="5-year workmanship warranty", at=2, k="check")],
             vo=[openers[variant % 3] + " Our founder, Mahmoud Ardeshiri, started on BC job sites as an hourly labourer, and registered the company in 2015.",
                 "Since then we've completed more than a hundred projects, and Mahmoud still prices and walks every job himself.",
                 service_line])
    d.update(kw)
    return d


def credentials(chapter="Before you hire", variant=0):
    lines = [
        ["Whoever you hire, ask for proof of these. Here's what we carry on every job: WorkSafeBC registration, and full liability insurance.",
         "A written site safety plan for each project, with fall protection and dust control when we cut.",
         "And a five-year workmanship warranty on the installation itself, on top of the manufacturer's product warranty."],
        ["Before you sign with any contractor, check four things. Are they registered with WorkSafeBC, and fully insured? We are, on every project.",
         "Do they issue a written safety plan for your job? Ours includes fall protection and silica dust control.",
         "And does the workmanship come with its own warranty? Ours is five years, separate from the product warranty."],
    ][variant % 2]
    return dict(kind="bullets", chapter=chapter, kicker="Ask any contractor for this", title="Proof, *not promises*",
                icon="check", isize=44, igap=30,
                items=[dict(t="Registered with WorkSafeBC", at=0),
                       dict(t="Full liability insurance on every job", at=0.5),
                       dict(t="Written site safety plan per project", s="fall protection, silica dust controlled at source", at=1),
                       dict(t="5-year workmanship warranty", s="separate from the manufacturer's product warranty", at=2)],
                vo=lines)


def end(url, title, sub="Free estimate. Mahmoud walks the job himself.", say=None):
    return dict(kind="end", title=title, url=url, sub=sub, url_at=0.6,
                vo=say or ["If you'd like a straight answer for your own house, send us a few photos, or book a free estimate.",
                           "Mahmoud will walk the job himself. Details are on the page linked below."])
