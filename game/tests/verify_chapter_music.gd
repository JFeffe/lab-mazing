extends SceneTree
var failed=false
func check(ok,message):
	if not ok:failed=true;push_error(message)
func settle(sound,game):
	for i in range(120):sound.update(game,1.0/60)
func _initialize():call_deferred("run")
func run():
	var game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.set_process(false)
	game.set_physics_process(false)
	game.test_mode=false
	game.muted=false
	var sound=game.soundscape
	sound.focused=true
	sound.levels={"master":0.8,"music":0.22,"effects":0.55,"ambience":0.4}
	game.playing=false
	settle(sound,game)
	check(sound.current_track==0 and sound.music.playing and sound.current_gain>0.17,"Menu must play at normal music gain")
	for level in range(1,26):
		game.playing=true
		game.level=level
		game.modal_open=false
		settle(sound,game)
		check(sound.current_track==int((level-1)/5)+1,"Wrong chapter track at level "+str(level))
		check(sound.music.stream.loop and sound.music.stream.get_length()>40,"Missing loop")
		var stream=sound.music.stream
		settle(sound,game)
		check(sound.music.stream==stream,"Steady playback replaces stream")
	check(sound.current_gain==0,"Final conversation lost its silence")
	game.playing=false
	settle(sound,game)
	check(sound.current_track==0 and sound.current_gain>0.17,"Returning from finale leaves menu silent")
	game.playing=true
	game.level=6
	settle(sound,game)
	var stream=sound.music.stream
	game.level=7
	game.modal_open=true
	settle(sound,game)
	check(sound.music.stream==stream and is_equal_approx(sound.current_gain,.8*.22*.45),"Reading must soften the same track")
	game.muted=true
	sound.update(game,.016)
	check(sound.current_gain==0 and sound.music.stream_paused,"Mute must act immediately")
	game.level=16
	settle(sound,game)
	check(sound.current_track==4 and (not sound.music.playing or sound.music.stream_paused),"Muted chapter change plays audio")
	game.muted=false
	settle(sound,game)
	check(sound.music.playing and not sound.music.stream_paused,"Unmute fails")
	sound.focused=false
	sound.update(game,.016)
	check(sound.music.stream_paused,"Unfocused music plays")
	sound.focused=true
	settle(sound,game)
	check(not sound.music.stream_paused,"Refocus fails")
	sound.levels.music=0
	sound.update(game,.016)
	check(sound.current_gain==0 and sound.music.stream_paused,"Zero volume plays")
	game.test_mode=true
	sound.music.stop()
	game.queue_free()
	await process_frame
	await process_frame
	print("CHAPTER / MENU MUSIC: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
