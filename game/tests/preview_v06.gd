extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func texts(node):
	var result=[]
	if node is Button:result.append(node)
	for child in node.get_children():result.append_array(texts(child))
	return result
func snap(name):
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("../docs/"+name+".png")
func tap_button(text):
	for b in texts(game.ui_layer):
		if b.text==text and b.is_visible_in_tree():
			var press=InputEventScreenTouch.new()
			press.index=0
			press.position=root.get_final_transform()*b.get_global_rect().get_center()
			press.pressed=true
			Input.parse_input_event(press)
			await process_frame
			press=press.duplicate()
			press.pressed=false
			Input.parse_input_event(press)
			await process_frame
			return
	failed=true
	push_error("Button not found: "+text)
func run():
	root.size=Vector2i(390,844)
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.choose_language("en")
	await create_timer(0.7).timeout
	await snap("mobile-title")
	await tap_button("Try level 2 directly")
	await create_timer(0.2).timeout
	# No test save should exist. Start may ask confirmation if another test left one.
	if not game.playing: await tap_button("Start")
	await snap("mobile-intro")
	await tap_button("Start exploring")
	if game.modal_open or not game.playing:
		failed=true;push_error("Synthetic touch did not activate GUI")
	await snap("mobile-game")
	await tap_button("Journal")
	await snap("mobile-journal")
	game.close_modal()
	# Real pointer input projected onto a discovered floor, with camera changes while moving.
	var before=game.player.position
	var pos=game.camera.unproject_position(Vector3(game.TILE,0,3*game.TILE))
	var click=InputEventMouseButton.new()
	click.position=root.get_final_transform()*pos;click.button_index=MOUSE_BUTTON_LEFT;click.pressed=true
	Input.parse_input_event(click)
	await create_timer(1.5).timeout
	if game.player.position.distance_to(before)<0.2:failed=true;push_error("Pointer did not move character")
	game.show_pause()
	root.size=Vector2i(844,390)
	await create_timer(0.5).timeout
	await snap("mobile-landscape-pause")
	game.done.installed_water_manifold=true
	for e in game.events:
		if e.id=="water_manifold":game.show_puzzle(e)
	await snap("mobile-landscape-dials")
	root.size=Vector2i(1280,800)
	await create_timer(0.5).timeout
	game.close_modal()
	game.player.position=Vector3(29*game.TILE,0.1,6*game.TILE)
	game.update_fog();game.update_camera(1);game.update_hud()
	await snap("desktop-machines")
	root.size=Vector2i(390,844)
	await create_timer(0.4).timeout
	game.start_game(false,1)
	for e in game.events:
		if e.id=="code03":game.show_puzzle(e)
	await snap("mobile-keypad")
	print("POINTER + TOUCH GUI: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
