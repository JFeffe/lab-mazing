extends SceneTree
var game
func _initialize(): call_deferred("run")
func snap(name):
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("../../deliverables/"+name+".png")
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.start_game(false)
	game.close_modal()
	game.playing=false
	await create_timer(1).timeout
	await snap("Apercu-prototype")
	# Show a discovered shortcut and the newest-first journal.
	var sc=game.shortcuts[2]
	for side in sc.sides:
		game.player.position=Vector3(side[0]*game.TILE,0.1,side[1]*game.TILE)
		game.record_walk()
	game.update_fog()
	game.update_camera(1)
	game.update_hud()
	await snap("Raccourci-v03")
	game.add_journal("test_old","Ancienne découverte\nPremier message.")
	game.add_journal("test_new","Dernière découverte\nCe message apparaît en premier.")
	game.show_journal()
	await snap("Journal-v03")
	game.show_title()
	await snap("Menu-v02")
	for e in game.events:
		if e.id=="oneway_a":game.player.position=Vector3(13*game.TILE,0.1,23*game.TILE);game.open_oneway(e)
	await snap("Controle-sas-v02")
	for e in game.events:
		if e.id=="star_vault":game.show_puzzle(e)
	await snap("Enigme-v02")
	game.close_modal()
	game.player.position=Vector3(25*game.TILE,0.1,2*game.TILE)
	game.update_fog()
	game.update_camera(1)
	game.find_nearest()
	game.update_hud()
	game.hud.show()
	await snap("Porte-v02")
	quit()
