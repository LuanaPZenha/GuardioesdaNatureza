"""Trilhas originais em loop: exploração e chefe."""
import numpy as np
import pygame

RATE = 22050
_channel = None
_tracks = {}
_current = None


def _add(buf, start, dur, freq, kind, vol):
    i0 = int(start * RATE)
    n = int(dur * RATE)
    if n <= 0 or i0 >= len(buf):
        return
    n = min(n, len(buf) - i0)
    t = np.arange(n, dtype=np.float32) / RATE
    phase = (t * freq) % 1
    if kind == "sine":
        wave = np.sin(2 * np.pi * freq * t)
    elif kind == "square":
        wave = np.where(phase < 0.5, 1.0, -1.0).astype(np.float32)
    elif kind == "tri":
        wave = 2 * np.abs(2 * phase - 1) - 1
    else:
        wave = 2 * phase - 1
    env = np.ones(n, dtype=np.float32)
    attack = min(n // 4, int(0.03 * RATE))
    release = min(n // 3, int(0.11 * RATE))
    if attack > 0:
        env[:attack] = np.linspace(0, 1, attack, dtype=np.float32)
    if release > 0:
        env[-release:] *= np.linspace(1, 0, release, dtype=np.float32)
    buf[i0:i0 + n] += wave * env * vol


def _sound(buf):
    peak = float(np.max(np.abs(buf))) or 1.0
    pcm = np.clip(buf / max(1.0, peak) * 0.9, -1, 1)
    data = (pcm * 32767).astype(np.int16)
    return pygame.mixer.Sound(buffer=data.tobytes())


def _calm():
    seconds = 8.0
    buf = np.zeros(int(RATE * seconds), dtype=np.float32)
    beat = 0.5
    bass = [110, 82.41, 110, 82.41, 130.81, 146.83, 82.41, 110]
    for i, freq in enumerate(bass):
        _add(buf, i * beat * 2, beat * 1.7, freq, "tri", 0.22)
        _add(buf, i * beat * 2, beat * 1.7, freq * 2, "sine", 0.07)
    melody = [
        (0, 0.42, 659.25),
        (1, 0.36, 587.33),
        (2, 0.32, 523.25),
        (3, 0.7, 440),
        (6, 0.36, 523.25),
        (7, 0.36, 659.25),
        (8, 0.42, 783.99),
        (9, 0.36, 659.25),
        (10, 0.7, 587.33),
        (12, 0.36, 523.25),
        (13, 0.32, 440),
        (14, 0.3, 392),
        (15, 0.42, 440),
    ]
    for step, dur, freq in melody:
        _add(buf, step * beat, dur, freq, "square", 0.11)
        _add(buf, step * beat, dur, freq, "sine", 0.05)
    t = np.arange(len(buf), dtype=np.float32) / RATE
    pad = np.sin(2 * np.pi * 220 * t) * 0.05
    pad += np.sin(2 * np.pi * 330 * t) * 0.035
    edge = int(0.2 * RATE)
    fade = np.ones(len(buf), dtype=np.float32)
    fade[:edge] = np.linspace(0, 1, edge, dtype=np.float32)
    fade[-edge:] = np.linspace(1, 0, edge, dtype=np.float32)
    buf += pad * fade
    return _sound(buf)


def _boss():
    seconds = 8.0
    n = int(RATE * seconds)
    t = np.arange(n, dtype=np.float32) / RATE
    trem = 0.72 + 0.28 * np.sin(2 * np.pi * 0.25 * t)
    buf = np.sin(2 * np.pi * 73.5 * t) * 0.2 * trem
    buf += np.sin(2 * np.pi * 78 * t) * 0.11 * trem
    buf += (2 * ((t * 55) % 1) - 1) * 0.05 * trem
    for hit in (0, 1.6, 3.2, 4.8, 6.4):
        _add(buf, hit, 0.09, 48, "sine", 0.55)
        _add(buf, hit + 0.2, 0.07, 42, "sine", 0.38)
        _add(buf, hit + 0.72, 0.12, 110, "saw", 0.08)
    motif = [
        (0.45, 0.7, 622.25),
        (2.2, 0.65, 587.33),
        (4.05, 0.6, 523.25),
        (5.85, 0.9, 466.16),
        (7.15, 0.28, 622.25),
        (7.15, 0.28, 659.25),
    ]
    for start, dur, freq in motif:
        _add(buf, start, dur, freq, "saw", 0.09)
        _add(buf, start, dur, freq * 0.5, "square", 0.05)
    return _sound(buf)


def start():
    global _channel, _tracks
    if not pygame.mixer.get_init():
        return
    pygame.mixer.set_reserved(1)
    _channel = pygame.mixer.Channel(0)
    try:
        _tracks = {"calm": _calm(), "boss": _boss()}
    except pygame.error:
        _tracks = {}
        return
    play("calm")


def play(kind):
    global _current
    sound = _tracks.get(kind)
    if sound is None or _channel is None or _current == kind:
        return
    _current = kind
    _channel.set_volume(0.55 if kind == "boss" else 0.42)
    _channel.play(sound, loops=-1, fade_ms=280)
