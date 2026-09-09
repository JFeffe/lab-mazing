extends SceneTree
var game
var failed=false
func _initialize(): call_deferred("run")
func check(valid,msg):
	if not valid:
		failed=true
		push_error(msg)
func event(id):
	for e in game.events:
		if e.id==id:return e
	return {}
func place(p):
	game.player.position=p
	game.player.velocity=Vector3.ZERO
func push_for(direction,frames):
	for i in range(frames):
		await physics_frame
		game.player.velocity=Vector3(direction.x*6,-2,direction.z*6)
		game.player.move_and_slide()
		game.record_walk()
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.localization.choose("en" if "--english" in OS.get_cmdline_user_args() else "fr",false)
	game.start_game(false)
	game.close_modal()
	game.playing=false
	await physics_frame
	# Test every door from both sides and at three lateral offsets, including edges.
	for e in game.events:
		if not game.door_bodies.has(e.id):continue
		var center=Vector3(e.cell[0]*game.TILE,0.1,e.cell[1]*game.TILE)
		var axis=Vector3.RIGHT if e.axis=="x" else Vector3.BACK
		var lateral=Vector3.BACK if e.axis=="x" else Vector3.RIGHT
		for sign_v in [-1,1]:
			for offset in [-0.9,0,0.9]:
				place(center-axis*sign_v*game.TILE+lateral*offset)
				await push_for(axis*sign_v,65)
				check((game.player.position-center).dot(axis*sign_v)<-0.3,"CLOSED GATE BYPASS "+e.id)
				if e.kind=="oneway": check(game.sas_entry_side(e)==(sign_v==1),"SAS APPROACH AT COLLISION "+e.id)
		if e.kind!="oneway":
			game.done[e.id]=true
			game.sync_event(e)
			place(center-axis*game.TILE)
			await push_for(axis,65)
			check((game.player.position-center).dot(axis)>0.8,"OPEN GATE BLOCK "+e.id)
			game.done.erase(e.id)
			game.sync_event(e)
		else:
			# Explicit reverse interaction and departures with each missing essential.
			for id in e.carry:game.inventory[id]=1
			game.done.exit_protocol=true
			place(center+axis*game.TILE)
			var before=game.player.position
			game.transit_sas(e)
			check(game.player.position==before,"REVERSE SAS "+e.id)
			for missing in e.carry+["exit_protocol"]:
				place(center-axis*game.TILE)
				before=game.player.position
				if missing=="exit_protocol":game.done.erase(missing)
				else:game.inventory[missing]=0
				game.transit_sas(e)
				check(game.player.position==before,"MISSING ESSENTIAL SAS "+missing)
				if missing=="exit_protocol":game.done[missing]=true
				else:game.inventory[missing]=1
			game.inventory.clear()
			game.done.erase("exit_protocol")
	print("COLLISIONS: closed/open gates + 42 edge/side pushes + reverse sas + missing essentials ","FAIL" if failed else "PASS")
	# Shortcuts stay hidden with fog alone or one physically visited side.
	game.start_game(false)
	game.close_modal()
	game.playing=false
	for sc in game.shortcuts:
		var k=game.key(sc.cell[0],sc.cell[1])
		for side in sc.sides:game.seen[game.key(side[0],side[1])]=true
		game.update_fog()
		check(not game.open_shortcuts.has(sc.id),"FOG REVEALED SHORTCUT "+sc.id)
		var a=Vector3(sc.sides[0][0]*game.TILE,0.1,sc.sides[0][1]*game.TILE)
		var b=Vector3(sc.sides[1][0]*game.TILE,0.1,sc.sides[1][1]*game.TILE)
		place(a)
		game.record_walk()
		check(not game.open_shortcuts.has(sc.id),"ONE SIDE REVEALED SHORTCUT "+sc.id)
		await push_for((b-a).normalized(),40)
		check(not game.open_shortcuts.has(sc.id),"WALKED THROUGH UNREVEALED SHORTCUT "+sc.id)
		place(b)
		game.record_walk()
		check(game.open_shortcuts.has(sc.id) and game.wall_bodies[k].collision_layer==0,"TWO SIDES DID NOT OPEN "+sc.id)
		await push_for((a-b).normalized(),65)
		check((game.player.position-b).dot((a-b).normalized())>game.TILE,"SHORTCUT COLLISION "+sc.id)
		place(a)
		await push_for((b-a).normalized(),65)
		check((game.player.position-a).dot((b-a).normalized())>game.TILE,"SHORTCUT REVERSE COLLISION "+sc.id)
	game.add_journal("old_note","old")
	game.add_journal("new_note","new")
	check(game.recent_journal_keys()[0]=="new_note","JOURNAL ORDER")
	game.add_journal("old_note","read again")
	check(game.recent_journal_keys()[0]=="old_note" and game.recent_journal_keys().count("old_note")==1,"JOURNAL REVISIT")
	game.test_mode=false
	game.save_game()
	var saved_walked=game.walked.duplicate()
	var saved_order=game.journal_order.duplicate()
	game.walked.clear()
	game.open_shortcuts.clear()
	game.journal_order.clear()
	game.load_game()
	check(game.open_shortcuts.size()==game.shortcuts.size() and game.walked==saved_walked and game.journal_order==saved_order,"SAVE SHORTCUTS/CHRONOLOGY")
	game.test_mode=true
	check(is_equal_approx(game.MOVE_SPEED,7.0*1.3) and not InputMap.has_action("run"),"SPEED / RUN BINDING")
	print("SHORTCUTS + JOURNAL + SAVE + SPEED: ","FAIL" if failed else "PASS")
	game.start_game(false)
	game.close_modal()
	game.playing=false
	var sas="oneway_b" if "--sas-b" in OS.get_cmdline_user_args() else "oneway_a"
	var route=JSON.parse_string(FileAccess.get_file_as_string("res://tests/route_"+sas+".json"))
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
				game.player.velocity=offset.normalized()*min(8.0,offset.length()*30)
				game.player.velocity.y=-2
				game.player.move_and_slide()
				game.record_walk()
				frames+=1
				if frames>120:
					check(false,"ROUTE COLLISION "+str(cell)+" approaching "+e.id)
					quit(1)
					return
			steps+=1
		await physics_frame
		game.find_nearest()
		check(game.nearest.get("id","")==e.id,"INTERACTION UNREACHABLE "+e.id+" nearest="+game.nearest.get("id","none"))
		if e.kind=="oneway":
			var before=game.inventory.duplicate()
			game.transit_sas(e)
			check(game.player.position.z>(e.cell[1]+0.8)*game.TILE,"SAS DID NOT TRANSFER")
			check(game.inventory==before,"SAS LOST INVENTORY")
			check(game.door_bodies[e.id].collision_layer==1,"SAS OPENED BACKWARD")
		elif e.kind in ["pickup","clue"]:
			game.interact(e)
			if e.kind=="pickup":
				game.interact(e)
				check(game.inventory[e.id]==1,"DUPLICATE PICKUP "+e.id)
		else:
			game.show_puzzle(e)
			if e.has("requires"):
				game.install_items(e)
				game.install_items(e)
				for id in e.requires:check(game.inventory[id]==0,"INSTALL COUNT "+id)
			if e.has("answer"):
				game.code_entry.text="0000"
				game.submit_answer()
				check(not game.done.has(e.id),"WRONG CODE ACCEPTED")
				game.code_entry.text=e.answer
				game.submit_answer()
			check(game.done.has(e.id),"MECHANISM DID NOT OPEN "+e.id)
		game.close_modal()
		print("ROUTE ",e.id," OK")
	check(game.won,"EXIT DID NOT COMPLETE")
	# Persist and resume after consumption; historical engravings must survive.
	game.won=false
	game.test_mode=false
	game.save_game()
	var before=game.done.duplicate()
	game.done.clear()
	game.inventory.clear()
	game.journal.clear()
	game.load_game()
	check(game.done==before and game.journal.has("disc_moon") and game.inventory.disc_moon==0,"SAVE/LOAD CONSUMED ITEMS")
	DirAccess.remove_absolute(game.SAVE)
	print("ESCAPE ROOM ",sas,": ","FAIL" if failed else "PASS"," — ",steps," route cells; real collisions, inventory, mechanisms, journal, save/load.")
	quit(1 if failed else 0)
