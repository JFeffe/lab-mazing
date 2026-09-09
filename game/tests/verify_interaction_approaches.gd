extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func check(ok,message):
	if not ok:failed=true;push_error(message)
func run():
	game=load("res://Main.tscn").instantiate();root.add_child(game);game.test_mode=true
	# Wall-mounted controls must be approached far enough to actually interact.
	# The old route chose the closest grid neighbor, even outside interaction range.
	for number in [3,4]:
		game.start_game(false,number);game.close_modal()
		for e in game.events:
			if e.kind=="door" and not e.has("wall_face"):game.done[e.id]=true;game.sync_event(e)
		for y in range(game.grid.size()):
			for x in range(game.grid[y].size()):game.seen[game.key(x,y)]=true
		for e in game.events:
			if not e.has("wall_face"):continue
			var c=Vector2i(e.cell[0],e.cell[1])
			for direction in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
				var from=c+direction
				if not game.Navigator.passable(game,from):continue
				game.close_modal();game.player.position=Vector3(from.x*game.TILE,.1,from.y*game.TILE)
				await physics_frame
				game.request_event(e)
				var frames=0
				while not game.modal_open and frames<180:
					await physics_frame;frames+=1
				check(game.modal_open and game.current_event.get("id","")==e.id,"Click cannot approach wall control %s from %s"%[e.id,from])
	# An unreachable object replaces the previous movement request, just like floor clicks.
	game.start_game(false,2);game.close_modal()
	game.request_cell(Vector2i(1,3))
	check(not game.move_path.is_empty(),"Setup: accessible starting route")
	var target=game.events.filter(func(e):return e.id=="lift_exit")[0]
	game.request_event(target)
	check(game.move_path.is_empty() and game.click_event.is_empty() and not game.destination_marker.visible,"Unreachable object retains previous destination")
	print("INTERACTION APPROACHES: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
