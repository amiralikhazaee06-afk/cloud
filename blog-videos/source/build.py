"""Build one video: TTS -> timeline -> SRT -> music/mix -> parallel render -> mux.

usage: python build.py <script_name> [--preview SECONDS_FROM:SECONDS_TO] [--stills]
"""
import hashlib, importlib, json, math, os, re, subprocess, sys, shutil
from multiprocessing import Pool
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "scripts"))
import engine as E

TTS_DIR = os.environ.get("TTS_DIR", os.path.join(HERE, "..", ".cache", "tts"))
MODEL_DIR = os.environ.get("KOKORO_DIR", os.path.join(HERE, "..", ".cache", "kokoro"))
VOICE, SPEED = "af_heart", 1.0
SR = 24000

# ---------------------------------------------------------------- pronunciation
# Display text keeps the real spelling (subtitles, screen). The voice gets a respelling.
PRON = [
    (r"\bLUX\b", "Lux"),                    # brand is said "lucks", never L-U-X
    (r"\bAL13\b", "A-L thirteen"),
    (r"\b9\.5\s?mm\b", "nine and a half millimetres"),
    (r"\b10\s?mm\b", "ten millimetres"),
    (r"\bPVDF\b", "P V D F"),
    (r"\bUV\b", "U V"),
    (r"\bACM\b", "A-C-M"),
    (r"\bSilversiding\b", "Silverside"),        # written "Silversiding", spoken "Silverside" (owner's request)
    (r"\bMahmoud Ardeshiri\b", "Mahmood Ardesheeree"),
    (r"\bMahmoud\b", "Mahmood"),
    (r"\bWorkSafeBC\b", "WorkSafe B C"),
    (r"\bAL13's\b", "A-L thirteen's"),
    (r"\bLUX's\b", "Lux's"),
    (r"\bZIP\b", "Zip"),
    (r"\bWRB\b", "weather barrier"),
    (r"\bAAMA\b", "Ah-ma"),
    (r"\bASTM\b", "A S T M"),
    (r"\bB117\b", "B one seventeen"),
    (r"\b2604\b", "twenty-six oh four"),
    (r"\b2605\b", "twenty-six oh five"),
    (r"\bCAN/ULC\b", "Can U L C"),
    (r"\bS102\b", "S one oh two"),
    (r"\bvs\.?\s", "versus "),
    (r"(\d+)\s?%", r"\1 percent"),
    (r"\b(\d+)\s?ft\b", r"\1 feet"),
    (r"\bHardie\b", "Hardy"),
    (r"\bTyvek\b", "Tie-vek"),
    (r"\bGalvalume\b", "Galvalume"),
    (r"\bstrata\b", "strata"),
    (r"\b1990s\b", "nineteen-nineties"),
    (r"\b1980s\b", "nineteen-eighties"),
    (r"\b2026\b", "twenty twenty-six"),
    (r"\b1998\b", "nineteen ninety-eight"),
    (r"\b2006\b", "two thousand six"),
    (r"\b2007\b", "two thousand seven"),
    (r"\b65,000\b", "sixty-five thousand"),
    (r"—", ", "),
    (r"\*", ""),
]
SPELL_OK = {"BC", "UV", "OK", "I"}

def pron(text):
    s = text
    for a, b in PRON: s = re.sub(a, b, s)
    return s.strip()


def caps_check(say):
    bad = [w for w in re.findall(r"\b[A-Z]{2,}\d*\b", say) if w not in SPELL_OK]
    return bad


# ---------------------------------------------------------------- TTS
_k = None
def kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(MODEL_DIR, "kokoro-v1.0.onnx"), os.path.join(MODEL_DIR, "voices-v1.0.bin"))
    return _k


def tts(say):
    os.makedirs(TTS_DIR, exist_ok=True)
    h = hashlib.sha1(f"{VOICE}|{SPEED}|{say}".encode()).hexdigest()[:16]
    p = os.path.join(TTS_DIR, h + ".wav")
    if not os.path.exists(p):
        a, sr = kokoro().create(say, voice=VOICE, speed=SPEED, lang="en-us")
        idx = np.where(np.abs(a) > 0.008)[0]
        a = a[max(0, idx[0] - int(0.02 * sr)): idx[-1] + int(0.06 * sr)]
        # 8 ms fades so joins never click
        f = int(0.008 * sr); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
        sf.write(p, a, sr)
    a, sr = sf.read(p, dtype="float32")
    return a


