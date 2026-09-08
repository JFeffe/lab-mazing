extends SceneTree
var game
var failed=false
func _initialize(): call_deferred("run")
func check(ok,message):
	if not ok: failed=true;push_error(message)
func event(id):
	for e in game.events:
		if e.id==id:return e
	return {}
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.localization.choose("en",false)
	game.start_game(false,9)
	game.elapsed=123
	game.show_win()
	for child in game.modal_box.get_children():
		if child is Button and child.text=="Continue to the archive department":child.pressed.emit();await process_frame;break
	check(game.level==10 and game.level_stats.has("9") and game.inventory.is_empty(),"Mission 4 to mission 5 transition")
	check(is_instance_valid(game.folamour),"Folamour has a physical model")
	await press("Accept the assignment")
	check(game.done.has("a_met"),"First archive recorded")
	game.close_modal()
	game.playing=false
	for e in game.events:
		for field in ["title","text","question","success","action"]:
			if e.has(field):check(game.localization.english.has(e[field]),"Translation missing: "+e.id+"."+field)
	# Hints are optional, bilingual and cannot mutate a archive mechanism.
	for language in ["fr","en"]:
		game.localization.choose(language,false)
		for e in game.events:
			if not e.has("puzzle_type"):continue
			game.hints.erase(e.id)
			game.show_puzzle(e)
			var before=JSON.stringify([game.done,game.inventory,game.puzzle_states,game.errors])
			await press(game.loc("Indice facultatif"))
			check(not game.hints.has(e.id),"Opening hint reveals an answer")
			for token in ["Afficher une piste","Afficher la méthode","Révéler la solution"]:await press(game.loc(token))
			check(game.hints[e.id]==3,"Missing archive hint tiers")
			check(before==JSON.stringify([game.done,game.inventory,game.puzzle_states,game.errors]),"Hint mutates archive state")
	var controls_v=game.PuzzleControls.Archives
	var solutions=0
	for n in range(27):
		var v=[n%3,int(n/3)%3,int(n/9)%3]
		if controls_v.solved(event("a_stacks"),v):solutions+=1
	check(solutions==1,"One safe stack alignment")
	var v=[1,0,1,0,0]
	check(not controls_v.solved(event("a_twin"),v),"Untested copy accepted")
	controls_v.move(event("a_twin"),v,4)
	check(controls_v.solved(event("a_twin"),v),"Matching tested copy rejected")
	controls_v.move(event("a_twin"),v,0)
	check(v[4]==0 and not controls_v.solved(event("a_twin"),v),"Changing copy must invalidate test")
	game.interact(event("a_seal"))
	check(not game.done.has("a_seal"),"Seal available before alignment")
	game.close_modal()
	# Closed copy-room gate cannot be crossed from either direction.
	for sign_v in [-1,1]:
		game.player.position=Vector3(29*game.TILE,.1,(20-sign_v)*game.TILE)
		for frame in range(65):
			await physics_frame
			game.player.velocity=Vector3(0,-2,sign_v*game.MOVE_SPEED)
			game.player.move_and_slide()
		check((game.player.position.z-20*game.TILE)*sign_v<0,"Copy room gate bypass")
	# Each blocked shelf cell is excluded from click/touch navigation and has a collider.
	for row in range(3):
		for x in range(13,22):
			var shelf=game.machine_parts.archive_storage.get_node("Shelf%d_%d"%[row,x])
			check((shelf.get_meta("body").collision_layer==1)==(x!=14),"Initial shelf collider")
	game.player.position=Vector3(14*game.TILE,.1,5*game.TILE)
	game.show_puzzle(event("a_stacks"))
	game.PuzzleControls.move(game,event("a_stacks"),0)
	check(game.PuzzleControls.state(game,event("a_stacks"))==[0,0,0],"Shelf safety lock failed")
	game.show_puzzle(event("a_final"))
	for child in game.modal_box.get_children():
		if child is Button:check(child.text!="Open the MIRROR file","Exit available early")
	game.close_modal()
	game.player.position=Vector3(17*game.TILE,0.1,23*game.TILE)
	var route=JSON.parse_string(FileAccess.get_file_as_string("res://tests/route_level10.json"))
	for step in route:
		var e=event(step.id)
		for cell in step.route:
			var target=Vector3(cell[0]*game.TILE,0,cell[1]*game.TILE)
			var frames=0
			while Vector2(game.player.position.x-target.x,game.player.position.z-target.z).length()>0.08:
				await physics_frame
				var offset=target-game.player.position
				offset.y=0
				game.player.velocity=offset.normalized()*min(game.MOVE_SPEED,offset.length()*30)
				game.player.velocity.y=-2
				game.player.move_and_slide()
				game.record_walk()
				frames+=1
				if frames>120:push_error("Blocked route: "+str(cell)+" to "+e.id);quit(1);return
		await physics_frame
		game.find_nearest()
		check(game.nearest.get("id","")==e.id,"Unreachable interaction: "+e.id)
		if e.kind in ["clue","pickup"]:
			game.interact(e)
		else:
			game.show_puzzle(e)
			if e.has("requires"):game.install_items(e)
			if e.has("puzzle_type"):
				var controls=game.PuzzleControls
				controls.submit(game,e)
				check(not game.done.has(e.id),"Wrong state accepted: "+e.id)
				# Change one real control, save, and resume the partially solved puzzle.
				var first="Control I" if e.puzzle_type=="stacks" else "Selected report:" if e.puzzle_type=="reports" else "Lamp:"
				await press(first)
				var partial=controls.state(game,e).duplicate()
				game.test_mode=false
				game.save_game()
				game.test_mode=true
				game.start_game(true)
				game.close_modal()
				game.playing=false
				check(game.level==10 and controls.state(game,e)==partial,"Partial puzzle resume: "+e.id)
				game.show_puzzle(e)
				await press("Reset this test")
				check(controls.state(game,e)==controls.initial(e),"Reset failed")
				if e.has("requires"):
					check(game.done.has("installed_"+e.id),"Reset loses installed objects")
					for id in e.requires:check(game.inventory[id]==0,"Consumed object reappears")
				var actions={"stacks":["Control I:","Control I:","Control II:"],"reports":["Selected report:","Log:","Clock:","Object:","Object:"],"twin":["Lamp:","Coil:","Projector:","Projector:","Ventilation:","Test the copy"]}
				for token in actions[e.puzzle_type]:await press(token)
				await press("Validate the test")
			elif e.kind=="exit":
				check(game.won,"Installing seal should open the final file")
		check(game.done.has(e.id),"Action failed: "+e.id)
		game.close_modal()
		print("LEVEL10 ROUTE ",e.id," PASS")
	check(game.won and game.level_stats["10"].secrets==3,"Level 10 completion and secrets")
	game.test_mode=false
	game.save_game()
	game.test_mode=true
	game.start_game(true)
	await process_frame
	check(game.won and game.level==10 and game.level_stats.has("9"),"Completed level resume")
	var all_text=""
	for child in game.modal_box.get_children():
		if child is Label:all_text+=child.text
	check("MIRROR" in all_text and "critical thinking" in all_text,"MIRROR revelation")
	check(game.machine_parts.archive_hatch.rotation.y>0,"Prototype door reveal")
	game.show_title()
	await press("Choose a chapter")
	check(game.modal_open and not game.playing,"Chapter menu")
	var available=false
	for child in game.modal_box.get_children():
		if child is Button and child.text==game.level_name(6):available=not child.disabled
	check(available,"Chapter 2 unavailable")
	# A corrupt primary must recover the previous valid checkpoint.
	var f=FileAccess.open(game.SAVE,FileAccess.WRITE)
	f.store_string("{broken");f.close()
	check(game.has_save() and game.read_save().level==10,"Backup recovery")
	print("LEVEL10 PHYSICS + PROGRESSION + SAVES: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)

func press(token):
	var candidates=[]
	collect_buttons(game.modal_box,candidates)
	for b in candidates:
		if b.text.begins_with(token) and not b.disabled:
			b.pressed.emit()
			await process_frame
			return
	check(false,"Button unavailable: "+token)
func collect_buttons(node,result):
	for child in node.get_children():
		if child is Button:result.append(child)
		collect_buttons(child,result)
