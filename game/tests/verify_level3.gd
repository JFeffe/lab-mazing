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
	game.start_game(false,2)
	game.elapsed=123
	game.show_win()
	for child in game.modal_box.get_children():
		if child is Button and child.text=="Continue to level 3":child.pressed.emit();await process_frame;break
	check(game.level==3 and game.level_stats.has("2") and game.inventory.is_empty(),"Level 2 to 3 transition")
	game.close_modal()
	game.playing=false
	for e in game.events:
		for field in ["title","text","question","success","action"]:
			if e.has(field):check(game.localization.english.has(e[field]),"Translation missing: "+e.id+"."+field)
	for id in ["optics_gate","archive_gate"]:
		var e=event(id)
		for sign_v in [-1,1]:
			for lane in [-0.9,0,0.9]:
				game.player.position=Vector3(e.cell[0]*game.TILE+lane,0.1,(e.cell[1]-sign_v)*game.TILE)
				for frame in range(60):
					await physics_frame
					game.player.velocity=Vector3(0,-2,sign_v*7)
					game.player.move_and_slide()
				check((game.player.position.z-e.cell[1]*game.TILE)*sign_v<0,"Gate bypass: "+id)
	game.show_puzzle(event("observation_exit"))
	for child in game.modal_box.get_children():
		if child is Button:check(child.text!="Enter the chamber","Exit available early")
	game.close_modal()
	game.player.position=Vector3(game.TILE,0.1,game.TILE)
	var route=JSON.parse_string(FileAccess.get_file_as_string("res://tests/route_level3.json"))
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
			if e.has("answer"):
				game.submit_answer()
				check(not game.done.has(e.id),"Wrong answer accepted: "+e.id)
				if e.has("dials"):
					game.cycle_dial(e,0)
					game.test_mode=false
					game.save_game()
					game.test_mode=true
					game.start_game(true)
					game.close_modal()
					game.playing=false
					check(game.level==3 and game.dial_settings[e.id][0]==1 and game.inventory.prism==0,"Partial dial resume")
					game.show_puzzle(e)
					for i in range(3):
						while game.dial_settings[e.id][i]!=int(str(e.answer)[i]):game.cycle_dial(e,i)
				else:game.code_entry.text=e.answer
				game.submit_answer()
			elif e.kind=="exit":
				for child in game.modal_box.get_children():
					if child is Button and child.text=="Enter the chamber":child.pressed.emit();await process_frame;break
		check(game.done.has(e.id),"Action failed: "+e.id)
		game.close_modal()
		print("LEVEL3 ROUTE ",e.id," PASS")
	check(game.won and game.level_stats["3"].secrets==3,"Level 3 completion and secrets")
	game.test_mode=false
	game.save_game()
	game.test_mode=true
	game.start_game(true)
	await process_frame
	check(game.won and game.level==3 and game.level_stats.has("2"),"Completed level resume")
	# A corrupt primary must recover the previous valid checkpoint.
	var f=FileAccess.open(game.SAVE,FileAccess.WRITE)
	f.store_string("{broken");f.close()
	check(game.has_save() and game.read_save().level==3,"Backup recovery")
	print("LEVEL3 PHYSICS + PROGRESSION + SAVES: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