# ---------------------------------------------------------------- subtitles
def fmt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_cue(text, maxc=84):
    """split a sentence into chunks of <= maxc chars at natural breaks"""
    text = text.replace("*", "")
    if len(text) <= maxc: return [text]
    words = text.split(); chunks, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxc:
            chunks.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
            if re.search(r"[,;:]$", w) and len(cur) > maxc * 0.45:
                chunks.append(cur); cur = ""
    if cur: chunks.append(cur)
    return chunks


def two_lines(c, maxl=42):
    if len(c) <= maxl: return c
    words = c.split(); best, bi = 1e9, 1
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        sc = abs(len(a) - len(b)) + (0 if len(a) <= maxl + 4 and len(b) <= maxl + 4 else 100)
        if sc < best: best, bi = sc, i
    return " ".join(words[:bi]) + "\n" + " ".join(words[bi:])


def write_srt(scenes, path):
    n, out = 1, []
    for s in scenes:
        for (txt, _), (c0, c1) in zip(s["_vo"], s["_cues"]):
            a0, a1 = s["_start"] + c0, s["_start"] + c1
            chunks = split_cue(txt)
            tot = sum(len(c) for c in chunks)
            t = a0
            for c in chunks:
                d = (a1 - a0) * len(c) / tot
                out.append(f"{n}\n{fmt(t)} --> {fmt(t + d - 0.02)}\n{two_lines(c)}\n"); n += 1; t += d
    open(path, "w", encoding="utf-8").write("\n".join(out))


# ---------------------------------------------------------------- music + sfx
def music(T, seed=3):
    SRm = 48000; n = int(SRm * T); t = np.arange(n) / SRm
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    chords = [[53, 57, 60, 64], [57, 60, 64, 67], [55, 60, 64, 71], [55, 62, 67, 69]]
    CL = 8.0; pad = np.zeros(n)
    rng = np.random.default_rng(seed)
    for ci in range(int(T / CL) + 2):
        notes = chords[ci % 4]; a, b = ci * CL - 2.5, (ci + 1) * CL + 2.5
        i0, i1 = max(0, int(a * SRm)), min(n, int(b * SRm))
        if i0 >= i1: continue
        tt = t[i0:i1]; env = np.sin(np.clip((tt - a) / (b - a), 0, 1) * np.pi) ** 1.5
        seg = np.zeros(len(tt))
        for m in notes:
            f = hz(m)
            for det in (-0.1, 0.0, 0.1):
                seg += np.sin(2 * np.pi * f * (1 + det / 100) * tt + rng.random() * 6) * 0.3
        seg += 0.8 * np.sin(2 * np.pi * hz(notes[0] - 12) * tt)
        pad[i0:i1] += seg * env
    # soft plucks on an eighth-note grid at 96 bpm for gentle forward motion
    pl = np.zeros(n); beat = 60 / 96 / 2; tb = 0.5; k = 0
    while tb < T - 2:
        if k % 2 == 0 or rng.random() < 0.35:
            ci = int(tb / CL) % 4; m = int(rng.choice(chords[ci])) + 12
            i0 = int(tb * SRm); L = int(1.6 * SRm); i1 = min(n, i0 + L); tt = np.arange(i1 - i0) / SRm
            env = (1 - np.exp(-tt / 0.006)) * np.exp(-tt / 0.35)
            f = hz(m); pl[i0:i1] += env * (np.sin(2 * np.pi * f * tt) + 0.2 * np.sin(4 * np.pi * f * tt))
        tb += beat; k += 1
    mix = pad / np.abs(pad).max() * 0.6 + pl / max(1e-6, np.abs(pl).max()) * 0.28
    mix *= np.clip(t / 2.5, 0, 1) * np.clip((T - t) / 4.0, 0, 1)
    mix /= np.abs(mix).max() * 1.1
    return np.stack([mix, np.roll(mix, int(0.012 * SRm))], 1).astype(np.float32), SRm


def whoosh(SRm=48000, d=0.5, seed=1):
    rng = np.random.default_rng(seed); n = int(d * SRm)
    x = rng.normal(0, 1, n); t = np.arange(n) / n
    # crude band sweep: moving average with shrinking window
    out = np.zeros(n); acc = 0.0
    for w in (40, 20, 10, 5):
        k = np.ones(w) / w; y = np.convolve(x, k, mode="same")
        out += y * np.exp(-((t - (0.2 + 0.15 * (40 / w) / 8)) ** 2) / 0.02)
    env = np.sin(np.clip(t, 0, 1) * np.pi) ** 2
    out *= env; out /= np.abs(out).max()
    return out.astype(np.float32)


