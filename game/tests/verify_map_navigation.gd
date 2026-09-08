extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func check(ok,message):
	if not ok:failed=true;push_error(message)
func map_click(map,point,button=MOUSE_BUTTON_RIGHT):
	var event=InputEventMouseButton.new()
	event.button_index=button
	event.pressed=true
	event.position=point
	map._gui_input(event)
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.start_game(false,4)
	game.close_modal()
	game.zoom=36.0
	var wheel=InputEventMouseButton.new()
	wheel.button_index=MOUSE_BUTTON_WHEEL_DOWN
	wheel.pressed=true
	for i in range(20):game._unhandled_input(wheel)
	check(game.zoom==48,"Extended zoom limit")
	for y in range(game.grid.size()):
		for x in range(game.grid.size()):game.seen[game.key(x,y)]=true
	game.show_map()
	var map
	for child in game.modal_box.get_children():
		if child.get_script()==game.MapWidget:map=child
	await process_frame
	var cell=min(map.size.x,map.size.y)/game.grid.size()
	var offset=(map.size-Vector2.ONE*cell*game.grid.size())/2
	map_click(map,offset+Vector2(2.5,1.5)*cell,MOUSE_BUTTON_LEFT)
	check(game.modal_open and game.move_path.is_empty(),"Left click must not navigate")
	map_click(map,offset+Vector2(0.5,0.5)*cell)
	check(game.modal_open and game.move_path.is_empty(),"Wall accepted")
	map_click(map,offset+Vector2(17.5,13.5)*cell)
	check(game.modal_open and game.move_path.is_empty(),"Locked region accepted")
	game.seen.erase(game.key(2,1))
	map_click(map,offset+Vector2(2.5,1.5)*cell)
	check(game.modal_open and game.move_path.is_empty(),"Unexplored cell accepted")
	game.seen[game.key(2,1)]=true
	map_click(map,offset+Vector2(2.5,1.5)*cell)
	check(not game.modal_open and game.move_path[-1]==Vector2i(2,1),"Right click did not close map and set route")
	for i in range(120):await physics_frame
	check(game.move_path.is_empty() and abs(game.player.position.x-2*game.TILE)<0.1,"Player did not reach map destination")
	game.player.position=Vector3(16*game.TILE,0.1,33*game.TILE)
	check(game.request_cell(Vector2i(18,33)),"Cannot route along exit corridor")
	for i in range(120):await physics_frame
	check(game.move_path.is_empty() and abs(game.player.position.x-18*game.TILE)<0.1,"Wall exit physically blocks corridor")
	var exit_node=game.event_nodes.test_exit
	check(exit_node.position.z>33*game.TILE+1,"Exit not mounted on south wall")
	check(game.Navigator.passable(game,Vector2i(17,33)),"Wall exit blocks corridor navigation")
	game.player.position=Vector3(17*game.TILE,0.1,33*game.TILE)
	await physics_frame
	game.find_nearest()
	check(game.nearest.get("id","")=="test_exit","Wall exit cannot be examined")
	for language in ["fr","en"]:
		game.localization.choose(language,false)
		for mobile in [false,true]:
			game.ui_mobile=mobile
			for source in ["Ramasser","Examiner"]:
				var b=game.interact_button
				var width=b.get_theme_font("font").get_string_size(game.loc(source),HORIZONTAL_ALIGNMENT_LEFT,-1,b.get_theme_font_size("font_size")).x
				check(width+b.get_theme_stylebox("normal").get_minimum_size().x<=125,"Action text exceeds button width")
	print("MAP NAVIGATION / ZOOM / WALL EXIT / BUTTONS: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
