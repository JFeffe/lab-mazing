"""Original quiet mechanical layers; no external samples, peaks capped at 0.2."""
from pathlib import Path
import math, struct, wave
dest=Path(__file__).resolve().parents[1]/'game/assets'
rate=16000;duration=8
for stage in range(3):
 samples=[]
 for i in range(rate*duration):
  t=i/rate
  # Integer periods over eight seconds make a seamless loop. The soft beacon
  # grows denser as backup procedures take over, never changing game timing.
  hum=.055*math.sin(2*math.pi*48*t)+.025*math.sin(2*math.pi*72*t)
  pulse=(.5-.5*math.cos(2*math.pi*(stage+1)*.5*t))**6
  signal=.05*pulse*math.sin(2*math.pi*(240+stage*30)*t)
  tremor=.025*math.sin(2*math.pi*96*t)*(.6+.4*math.sin(2*math.pi*.25*t))
  samples.append(struct.pack('<h',int(32767*(hum+signal+tremor))))
 with wave.open(str(dest/f'horizon{stage}.wav'),'wb') as out:
  out.setnchannels(1);out.setsampwidth(2);out.setframerate(rate);out.writeframes(b''.join(samples))
 print('horizon',stage,'PCM mono, 8 seconds, original synthesis')
