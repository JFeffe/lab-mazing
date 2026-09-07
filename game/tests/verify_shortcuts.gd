extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func check(ok,message):
	if not ok:failed=true;push_error(message)
func point(c):return Vector3(c[0]*game.TILE,0.1,c[1]*game.TILE)
func push(direction,frames=65):
	for frame in range(frames):
		await physics_frame
		game.player.velocity=direction*6
		game.player.velocity.y=-2
		game.player.move_and_slide()
		game.record_walk()
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	var audit=JSON.parse_string(FileAccess.get_file_as_string("res://tests/shortcut_audit.json"))
	for number in range(1,6):
		game.start_game(false,number)
		game.close_modal()
		game.playing=false
		for sc in game.shortcuts:
			game.walked.clear()
			game.open_shortcuts.clear()
			game.sync_shortcuts()
			var a=point(sc.sides[0])
			var b=point(sc.sides[1])
			var k=game.key(sc.cell[0],sc.cell[1])
			game.seen[k]=true
			for c in sc.sides:game.seen[game.key(c[0],c[1])]=true
			game.update_fog()
			check(not game.open_shortcuts.has(sc.id),"Fog opens shortcut "+sc.id)
			game.player.position=a
			game.record_walk()
			await push((b-a).normalized(),40)
			check(not game.open_shortcuts.has(sc.id) and game.wall_bodies[k].collision_layer==1,"One side or collision opens "+sc.id)
			check((game.player.position-a).length()<game.TILE,"Unopened wall crossed "+sc.id)
			game.player.position=b
			game.record_walk()
			check(game.open_shortcuts.has(sc.id) and game.wall_bodies[k].collision_layer==0,"Both sides must open "+sc.id)
			var route=game.Navigator.route(game,Vector2i(sc.sides[0][0],sc.sides[0][1]),Vector2i(sc.sides[1][0],sc.sides[1][1]))
			check(route.size()==3,"Click/touch route must use shortcut "+sc.id)
			await push((a-b).normalized())
			check((game.player.position-b).dot((a-b).normalized())>game.TILE,"Shortcut blocked "+sc.id)
			game.player.position=a
			await push((b-a).normalized())
			check((game.player.position-a).dot((b-a).normalized())>game.TILE,"Reverse shortcut blocked "+sc.id)
		# Old revision: checkpoint is inside a former shortcut wall.
		var old=audit[number-1].before[0]
		game.test_mode=false
		game.save_game()
		game.test_mode=true
		var data=game.read_save()
		data.erase("shortcut_layout_revision")
		data.open_shortcuts={old.id:true}
		data.walked={}
		for c in old.sides:data.walked[game.key(c[0],c[1])]=true
		data.walked[game.key(old.cell[0],old.cell[1])]=true
		data.position=[old.cell[0]*game.TILE,0.1,old.cell[1]*game.TILE]
		data.inventory={"checkpoint_token":2}
		data.done={"checkpoint_progress":true}
		var f=FileAccess.open(game.SAVE,FileAccess.WRITE)
		f.store_string(JSON.stringify(data));f.close()
		game.start_game(true)
		game.close_modal()
		game.playing=false
		check(game.inventory.get("checkpoint_token")==2 and game.done.has("checkpoint_progress"),"Migration lost game progress")
		check(game.floor_at(roundi(game.player.position.x/game.TILE),roundi(game.player.position.z/game.TILE)),"Migration leaves player inside wall")
		check(game.player.position.distance_to(point(old.cell))<game.TILE*2,"Migration teleports away from visited corridor")
		for sc in game.shortcuts:
			var eligible=true
			for c in sc.sides:eligible=eligible and game.walked.has(game.key(c[0],c[1]))
			check(game.open_shortcuts.has(sc.id)==eligible,"Stale ID opens relocated shortcut "+sc.id)
		# New placement already visited on both sides must open upon migration,
		# without needing to step onto an unvisited tile first.
		var sc=game.shortcuts[0]
		data.walked={}
		for c in sc.sides:data.walked[game.key(c[0],c[1])]=true
		game.walked=data.walked.duplicate()
		game.restore_shortcuts(data)
		game.sync_shortcuts()
		check(game.open_shortcuts.has(sc.id),"Previously visited sides ignored on migration")
		game.player.position=point(sc.sides[0])
		game.test_mode=false
		game.save_game()
		game.test_mode=true
		check(game.read_save().shortcut_layout_revision==game.SHORTCUT_LAYOUT_REVISION,"Layout revision not saved")
		var order=game.journal_order.duplicate()
		game.start_game(true)
		game.close_modal()
		game.playing=false
		check(game.open_shortcuts.has(sc.id) and game.journal_order==order,"New checkpoint loses shortcut or chronology")
		print("LEVEL ",number," SHORTCUT COLLISIONS + TWO-SIDE REVEAL + MIGRATION PASS")
	print("ALL SHORTCUTS: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
