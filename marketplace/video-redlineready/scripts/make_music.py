"""Placeholder background track: calm, upbeat ambient pad + soft pulse, ~96 BPM, 56 s.
Standard library only. Replace with a real royalty-free track (marketplace/assets/music.mp3)."""
import math, struct, wave, sys

SR, DUR, BPM = 22050, 56.0, 96
beat = 60 / BPM
bar = 4 * beat
N = int(SR * DUR)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
# vi - IV - I - V with sevenths/sixths (C major), a calmer, more deliberate feel than BidReady, voiced softly
chords = [[45, 57, 60, 64, 67], [41, 57, 60, 64, 69], [48, 60, 64, 67, 71], [43, 55, 59, 62, 64]]
arp = [[69, 72, 76, 72], [69, 72, 77, 72], [72, 76, 79, 76], [67, 71, 74, 71]]
out = [0.0] * N
two_pi = 2 * math.pi
for i in range(N):
    t = i / SR
    b = int(t // bar) % 4
    tb = t % bar
    # pad: slow swell per bar, sine + quiet 2nd harmonic
    env = min(1.0, tb / 0.8) * (0.85 + 0.15 * math.cos(two_pi * tb / bar))
    s = 0.0
    for k, m in enumerate(chords[b]):
        f = hz(m)
        w = 0.5 if k == 0 else 0.22
        s += w * (math.sin(two_pi * f * t) + 0.18 * math.sin(two_pi * 2 * f * t + 0.3))
    s *= 0.11 * env
    # soft pulse: eighth-note pluck arpeggio
    eighth = beat / 2
    n = int(tb // eighth)
    te = tb % eighth
    f = hz(arp[b][n % 4])
    s += 0.07 * math.exp(-te * 9) * (math.sin(two_pi * f * t) + 0.3 * math.sin(two_pi * 2 * f * t))
    # gentle kick-like thump on beats 1 and 3
    tq = tb % (2 * beat)
    s += 0.16 * math.exp(-tq * 18) * math.sin(two_pi * (55 + 60 * math.exp(-tq * 30)) * tq)
    out[i] = s
peak = max(abs(x) for x in out) or 1
with wave.open(sys.argv[1], "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b"".join(struct.pack("<h", int(32767 * 0.85 * x / peak)) for x in out))
print("wrote", sys.argv[1], DUR, "s")