# ---------------------------------------------------------------- render workers
def _work(args):
    name, a, b, out = args
    mod = importlib.import_module(name)
    scenes, total, chapters = prepare(mod, quiet=True)
    E.render_video(scenes, total, chapters, out, start=a, end=b)
    return out


def prepare(mod, quiet=False):
    scenes = mod.SCENES
    durs = []
    for s in scenes:
        vo = []
        for v in s.get("vo", []):
            txt, say = (v if isinstance(v, tuple) else (v, pron(v)))
            bad = caps_check(say)
            if bad and not quiet: print("  !! check pronunciation:", bad, "in:", say)
            vo.append((txt, say))
        s["_vo"] = vo
        durs.append([len(tts(say)) / SR for _, say in vo])
    total = E.build_timeline(scenes, durs)
    chapters = [(s["_start"], s["chapter"]) for s in scenes if s.get("chapter")]
    return scenes, total, chapters


def build(name, outdir, preview=None, stills=False, workers=4):
    mod = importlib.import_module(name)
    os.makedirs(outdir, exist_ok=True)
    scenes, total, chapters = prepare(mod)
    print(f"{name}: {total:.1f}s, {len(scenes)} scenes")
    if stills:
        for i, s in enumerate(scenes):
            T = s["_start"] + min(s["_dur"] - 0.2, max(s["_dur"] * 0.85, 1.2))
            E.frame_at(scenes, T, total, chapters).save(os.path.join(outdir, f"still_{i:02d}.jpg"), quality=82)
        return
    # ---- audio
    SRm = 48000
    voice = np.zeros(int((total + 1) * SRm), np.float32)
    for s in scenes:
        for (txt, say), (c0, c1) in zip(s["_vo"], s["_cues"]):
            a = tts(say)
            a48 = np.interp(np.arange(int(len(a) * SRm / SR)) / SRm, np.arange(len(a)) / SR, a).astype(np.float32)
            i0 = int((s["_start"] + c0) * SRm); voice[i0:i0 + len(a48)] += a48
    mus, _ = music(total + 1)
    wh = whoosh()
    sfx = np.zeros_like(voice)
    for s in scenes[1:]:
        i0 = int((s["_start"] - 0.22) * SRm)
        if i0 > 0: sfx[i0:i0 + len(wh)] += wh[:len(sfx) - i0]
    # duck music under the voice
    env = np.convolve(np.abs(voice), np.ones(4800) / 4800, mode="same")
    duck = 1 - 0.45 * np.clip(env / (env.max() * 0.25 + 1e-6), 0, 1)
    m = mus[:len(voice)] * (0.16 * duck)[:, None]
    mix = voice[:, None] * 0.92 + m + sfx[:, None] * 0.05
    sf.write(os.path.join(outdir, "mix.wav"), mix, SRm)
    write_srt(scenes, os.path.join(outdir, "subtitles.srt"))
    json.dump([{"t": round(st, 2), "chapter": c} for st, c in chapters], open(os.path.join(outdir, "chapters.json"), "w"), indent=1)
    # ---- video
    a, b = (0, total) if not preview else preview
    seg = (b - a) / workers
    jobs = [(name, a + i * seg, a + (i + 1) * seg, os.path.join(outdir, f"part{i}.mp4")) for i in range(workers)]
    with Pool(workers) as p: p.map(_work, jobs)
    lst = os.path.join(outdir, "parts.txt")
    open(lst, "w").write("".join(f"file '{os.path.basename(j[3])}'\n" for j in jobs))
    out = os.path.join(outdir, f"{name}.mp4" if not preview else "preview.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-ss", str(a),
                    "-i", os.path.join(outdir, "mix.wav"), "-t", str(b - a),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", out], check=True)
    for j in jobs: os.remove(j[3])
    os.remove(lst)
    print("wrote", out)
    return out


if __name__ == "__main__":
    name = sys.argv[1]
    outdir = os.path.join(HERE, "..", "out", name)
    prev = None
    if "--preview" in sys.argv:
        a, b = sys.argv[sys.argv.index("--preview") + 1].split(":"); prev = (float(a), float(b))
    build(name, outdir, preview=prev, stills="--stills" in sys.argv)
