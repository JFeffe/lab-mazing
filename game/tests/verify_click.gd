extends SceneTree
var game
var failed=false
func _initialize(): call_deferred("run")
func check(ok,message):
	if not ok:failed=true;push_error(message)
func event(id):
	for e in game.events:
		if e.id==id:return e
	return {}
func visit(id):
	game.close_modal()
	game.request_event(event(id))
	var frames=0
	while not game.modal_open and frames<40000:
		await physics_frame
		frames+=1
	check(game.modal_open,"Click navigation failed: "+id)
	check(game.move_path.is_empty(),"Movement continues during modal")
	print("CLICK ",id," frames=",frames)
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.localization.choose("en",false)
	game.start_game(false,2)
	game.close_modal()
	check(not game.request_cell(Vector2i(33,33)),"Unexplored destination accepted")
	for y in range(game.grid.size()):
		for x in range(game.grid.size()):game.seen[game.key(x,y)]=true
	check(not game.request_cell(Vector2i(1,13)),"Navigation crosses locked 105")
	check(not game.Navigator.passable(game,Vector2i(17,11)),"Closed door passable")
	for id in ["tool_handle","tool_head","tool_bench","generator","valve_wheel","gauge_pump","gauge_filter","gauge_tank","pipe_plan","water_manifold","copper_coil","ceramic_core","relay_bench","hoist_cable","hoist_hook","hoist","lift_power","lift_exit"]:
		await visit(id)
		var e=event(id)
		if e.has("requires"):game.install_items(e)
		if e.has("dials"):
			game.dial_settings[e.id]=[2,3,1]
			game.submit_answer()
		if id=="lift_exit":game.complete(e)
	check(game.won,"Click-only campaign did not reach exit")
	check(game.journal_entry("object_power_relay").begins_with("[210]"),"Craft reference missing")
	# One-way barriers remain impassable to automatic navigation, even after transit.
	game.start_game(false,1)
	for y in range(game.grid.size()):
		for x in range(game.grid.size()):game.seen[game.key(x,y)]=true
	check(not game.Navigator.passable(game,Vector2i(13,24)),"Sas bypass via pathfinder")
	game.done.oneway_a=true
	check(not game.Navigator.passable(game,Vector2i(13,24)),"Used sas becomes bidirectional")
	game.close_modal()
	game.request_cell(Vector2i(9,1))
	game.show_pause()
	check(game.move_path.is_empty(),"Pause retains movement request")
	game.ui_mobile=true
	game.show_puzzle(event("code03"))
	for digit in ["4","7","2","6"]:
		for child in game.modal_box.get_children():
			if child is GridContainer:
				for b in child.get_children():
					if b.text==digit: b.pressed.emit();await process_frame;break
	check(game.code_entry.text=="4726","Touch keypad does not compose code")
	game.submit_answer()
	check(game.done.has("code03"),"Keypad did not open level-one door")
	print("CLICK / TOUCH NAVIGATION: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
