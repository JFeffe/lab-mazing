extends SceneTree
var game
var failed=false
func _initialize(): call_deferred("run")
func check(ok,msg):
	if not ok:failed=true;push_error(msg)
func event(id):
	for e in game.events:
		if e.id==id:return e
	return {}
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.localization.choose("en" if "--english" in OS.get_cmdline_user_args() else "fr",false)
	game.start_game(false)
	game.close_modal()
	game.playing=false
	# Transition endpoint independently from the first-level physical regression.
	game.inventory={"disc_sun":1,"legacy_dummy":9}
	game.add_journal("legacy_note","level 1")
	game.elapsed=123
	game.show_win()
	check(game.level_stats.has("1"),"LEVEL1 SUMMARY NOT RECORDED")
	for child in game.modal_box.get_children():
		if child is Button and child.text==game.loc("Continuer vers le niveau 2"):child.pressed.emit();await process_frame;break
	check(game.level==2 and game.inventory.is_empty() and not game.journal.has("legacy_note"),"TRANSITION DID NOT RESET INVENTORY/JOURNAL")
	check(game.level_stats["1"].time==123,"TRANSITION LOST SUMMARY")
	game.close_modal()
	game.playing=false
	game.test_mode=false
	game.save_game()
	game.test_mode=true
	game.start_game(true)
	game.close_modal()
	game.playing=false
	check(game.level==2 and game.level_stats.has("1") and is_equal_approx(game.player.position.x,game.TILE),"LEVEL2 CHECKPOINT RESUME")
	await physics_frame
	# Gates and final controls must stay blocked before their dependencies.
	for id in ["power_gate","water_gate","lift_exit"]:
		var e=event(id)
		for sign_v in [-1,1]:
			for lane in [-0.9,0,0.9]:
				game.player.position=Vector3(e.cell[0]*game.TILE+lane,0.1,(e.cell[1]-sign_v)*game.TILE)
				for frame in range(60):
					await physics_frame
					game.player.velocity=Vector3(0,-2,sign_v*7)
					game.player.move_and_slide()
				check((game.player.position.z-e.cell[1]*game.TILE)*sign_v<0,"GATE BYPASS "+id)
	game.show_puzzle(event("lift_exit"))
	for child in game.modal_box.get_children():
		if child is Button:check(child.text!=game.loc("Monter dans l’ascenseur"),"FINAL ACTION AVAILABLE EARLY")
	game.close_modal()
	game.player.position=Vector3(game.TILE,0.1,game.TILE)
	# Full route at actual gameplay speed and with physical-visit shortcut recording.
	var route=JSON.parse_string(FileAccess.get_file_as_string("res://tests/route_level2.json"))
	var steps=0
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
				if frames>120:
					check(false,"ROUTE BLOCK "+str(cell)+" toward "+e.id)
					quit(1)
					return
			steps+=1
		await physics_frame
		game.find_nearest()
		check(game.nearest.get("id","")==e.id,"INTERACTION THROUGH WALL / OUT OF REACH "+e.id+" nearest="+game.nearest.get("id","none"))
		if e.kind in ["pickup","clue"]:
			game.interact(e)
			if e.kind=="pickup":game.interact(e);check(game.inventory[e.id]==1,"DUPLICATE PICKUP")
		else:
			game.show_puzzle(e)
			if e.has("requires"):
				game.install_items(e)
				game.install_items(e)
				for id in e.requires:check(game.inventory[id]==0,"DOUBLE CONSUMPTION "+id)
			if e.has("dials"):
				game.submit_answer()
				check(not game.done.has(e.id),"WRONG DIALS ACCEPTED")
				# Drive each actual dial button; test closing and reloading partway through.
				game.cycle_dial(e,0)
				game.test_mode=false
				game.save_game()
				game.test_mode=true
				game.start_game(true)
				game.close_modal()
				game.playing=false
				check(game.done.has("installed_water_manifold") and game.inventory.valve_wheel==0 and game.dial_settings.water_manifold[0]==1,"PARTIAL DIAL RESUME")
				game.show_puzzle(e)
				for i in range(3):
					var target_value=int(str(e.answer)[i])
					while game.dial_settings[e.id][i]!=target_value:
						for child in game.modal_box.get_children():
							if child is HBoxContainer:child.get_child(i).pressed.emit();await process_frame;break
				game.submit_answer()
			elif e.kind=="exit":
				for child in game.modal_box.get_children():
					if child is Button and child.text==game.loc(e.action):child.pressed.emit();await process_frame;break
			check(game.done.has(e.id),"MECHANISM FAILED "+e.id)
			for id in e.get("grants",{}):check(game.inventory.get(id,0)==1,"CRAFT OUTPUT MISSING/DUPLICATED "+id)
		game.close_modal()
		print("LEVEL2 ROUTE ",e.id," OK")
	check(game.won and game.level_stats.size()==2,"CAMPAIGN DID NOT FINISH")
	check(game.inventory.get("power_relay",0)==0,"FINAL RELAY NOT CONSUMED")
	game.test_mode=false
	game.save_game()
	game.test_mode=true
	game.start_game(true)
	await process_frame
	check(game.level==2 and game.won and game.level_stats.size()==2,"COMPLETED CAMPAIGN RESUME")
	DirAccess.remove_absolute(game.SAVE)
	print("CAMPAIGN + MACHINES: ","FAIL" if failed else "PASS"," — ",steps," physical route cells, gates, crafting, interactive dials, partial saves, full campaign.")
	quit(1 if failed else 0)
