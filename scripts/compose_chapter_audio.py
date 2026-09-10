"""Five original Folamour themes, synthesized without samples.

Run with Python/numpy and ffmpeg. Chapter 1 and existing effects are never written.
24-bar circular arrangements, matched to the original lounge's RMS loudness.
"""
import json
import argparse
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

def compose_menu(reference_rms):
    """A relaxed spy-lounge shuffle: a real drum pocket and a recurring hook."""
    bpm, bars, swing = 100, 24, .61
    beat = 60 / bpm
    music = np.zeros((round(bars * 4 * beat * RATE), 2))
    rng = np.random.default_rng(16023)
    harmony = [
        (38, [53, 57, 60, 64]), (43, [53, 57, 59, 64]),
        (36, [52, 55, 59, 62]), (45, [55, 61, 64, 70]),
        (38, [53, 57, 60, 64]), (46, [53, 57, 60, 65]),
        (40, [55, 58, 62, 65]), (45, [55, 61, 64, 70]),
    ]
    # Call, space, answer: pitches follow the chords, with one chromatic pickup.
    hook = [
        [(0,69),(.5,72),(1,74),(2.5,72)],
        [(1,71),(1.5,69),(3,67)],
        [(0,67),(.5,71),(1,74),(2.5,76)],
        [(1,73),(2.5,70),(3,69)],
        [(0,69),(.5,72),(1,74),(2.5,77)],
        [(1,77),(1.5,76),(3,72)],
        [(0,74),(.5,77),(1,76),(2.5,74)],
        [(1,73),(2,70),(3,69),(3.5,68)],
    ]

    def at(bar, off):
        # Swing only the offbeat eighths; keep the kick and backbeat steady.
        whole = int(off)
        return (bar * 4 + whole + (swing if off - whole == .5 else off - whole)) * beat

    def add(signal, start, pan=0):
        idx = (round(start * RATE) + np.arange(len(signal))) % len(music)
        music[idx, 0] += signal * np.sqrt((1 - pan) / 2)
        music[idx, 1] += signal * np.sqrt((1 + pan) / 2)

    def note(midi, start, duration, gain, pan=0, kind='piano'):
        t = np.arange(round(duration * RATE)) / RATE
        f = 440 * 2 ** ((midi - 69) / 12)
        phase = 2 * np.pi * f * t
        if kind == 'bass':
            tone = np.sin(phase) + .32*np.sin(2*phase)*np.exp(-5*t) + .12*np.sin(3*phase)*np.exp(-9*t)
        elif kind == 'vibe':
            tone = np.sin(phase + .5*np.sin(phase*2.003)*np.exp(-7*t))
            tone *= .92 + .08*np.cos(2*np.pi*4.4*t)
        else:
            tone = np.sin(phase) + .3*np.sin(2*phase)*np.exp(-4*t) + .08*np.sin(3*phase)*np.exp(-7*t)
        env = (1-np.exp(-t*130))*np.exp(-t/(duration*.38))*np.clip((duration-t)/.06,0,1)
        add(tone*env*gain,start,pan)

    def drum(kind, start, gain):
        duration = {'kick':.25,'rim':.08,'brush':.15,'hat':.055}[kind]
        t = np.arange(round(duration*RATE))/RATE
        noise = rng.normal(0,1,len(t))
        if kind == 'kick':
            tone = np.sin(2*np.pi*(52*t+2.2*(1-np.exp(-t*24))))*np.exp(-t*22)
        elif kind == 'rim':
            tone = (.7*np.sin(2*np.pi*930*t)+.3*np.sin(2*np.pi*1370*t))*np.exp(-t*100)
        elif kind == 'brush':
            tone = np.convolve(noise,np.ones(6)/6,'same')*np.exp(-t*32)
        else:
            tone = (noise-np.convolve(noise,np.ones(7)/7,'same'))*np.exp(-t*90)
        tone *= (1-np.exp(-t*1000))*np.clip((duration-t)/.012,0,1)
        add(tone*gain,start,.18 if kind=='hat' else -.12 if kind=='rim' else 0)

    for bar in range(bars):
        phrase, section = bar%8, bar//8
        root, chord = harmony[phrase]
        next_root = harmony[(phrase+1)%8][0]
        sparse = section==1 and phrase<4
        for off,pitch,gain in [(0,root,.20),(1.5,root+12,.105),(2.5,root+7,.14),(3.5,next_root-1,.075)]:
            note(pitch,at(bar,off),beat*.78,gain,kind='bass')
        for off,gain in [(.5,.055),(2,.045),(3.5,.028)]:
            for j,pitch in enumerate(chord):
                note(pitch,at(bar,off)+j*.011,beat*.9,gain,(j-1.5)*.15)
        for off,pitch in hook[phrase]:
            if sparse and off<2:continue
            note(pitch,at(bar,off),beat*1.35,.071,-.22,'vibe')
        # Piano answers in the middle eight, then a restrained returning hook.
        if section==1 and phrase>=4:
            for off,pitch in [(2,chord[1]+12),(2.5,chord[2]+12),(3,chord[3]+12)]:
                note(pitch,at(bar,off),beat*.6,.036,.28)
        for off,gain in [(0,.16),(2.5,.11)]:drum('kick',at(bar,off),gain)
        for off in [1,3]:
            drum('rim',at(bar,off),.055)
            drum('brush',at(bar,off)+.008,.072)
        for off in [0,.5,1,1.5,2,2.5,3,3.5]:
            drum('hat',at(bar,off),.010 if off%1 else .017)
        if phrase==7 and section!=1:
            drum('rim',at(bar,3.5),.027)
    # Short room reflection keeps percussion crisp; circular tails join the loop.
    music += .12*np.roll(music,round(.14*RATE),axis=0)[:,::-1] + .055*np.roll(music,round(.29*RATE),axis=0)
    music *= reference_rms / np.sqrt(np.mean(music**2))
    export('folamour_menu',music,True)
    return dict(file='folamour_menu.ogg',title='Le swing des petites anomalies',bpm=bpm,bars=bars,seconds=len(music)/RATE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--menu-only', action='store_true', help='Regenerate only the menu theme')
    args = parser.parse_args()
    decoded = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(DEST / 'folamour_lounge.ogg'), '-f', 'f32le', '-ac', '2', '-ar', str(RATE), '-'])
    reference_rms = float(np.sqrt(np.mean(np.frombuffer(decoded, '<f4') ** 2)))
    tracks = [] if args.menu_only else [compose_theme(*theme, reference_rms) for theme in THEMES]
    tracks.append(compose_menu(reference_rms))
    print(json.dumps(tracks, ensure_ascii=False, indent=2))
