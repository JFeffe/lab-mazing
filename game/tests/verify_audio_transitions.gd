extends SceneTree
class Probe:
 extends RefCounted
 var writes=0
 var stream_paused=false:
  set(value):
   writes+=1
   stream_paused=value
func _initialize():
 var audio=load("res://LabAudio.gd")
 var player=Probe.new()
 for i in range(36000):audio.set_paused(player,false)
 assert(player.writes==0,"Steady playback repeatedly resumes Web samples")
 for i in range(36000):audio.set_paused(player,true)
 assert(player.writes==1,"Steady pause repeatedly stops Web samples")
 for i in range(36000):audio.set_paused(player,false)
 assert(player.writes==2,"Resume must occur exactly once")
 print("PASS 108000 audio updates: exactly two backend state changes")
 quit()
