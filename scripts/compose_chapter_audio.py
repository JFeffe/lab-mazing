"""Five original Folamour themes, synthesized without samples.

Run with Python/numpy and ffmpeg. Chapter 1 and existing effects are never written.
24-bar circular arrangements, matched to the original lounge's RMS loudness.
"""
import json
import subprocess
import numpy as np
from compose_audio import RATE, DEST, export

# Root, suspended/seventh electric-piano voicing; shared lounge vocabulary.
HARMONY = [
    (38, [53, 57, 60, 64]), (43, [53, 57, 59, 64]),
    (36, [52, 55, 59, 62]), (45, [55, 61, 65, 71]),
    (38, [53, 57, 60, 64]), (41, [57, 60, 64, 67]),
    (40, [55, 59, 62, 66]), (45, [55, 61, 65, 70]),
]
THEMES = [
    ('folamour_chapter2', 'Le tampon qui dansait', 84, [0, 5, 2, 1, 4, 6, 5, 7], [72, 76, 79, 76, 74, 77, 76, 73]),
    ('folamour_chapter3', 'La prévoyance en chaussons', 88, [4, 1, 6, 3, 5, 2, 0, 7], [74, 73, 77, 76, 79, 77, 74, 71]),
    ('folamour_chapter4', 'Le miroir prend des vacances', 92, [2, 6, 5, 3, 0, 1, 4, 7], [76, 79, 78, 74, 73, 77, 76, 70]),
    ('folamour_chapter5', 'Tout va presque bien', 96, [0, 6, 1, 3, 5, 4, 2, 7], [77, 76, 74, 79, 78, 76, 73, 74]),
    ('folamour_menu', 'Ouverture du service des catastrophes', 108, [0, 5, 1, 3, 2, 6, 4, 7], [74, 77, 76, 73, 79, 78, 76, 70]),
]

def compose_theme(name, title, bpm, progression, melody, reference_rms):
    beat = 60 / bpm
    music = np.zeros((round(24 * 4 * beat * RATE), 2))
    rng = np.random.default_rng(bpm)
    menu = name.endswith('menu')

    def add(signal, start, pan=0):
        idx = (round(start * RATE) + np.arange(len(signal))) % len(music)
        music[idx, 0] += signal * np.sqrt((1 - pan) / 2)
        music[idx, 1] += signal * np.sqrt((1 + pan) / 2)

    def note(midi, start, duration, gain, pan=0, bell=False, bend=False):
        t = np.arange(round(duration * RATE)) / RATE
        f = 440 * 2 ** ((midi - 69) / 12)
        phase = 2 * np.pi * f * t
        if bend:
            phase += .9 * (1 - np.exp(-t * 12))
        tone = (np.sin(phase + 1.1 * np.sin(2 * np.pi * f * 2.003 * t) * np.exp(-3 * t))
                if bell else np.sin(phase) + .23 * np.sin(2 * phase) * np.exp(-3 * t))
        env = (1 - np.exp(-t * 55)) * np.exp(-t / (duration * .32))
        env *= np.minimum(1, (duration - t) / .12)
        add(tone * env * gain, start, pan)

    for bar in range(24):
        section, phrase = divmod(bar, 8)
        root, chord = HARMONY[progression[phrase]]
        start = bar * 4 * beat
        # Walking bass only in the menu; chapters retain the spacious original pulse.
        for off, pitch in ([(0, root), (1.5, root + 7), (2, root + 12), (3.5, root + 7)]
                           if menu else [(0, root), (2.5, root + 12)]):
            note(pitch, start + off * beat, beat * (1.2 if menu else 2.5), .15 if off == 0 else .075, -.1)
        for off, strength in ([(.5, .08), (2, .05), (3.25, .055)] if menu else [(0, .085), (2.5, .035)]):
            for j, pitch in enumerate(chord):
                note(pitch, start + off * beat + .025 * j, beat * (1.5 if menu else 3.7), strength, (j - 1.5) * .15)
        pitch = melody[phrase]
        note(pitch, start + (1.5 if not menu else .5) * beat, 2.5 * beat, .045, -.35, True)
        # A contrasting middle section and a returning, varied last phrase.
        if section == 1 or menu:
            for off, reply in [(2.25, chord[-1] + 12), (3, pitch + (2 if phrase % 2 else -2))]:
                note(reply, start + off * beat, .9 * beat, .026 if not menu else .047, .35, True)
        elif section == 2 and phrase % 2 == 1:
            note(chord[1] + 12, start + 3.25 * beat, 1.4 * beat, .025, .3, True)
        if menu and phrase in [3, 7]:
            # A tiny wrong-footed flourish, answered by the next bar's soft bass.
            for k, p in enumerate([pitch + 1, pitch, pitch - 5]):
                note(p, start + (3.25 + k * .25) * beat, .45 * beat, .04, .2, True, True)
        for off in ([1, 2.5, 3] if menu else [1, 3]):
            t = np.arange(round(.13 * RATE)) / RATE
            brush = np.convolve(rng.normal(0, 1, len(t)), np.ones(12) / 12, 'same')
            add(brush * np.exp(-t * 40) * (.036 if menu else .022), start + off * beat)
    music += .19 * np.roll(music, round(.31 * RATE), axis=0)[:, ::-1] + .10 * np.roll(music, round(.63 * RATE), axis=0)
    music *= reference_rms / np.sqrt(np.mean(music ** 2))
    export(name, music, True)
    return dict(file=name + '.ogg', title=title, bpm=bpm, bars=24, seconds=len(music) / RATE)

if __name__ == '__main__':
    decoded = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(DEST / 'folamour_lounge.ogg'), '-f', 'f32le', '-ac', '2', '-ar', str(RATE), '-'])
    reference_rms = float(np.sqrt(np.mean(np.frombuffer(decoded, '<f4') ** 2)))
    tracks = [compose_theme(*theme, reference_rms) for theme in THEMES]
    print(json.dumps(tracks, ensure_ascii=False, indent=2))
