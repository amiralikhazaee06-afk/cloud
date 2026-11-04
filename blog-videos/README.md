# Silver Siding blog videos

One YouTube video (1920×1080, 16:9) for each blog post on silversiding.ca, plus a blog-update brief per post.

## Deliverables (`packages/`)
| Zip | Blog post | Video length |
|---|---|---|
| `01-what-is-a-rainscreen-wall.zip` | /what-is-a-rainscreen-wall/ | 5:15 |
| `02-metal-vs-vinyl-vs-fibre-cement-wet-climate.zip` | /siding-for-wet-coastal-climate/ | 5:45 |
| `03-lux-vs-longboard-vs-al13.zip` | /lux-panels-vs-other-metal-siding/ | 6:26 |
| `04-siding-design-ideas-2026.zip` | /modern-custom-home-siding-trends/ | 5:43 |

Each zip contains:
- `video.mp4`: H.264 1080p30, AAC 48 kHz, loudness normalised to −14 LUFS (YouTube's target). No burned-in subtitles.
- `subtitles.srt`: upload in YouTube Studio → Subtitles → English. YouTube indexes this text.
- `thumbnail.jpg`: 1280×720.
- `title.txt`: the recommended title plus two alternatives for YouTube's A/B "Test & compare".
- `caption.txt`: the YouTube description, with chapters timed from the actual video.
- `tags.txt`: YouTube tags.
- `blog-update.md`: brief (in Persian) for an AI model, covering what the post is missing and how to update it, based on Search Console, Google Autocomplete questions and competitor pages.

## How the videos were made (`source/`)
- `scripts/*.py`: the narration and on-screen content for each video, scene by scene. Each scene notes which searcher question it answers.
- `build.py`: text-to-speech (Kokoro, voice `af_heart`, speed 1.0), timeline, SRT, music and audio mix, parallel render, mux.
- `engine.py`: the motion-graphics renderer (style follows the reference reel: cream and black backgrounds, one red accent, pop-in type, cut-out cards).
- `thumbs.py`, `package.py`: thumbnails and zips.
- Pronunciation: subtitles keep the real spelling; the voice gets a respelling from the `PRON` table in `build.py` (`LUX` → "Lux", `AL13` → "A-L thirteen", `9.5 mm` → "nine and a half millimetres", `Hardie` → "Hardy"…). The build prints a warning for any remaining all-caps token, so acronyms are never spelled out by accident.

Rebuild a video (needs the Kokoro model in `.cache/kokoro/` and site photos in `media/`):

```bash
cd source && python3 build.py rainscreen && python3 thumbs.py && python3 package.py rainscreen
```

Photos come from the site's own blog posts and /gallery/ page. Real project photos are labelled "From our project gallery"; no material is named on a photo unless the file name states it.
