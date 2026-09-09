extends SceneTree
var game
var output=OS.get_environment("LAB_AUDIT_SHOTS")
func _initialize():call_deferred("run")
func snap(name):
	for i in range(3):await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(output+"/"+name+".png")
func run():
	if output.is_empty():push_error("Set LAB_AUDIT_SHOTS to an output directory");quit(1);return
	DirAccess.make_dir_recursive_absolute(output)
	root.size=Vector2i(1280,800)
	game=load("res://Main.tscn").instantiate();root.add_child(game);game.test_mode=true
	for number in range(1,26):
		game.start_game(false,number);game.close_modal()
		var focus=game.start_cell
		if not game.shortcuts.is_empty():
			var sc=game.shortcuts[-1]
			for side in sc.sides:game.walked[game.key(side[0],side[1])]=true
			game.restore_shortcuts({"shortcut_layout_revision":game.SHORTCUT_LAYOUT_REVISION})
			game.sync_shortcuts()
			focus=Vector2i(sc.sides[0][0],sc.sides[0][1])
		game.player.position=Vector3(focus.x*game.TILE,.1,focus.y*game.TILE)
		game.zoom=30.0;game.update_camera(1);game.update_fog();game.find_nearest();game.update_hud()
		await snap("level-%02d"%number)
		print("VISUAL ",number," CAPTURED")
	game.start_game(false,3);game.close_modal()
	for dimensions in [Vector2i(390,844),Vector2i(844,390)]:
		root.size=dimensions;game.show_pause()
		await snap("pause-%dx%d"%[dimensions.x,dimensions.y])
		game.Subject16.show(game)
		await snap("dossier-%dx%d"%[dimensions.x,dimensions.y])
	quit()
