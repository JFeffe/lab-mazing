extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func check(ok,message):
	if not ok:failed=true;push_error(message)
func event(id):
	for e in game.events:
		if e.id==id:return e
	return {}
func press(token):
	for child in game.modal_box.get_children():
		if child is Button and child.text==token:
			child.pressed.emit()
			await process_frame
			return
	check(false,"Missing button: "+token)
func state():return JSON.stringify([game.done,game.inventory,game.puzzle_states,game.dial_settings,game.errors])
func labels(node):
	var result=""
	if node is Label:result+=node.text+"\n"
	for child in node.get_children():result+=labels(child)
	return result
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	for level in range(1,6):
		game.start_game(false,level)
		for language in ["fr","en"]:
			game.localization.choose(language,false)
			for e in game.events:
				if e.has("answer") or e.has("puzzle_type"):
					check(game.guidance_data.hints.has(e.id),"Missing authored help: "+e.id)
				if not game.Guidance.is_challenge(e):continue
				var steps=game.Guidance.hint_steps(game,e)
				check(steps.size()==3 and not steps[2].is_empty(),"Missing hint tier: "+e.id)
				game.hints.erase(e.id)
				game.show_puzzle(e)
				var before=state()
				await press(game.loc("Indice facultatif"))
				check(not game.hints.has(e.id),"Opening help counts as revealing it")
				check(not labels(game.modal_box).contains(steps[2]),"Solution exposed early")
				for token in ["Afficher une piste","Afficher la méthode","Révéler la solution"]:
					await press(game.loc(token))
				check(int(game.hints[e.id])==3 and labels(game.modal_box).contains(steps[2]),"Three-tier reveal failed: "+e.id+" "+language+" / "+labels(game.modal_box)+" / expected "+steps[2])
				check(state()==before,"Hint mutated puzzle or inventory")
				game.show_hint(e)
				check(int(game.hints[e.id])==3,"Rereading counts twice")
			# All objective prerequisites are real event IDs, with bilingual text.
			for stage in game.guidance_data.stages[str(level)]:
				for id in stage[0]:check(not event(id).is_empty(),"Invalid objective event: "+id)
				check(game.guidance_data.objectives[stage[1]].size()==2,"Objective translation missing")
		game.test_mode=false
		game.save_game()
		game.test_mode=true
		var saved_hints=game.hints.duplicate()
		game.start_game(true)
		check(JSON.stringify(game.hints)==JSON.stringify(saved_hints),"Revealed hints lost on resume")
	# Reading hints in the journal must not enable remote operation of machinery.
	game.show_hint(event("f_dosing"),null,false)
	for child in game.modal_box.get_children():
		if child is Button:check(child.text!=game.loc("Retour au mécanisme"),"Journal permits remote mechanism access")
	game.start_game(false,5)
	game.localization.choose("en",false)
	check(game.Guidance.objective(game).contains("West wing") and game.Guidance.objective(game).contains("East wing"),"Parallel objectives missing")
	game.done.f_tower=true
	check(not game.Guidance.objective(game).contains("East wing"),"Completed wing remains an objective")
	game.done.f_dosing=true
	check(game.Guidance.objective(game).contains("station 103"),"Assembly objective missing")
	game.done.f_assembly=true
	check(game.Guidance.objective(game).contains("north wing"),"North objective missing")
	game.done.f_rotors=true
	check(game.Guidance.objective(game).contains("405"),"Final objective missing")
	game.level_stats={"1":{"time":60,"secrets":2,"hints":1,"errors":0},"2":{"time":90,"secrets":3,"hints":2,"errors":0,"puzzles":7,"shortcuts":4}}
	game.elapsed=120
	game.show_win()
	var summary=game.Guidance.summary(game)
	check(summary.time==270 and summary.levels==3 and summary.tracked==2,"Campaign totals / legacy coverage wrong")
	check(labels(game.modal_box).contains("older saves") and labels(game.modal_box).contains("Partial summary"),"Legacy and partial notes missing")
	var original=JSON.stringify(game.level_stats)
	game.show_win()
	check(original==JSON.stringify(game.level_stats),"Reopening summary double counts")
	# Preferences survive a fresh audio object and cannot be replaced by a stale game save.
	game.soundscape.levels.music=.13
	game.soundscape.levels.effects=.41
	game.soundscape.preference_muted=true
	game.soundscape.persist()
	var fresh=load("res://LabAudio.gd").new()
	fresh.load_settings()
	check(is_equal_approx(fresh.levels.music,.13) and fresh.preference_muted,"Audio preferences not persisted")
	fresh.free()
	game.start_game(true)
	check(game.muted,"Old checkpoint overrode current mute preference")
	game.test_mode=false
	game.soundscape.update(game,.1)
	check((not game.soundscape.music.playing or game.soundscape.music.stream_paused) and game.audio.volume_db<=-80,"Mute fails on active players")
	game.muted=false
	game.soundscape.focused=false
	var before_time=game.elapsed
	game.close_modal()
	game._physics_process(1)
	check(game.elapsed==before_time,"Background app counts play time")
	game.soundscape.update(game,.1)
	check(not game.soundscape.music.playing or game.soundscape.music.stream_paused,"Background app keeps music running")
	game.soundscape.focused=true
	game.soundscape.levels.music=0
	game.soundscape.update(game,.1)
	check(not game.soundscape.music.playing or game.soundscape.music.stream_paused,"Zero music volume still plays")
	check(game.soundscape.music.stream.get_length()>40 and game.soundscape.music.stream.loop,"Music loop missing")
	game.test_mode=true
	# New dialogs must fit both mobile orientations and both languages.
	for dimensions in [Vector2i(390,844),Vector2i(844,390)]:
		root.size=dimensions
		await process_frame
		await process_frame
		for language in ["fr","en"]:
			game.localization.choose(language,false)
			for dialog in ["objective","audio","hint","summary"]:
				if dialog=="objective":game.show_objective()
				elif dialog=="audio":game.show_audio()
				elif dialog=="hint":game.show_hint(event("f_dosing"))
				else:game.show_win()
				await process_frame
				await process_frame
				check(game.modal_box.size.x<=game.get_viewport().get_visible_rect().size.x,"Mobile overflow: "+dialog)
	print("CHAPTER POLISH: ","FAIL" if failed else "PASS"," — hints, objectives, saves, legacy summary, audio controls, FR/EN mobile")
	quit(1 if failed else 0)
