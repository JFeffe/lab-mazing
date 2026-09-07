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
	game.choose_language("en")
	game.show_title()
	await create_timer(0.5).timeout
	await snap("Menu-English-v05")
	game.show_language()
	await snap("Language-v05")
	game.start_game(false,2)
	game.close_modal()
	game.show_pause()
	await snap("Pause-English-v05")
	game.done.installed_water_manifold=true
	game.dial_settings.water_manifold=[2,3,1]
	for e in game.events:
		if e.id=="water_manifold":game.show_puzzle(e)
	await snap("Dials-English-v05")
	game.inventory={"socket_tool":1,"power_relay":1}
	game.show_inventory()
	await snap("Bag-English-v05")
	for e in game.events:
		if e.id in ["pipe_plan","gauge_tank"]:game.add_journal(e.id,e.title+"\n"+e.text)
	game.show_journal()
	await snap("Journal-English-v05")
	game.choose_language("fr",true)
	game.show_pause()
	await snap("Pause-Francais-v05")
	quit()
