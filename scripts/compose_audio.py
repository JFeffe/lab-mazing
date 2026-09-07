"""Original, deterministic music and sound effects for Folamour (no samples).

Requires numpy and ffmpeg. The circular arrangement/reverb makes the Ogg loop
continuous. Regeneration is optional; the exported assets are committed.
"""
from pathlib import Path
import subprocess
import tempfile
import wave
import numpy as np

DEST = Path(__file__).resolve().parents[1] / 'game/assets'
RATE = 22050

def export(name, signal, ogg=False):
    signal = np.asarray(signal)
    peak = np.max(np.abs(signal))
    signal = signal * (0.65 / max(peak, 0.65))
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / 'audio.wav'
        with wave.open(str(path), 'wb') as out:
            out.setnchannels(2 if signal.ndim == 2 else 1)
            out.setsampwidth(2)
            out.setframerate(RATE)
            out.writeframes((signal * 32767).astype('<i2').tobytes())
        target = DEST / (name + ('.ogg' if ogg else '.wav'))
        if ogg:
            subprocess.run(['ffmpeg','-loglevel','error','-y','-i',str(path),'-c:a','libvorbis','-q:a','3',str(target)],check=True)
        else:
            target.write_bytes(path.read_bytes())

def compose():
    # 16 bars at 80 bpm: electric piano, rounded bass, brushed percussion,
    # with suspended harmony and sparse, slightly detuned bell replies.
    seconds, beat = 48, .75
    music = np.zeros((int(seconds * RATE), 2))
    rng = np.random.default_rng(16)
    def note(midi, start, duration, gain, pan=0, bell=False):
        t = np.arange(int(duration*RATE))/RATE
        f = 440 * 2**((midi-69)/12)
        if bell:
            tone = np.sin(2*np.pi*f*t + 1.1*np.sin(2*np.pi*f*2.003*t)*np.exp(-3*t))
        else:
            tone = np.sin(2*np.pi*f*t) + .23*np.sin(2*np.pi*f*2*t)*np.exp(-3*t)
        envelope = (1-np.exp(-t*55))*np.exp(-t/(duration*.32))
        envelope *= np.minimum(1,(duration-t)/.12)
        wave_v = gain*tone*envelope
        idx=(int(start*RATE)+np.arange(len(t)))%len(music)
        music[idx,0] += wave_v*np.sqrt((1-pan)/2)
        music[idx,1] += wave_v*np.sqrt((1+pan)/2)
    chords = [(38,[53,57,60,64]), (43,[53,57,59,64]),
              (36,[52,55,59,62]), (45,[55,61,65,71]),
              (38,[53,57,60,64]), (41,[57,60,64,67]),
              (40,[55,59,62,66]), (45,[55,61,65,70])]
    melody = [76,74,71,73,77,76,74,70,76,79,78,77,76,74,73,69]
    for bar in range(16):
        base, chord = chords[bar%8]
        start = bar*4*beat
        note(base,start,2.1,.17,-.1)
        note(base+12,start+2.5*beat,1.0,.08,-.1)
        for j, pitch in enumerate(chord):
            note(pitch,start+.035*j,2.8,.085,(j-1.5)*.15)
            note(pitch,start+2.5*beat+.02*j,1.3,.035,(j-1.5)*.15)
        note(melody[bar],start+1.5*beat,3,.04,.4 if bar%2 else -.4,True)
        # Soft filtered brush ticks, never a prominent drum beat.
        for off in [1,3]:
            t=np.arange(int(.13*RATE))/RATE
            noise=np.convolve(rng.normal(0,1,len(t)),np.ones(12)/12,'same')
            brush=noise*np.exp(-t*40)*.022
            idx=int((start+off*beat)*RATE)+np.arange(len(t))
            music[idx,:]+=brush[:,None]
    music += .19*np.roll(music,int(.31*RATE),axis=0)[:,::-1] + .10*np.roll(music,int(.63*RATE),axis=0)
    export('folamour_lounge',music,True)
    t=np.arange(int(.12*RATE))/RATE
    noise=rng.normal(0,1,len(t))
    export('footstep',(.13*np.sin(2*np.pi*95*t)+.025*noise)*np.exp(-t*44)*(1-np.exp(-t*500)))
    t=np.arange(int(.65*RATE))/RATE
    env=np.sin(np.pi*t/.65)**2
    export('door',env*(.10*np.sin(2*np.pi*(190*t-70*t*t))+.012*rng.normal(0,1,len(t))))
    t=np.arange(int(.9*RATE))/RATE
    export('machine',.10*np.sin(2*np.pi*(70*t+100*t*t))*np.sin(np.pi*t/.9)**2)
    t=np.arange(int(2.4*RATE))/RATE
    victory=np.zeros(len(t))
    for i,midi in enumerate([62,66,69,73,74]):
        u=np.maximum(0,t-i*.23)
        victory+=(t>=i*.23)*.10*np.sin(2*np.pi*440*2**((midi-69)/12)*u)*(1-np.exp(-u*80))*np.exp(-u*2.5)
    victory*=np.minimum(1,(2.4-t)/.1)
    export('chapter_complete',victory)

if __name__=='__main__': compose()
