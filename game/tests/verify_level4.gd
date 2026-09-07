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
	game.start_game(false,3)
	game.elapsed=123
	game.show_win()
	for child in game.modal_box.get_children():
		if child is Button and child.text=="Continue to level 4":child.pressed.emit();await process_frame;break
	check(game.level==4 and game.level_stats.has("3") and game.inventory.is_empty(),"Level 3 to 4 transition")
	game.close_modal()
	game.playing=false
	for e in game.events:
		for field in ["title","text","question","success","action"]:
			if e.has(field):check(game.localization.english.has(e[field]),"Translation missing: "+e.id+"."+field)
	for id in ["test_gate","circuit_gate"]:
		var e=event(id)
		for sign_v in [-1,1]:
			for lane in [-0.9,0,0.9]:
				game.player.position=Vector3(e.cell[0]*game.TILE+lane,0.1,(e.cell[1]-sign_v)*game.TILE)
				for frame in range(60):
					await physics_frame
					game.player.velocity=Vector3(0,-2,sign_v*7)
					game.player.move_and_slide()
				check((game.player.position.z-e.cell[1]*game.TILE)*sign_v<0,"Gate bypass: "+id)
	game.show_puzzle(event("test_exit"))
	for child in game.modal_box.get_children():
		if child is Button:check(child.text!="Complete the tests","Exit available early")
	game.close_modal()
	game.player.position=Vector3(game.TILE,0.1,game.TILE)
	var route=JSON.parse_string(FileAccess.get_file_as_string("res://tests/route_level4.json"))
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
				var first="1 kg" if e.puzzle_type=="balance" else "MOON" if e.puzzle_type=="sequence" else "Lever I :"
				await press(first)
				var partial=controls.state(game,e).duplicate()
				game.test_mode=false
				game.save_game()
				game.test_mode=true
				game.start_game(true)
				game.close_modal()
				game.playing=false
				check(game.level==4 and controls.state(game,e)==partial,"Partial puzzle resume: "+e.id)
				game.show_puzzle(e)
				await press("Reset this test")
				check(controls.state(game,e)==controls.initial(e),"Reset failed")
				if e.has("requires"):
					check(game.done.has("installed_"+e.id),"Reset loses installed objects")
					for id in e.requires:check(game.inventory[id]==0,"Consumed object reappears")
				match e.puzzle_type:
					"balance":
						for token in ["1 kg","2 kg","2 kg","3 kg","3 kg","5 kg"]:await press(token)
					"sequence":
						await press("SUN")
						await press("Remove the last symbol")
						for token in ["MOON","STAR","SUN","PLANET","COMET"]:await press(token)
					"circuit":
						await press("Lever II :")
						await press("Lever II :")
						check(controls.state(game,e)==controls.initial(e),"Double toggle must cancel")
						for token in ["Lever I :","Lever III :","Lever IV :"]:await press(token)
				await press("Validate the test")
			elif e.kind=="exit":
				for child in game.modal_box.get_children():
					if child is Button and child.text=="Complete the tests":child.pressed.emit();await process_frame;break
		check(game.done.has(e.id),"Action failed: "+e.id)
		game.close_modal()
		print("LEVEL4 ROUTE ",e.id," PASS")
	check(game.won and game.level_stats["4"].secrets==3,"Level 4 completion and secrets")
	game.test_mode=false
	game.save_game()
	game.test_mode=true
	game.start_game(true)
	await process_frame
	check(game.won and game.level==4 and game.level_stats.has("3"),"Completed level resume")
	# A corrupt primary must recover the previous valid checkpoint.
	var f=FileAccess.open(game.SAVE,FileAccess.WRITE)
	f.store_string("{broken");f.close()
	check(game.has_save() and game.read_save().level==4,"Backup recovery")
	print("LEVEL4 PHYSICS + PROGRESSION + SAVES: ","FAIL" if failed else "PASS")
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
