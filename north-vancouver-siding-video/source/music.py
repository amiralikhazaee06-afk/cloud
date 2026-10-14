import numpy as np, soundfile as sf, sys, random
SR = 44100; T = float(sys.argv[1]); n = int(SR * T)
t = np.arange(n) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
# warm, slow progression: Fmaj7 - Am7 - Cmaj7/G - Gsus2  (8 s per chord)
chords = [[53, 57, 60, 64], [57, 60, 64, 67], [55, 60, 64, 71], [55, 62, 67, 69]]
CL = 8.0
pad = np.zeros(n)
for ci in range(int(T / CL) + 2):
    notes = chords[ci % 4]
    a, b = ci * CL - 2.5, (ci + 1) * CL + 2.5
    i0, i1 = max(0, int(a * SR)), min(n, int(b * SR))
    if i0 >= i1: continue
    tt = t[i0:i1]
    env = np.sin(np.clip((tt - a) / (b - a), 0, 1) * np.pi) ** 1.5
    seg = np.zeros(len(tt))
    for m in notes:
        f = hz(m)
        for det in (-0.12, 0.0, 0.12):
            seg += np.sin(2 * np.pi * f * (1 + det / 100) * tt + random.random() * 6) * 0.33
        seg += 0.12 * np.sin(2 * np.pi * 2 * f * tt)
    root = hz(notes[0] - 12)
    seg += 0.9 * np.sin(2 * np.pi * root * tt)
    pad[i0:i1] += seg * env
# gentle low-pass (one-pole, run twice)
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    from itertools import accumulate
    # vectorised IIR via scipy-free trick: process in blocks with python loop on decimated signal
    return x
pad *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t) ** 2
# sparse soft "felt piano" notes
rng = random.Random(3); bell = np.zeros(n); tb = 1.0
while tb < T - 3:
    ci = int(tb / CL) % 4
    m = rng.choice(chords[ci]) + 12
    i0 = int(tb * SR); L = int(3.5 * SR); i1 = min(n, i0 + L); tt = np.arange(i1 - i0) / SR
    env = (1 - np.exp(-tt / 0.012)) * np.exp(-tt / 0.9)
    f = hz(m)
    bell[i0:i1] += env * (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt) + 0.08 * np.sin(2 * np.pi * 3 * f * tt))
    tb += rng.choice([2.0, 2.0, 4.0, 1.0, 3.0])
mix = pad / np.abs(pad).max() * 0.55 + bell / np.abs(bell).max() * 0.22
fade = np.clip(t / 3.0, 0, 1) * np.clip((T - t) / 5.0, 0, 1)
mix *= fade
mix /= np.abs(mix).max() * 1.12
st = np.stack([mix, np.roll(mix, int(0.011 * SR))], 1)
sf.write("out/music_raw.wav", st, SR)
