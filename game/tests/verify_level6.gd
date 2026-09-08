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
	game.start_game(false,5)
	game.elapsed=123
	game.show_win()
	for child in game.modal_box.get_children():
		if child is Button and child.text=="Accept the internship — Chapter 2":child.pressed.emit();await process_frame;break
	check(game.level==6 and game.level_stats.has("5") and game.inventory.is_empty(),"Chapter 1 to chapter 2 transition")
	check(is_instance_valid(game.folamour),"Folamour has a physical model")
	await press("Start my shift")
	check(game.done.has("g_met"),"First meeting recorded")
	game.close_modal()
	game.playing=false
	for e in game.events:
		for field in ["title","text","question","success","action"]:
			if e.has(field):check(game.localization.english.has(e[field]),"Translation missing: "+e.id+"."+field)
	# Hints are optional, bilingual and cannot mutate a greenhouse mechanism.
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
			check(game.hints[e.id]==3,"Missing greenhouse hint tiers")
			check(before==JSON.stringify([game.done,game.inventory,game.puzzle_states,game.errors]),"Hint mutates greenhouse state")
	# Verify actual engine connectivity, rather than only a prescribed button sequence.
	var pipe_solutions=0
	for a in range(4):
		for b in range(4):
			for c in range(4):
				for d in range(4):
					if game.PuzzleControls.Greenhouse.flowing([a,b,c,d]).size()==4:pipe_solutions+=1
	check(pipe_solutions==1,"Pipe circuit accepts a leak or an extra solution")
	for id in ["g_bridge"]:
		var e=event(id)
		for sign_v in [-1,1]:
			for lane in [-0.9,0,0.9]:
				game.player.position=Vector3((e.cell[0]-sign_v)*game.TILE,0.1,e.cell[1]*game.TILE+lane)
				for frame in range(60):
					await physics_frame
					game.player.velocity=Vector3(sign_v*game.MOVE_SPEED,-2,0)
					game.player.move_and_slide()
				check((game.player.position.x-e.cell[0]*game.TILE)*sign_v<0,"Gate bypass: "+id)
	game.show_puzzle(event("g_coffee"))
	for child in game.modal_box.get_children():
		if child is Button:check(child.text!="Serve the coffee","Exit available early")
	game.close_modal()
	game.player.position=Vector3(17*game.TILE,0.1,23*game.TILE)
	var route=JSON.parse_string(FileAccess.get_file_as_string("res://tests/route_level6.json"))
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
				var first="A\n" if e.puzzle_type=="pipes" else "Light:" if e.puzzle_type=="growth" else "Bean :"
				await press(first)
				var partial=controls.state(game,e).duplicate()
				game.test_mode=false
				game.save_game()
				game.test_mode=true
				game.start_game(true)
				game.close_modal()
				game.playing=false
				check(game.level==6 and controls.state(game,e)==partial,"Partial puzzle resume: "+e.id)
				game.show_puzzle(e)
				await press("Reset this test")
				check(controls.state(game,e)==controls.initial(e),"Reset failed")
				if e.has("requires"):
					check(game.done.has("installed_"+e.id),"Reset loses installed objects")
					for id in e.requires:check(game.inventory[id]==0,"Consumed object reappears")
				var actions={"pipes":["A\n","A\n","B\n","D\n","D\n","D\n"],"growth":["Light:","Watering:","Watering:","Trellis:"],"blend":["Bean :","Petal :","Moss :"]}
				for token in actions[e.puzzle_type]:await press(token)
				await press("Validate the test")
			elif e.kind=="exit":
				for child in game.modal_box.get_children():
					if child is Button and child.text=="Serve the coffee":child.pressed.emit();await process_frame;break
		check(game.done.has(e.id),"Action failed: "+e.id)
		game.close_modal()
		print("LEVEL6 ROUTE ",e.id," PASS")
	check(game.won and game.level_stats["6"].secrets==3,"Level 6 completion and secrets")
	game.test_mode=false
	game.save_game()
	game.test_mode=true
	game.start_game(true)
	await process_frame
	check(game.won and game.level==6 and game.level_stats.has("5"),"Completed level resume")
	var all_text=""
	for child in game.modal_box.get_children():
		if child is Label:all_text+=child.text
	check("Coffee is served" in all_text and "photocopies" in all_text and "second internship assignment is available" in all_text,"First mission ending and coming next")
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
	check(game.has_save() and game.read_save().level==6,"Backup recovery")
	print("LEVEL6 PHYSICS + PROGRESSION + SAVES: ","FAIL" if failed else "PASS")
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
