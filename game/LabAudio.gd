extends Node
const SETTINGS="user://audio.cfg"
var levels={"master":0.8,"music":0.22,"effects":0.55,"ambience":0.4}
var music:AudioStreamPlayer
var step:AudioStreamPlayer
var mechanical:AudioStreamPlayer
var fanfare:AudioStreamPlayer
var preference_muted=false
var focused=true
var step_distance=0.0
var current_gain=0.0

func _ready():
	load_settings()
	music=make_player("folamour_lounge.ogg")
	music.stream.loop=true
	step=make_player("footstep.wav")
	mechanical=make_player("door.wav")
	fanfare=make_player("chapter_complete.wav")

func make_player(path):
	var p=AudioStreamPlayer.new()
	p.stream=load("res://assets/"+path)
	add_child(p)
	return p

func load_settings():
	var config=ConfigFile.new()
	if config.load(SETTINGS)==OK:
		preference_muted=bool(config.get_value("volume","muted",false))
		for key in levels:levels[key]=clampf(float(config.get_value("volume",key,levels[key])),0,1)

func persist():
	var config=ConfigFile.new()
	config.set_value("volume","muted",preference_muted)
	for key in levels:config.set_value("volume",key,levels[key])
	config.save(SETTINGS)

func gain(game,channel):
	return 0.0 if game.muted or game.test_mode or not focused else levels.master*levels[channel]

func update(game,delta):
	var active=game.playing and focused and not game.test_mode
	var target=gain(game,"music")*(0.45 if game.modal_open else 1.0) if active else 0.0
	current_gain=move_toward(current_gain,target,delta*.16)
	# Muting and zero volume take effect immediately, including ongoing sounds.
	if gain(game,"music")==0:current_gain=0
	music.volume_db=linear_to_db(maxf(current_gain,0.00001))
	music.stream_paused=not active or gain(game,"music")==0
	if active and gain(game,"music")>0 and not music.playing:music.play()
	for p in [step,mechanical,fanfare,game.audio]:
		p.volume_db=linear_to_db(maxf(gain(game,"effects"),0.00001))
		p.stream_paused=gain(game,"effects")<=0

func movement(game,distance):
	step_distance+=distance
	if step_distance>=1.35:
		step_distance=fmod(step_distance,1.35)
		if gain(game,"effects")>0:
			step.pitch_scale=game.rng.randf_range(.94,1.06)
			step.play()

func effect(game,kind):
	if gain(game,"effects")<=0:return
	if kind=="chapter_complete":fanfare.play()
	else:
		mechanical.stream=load("res://assets/"+kind+".wav")
		mechanical.play()
