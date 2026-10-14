import json, sys, numpy as np, soundfile as sf
sys.path.insert(0, ".")
from script import SCENES
from kokoro_onnx import Kokoro
k = Kokoro("tts/kokoro-v1.0.onnx", "tts/voices-v1.0.bin")
out = []
for i, s in enumerate(SCENES):
    text = s.get("say", s["sub"])
    a, sr = k.create(text, voice="af_heart", speed=0.97, lang="en-us")
    # trim leading/trailing near-silence
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0]-int(.03*sr)): idx[-1]+int(.08*sr)]
    sf.write(f"tts/s{i:02d}.wav", a, sr)
    out.append(len(a)/sr); print(i, round(len(a)/sr, 2), flush=True)
json.dump(dict(sr=sr, durs=out), open("tts/durs.json", "w"))
print("total", sum(out))
