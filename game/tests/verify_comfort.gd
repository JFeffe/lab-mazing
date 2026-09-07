extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func check(ok,msg):
	if not ok:failed=true;push_error(msg)
func run():
	root.size=Vector2i(390,844)
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.start_game(false,3)
	game.close_modal()
	await process_frame
	await process_frame
	await process_frame
	check(game.ui_mobile,"Mobile layout not detected")
	check(game.modal_scroll.size.x<=game.get_viewport().get_visible_rect().size.x,"Mobile modal too wide")
	game.request_cell(Vector2i(1,3))
	game.update_hud()
	check(not game.move_path.is_empty() and game.destination_marker.visible,"Destination marker missing")
	check(game.action_label.text.begins_with("Destination"),"Destination label missing")
	game.show_map()
	var preview_found=false
	for child in game.modal_box.get_children():
		if child.get_script()==game.MapWidget: preview_found=not child.route_preview.is_empty()
	check(preview_found,"Mobile map route preview missing")
	game.show_pause()
	check(game.move_path.is_empty() and not game.destination_marker.visible,"Pause did not cancel destination")
	game.close_modal()
	game.auto_timer=4.1
	game.test_mode=false
	game._physics_process(0.01)
	game.test_mode=true
	check(game.read_save().get("level",0)==3,"Timed autosave missing")
	check(game.save_status=="Progression sauvegardée sur cet appareil.","Save confirmation missing")
	game.show_title()
	game.start_game(true)
	check(game.level==3,"Resume wrong level")
	root.size=Vector2i(844,390)
	await process_frame
	await process_frame
	game.show_pause()
	check(game.modal_scroll.size.y<=game.get_viewport().get_visible_rect().size.y,"Landscape menu exceeds viewport")
	print("MOBILE LAYOUT + DESTINATION + AUTOSAVE: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
