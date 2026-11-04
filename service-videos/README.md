# Silversiding service-page videos

One YouTube video (1920×1080, 16:9) for each service page on silversiding.ca, in Search Console order (most clicks and impressions first), plus a Persian update brief per page.

## Deliverables (`packages/`)
| Zip | Service page |
|---|---|
| `S01-allura-siding.zip` | /services/allura-siding/ |
| `S02-acm-panels.zip` | /services/acm-panels/ |
| `S03-soffit-installation-and-soffit-re-place.zip` | /services/soffit-installation-and-soffit-re-place/ |
| `S04-metal-siding.zip` | /services/metal-siding/ |
| `S05-lux-panels.zip` | /services/lux-panels/ |
| `S06-stone-siding.zip` | /services/stone-siding/ |
| `S07-longboard-siding.zip` | /services/longboard-siding/ |
| `S08-tyvek-air-barrier.zip` | /services/tyvek-air-barrier/ |
| `S09-al13-panels.zip` | /services/al13-panels/ |
| `S10-james-hardie-siding.zip` | /services/james-hardie-siding/ |
| `S11-siding-repair.zip` | /services/siding-repair/ |
| `S12-windows-preparation.zip` | /services/windows-preparation/ |
| `S13-vinyl-siding.zip` | /services/vinyl-siding/ |
| `S14-brick-and-stone-siding.zip` | /services/brick-and-stone-siding/ |
| `S15-rainscreen.zip` | /services/rainscreen/ |

Each zip contains `video.mp4`, `thumbnail.jpg`, `title.txt` (plus two A/B alternatives), `caption.txt` (description with timed chapters, E-E-A-T line and contact details), `tags.txt`, `subtitles.srt`, `page-update.md` (brief for this page, in Persian) and `sitewide-eeat.md` (issues shared by every page, in Persian).

## Notes
- **Brand:** written as "Silversiding" everywhere (subtitles, captions, screen); spoken as "Silverside".
- **E-E-A-T** in every video: who is talking (founded 2015 by Mahmoud Ardeshiri, 100+ projects, every job priced and walked by him), documented projects (Mountain Highway, North Vancouver; Mackenzie Street, Vancouver) where relevant, and the credentials scene (WorkSafeBC, liability insurance, written site safety plan, 5-year workmanship warranty). All facts come from the site's About and founder pages.
- **Photos:** real gallery photos are labelled the way the site labels them; AI renders are labelled "Illustration".
- **Source:** the videos are built with the shared tooling in `../blog-videos/source/` (scripts `scripts/svc*.py`, briefs `briefs/services/`).
