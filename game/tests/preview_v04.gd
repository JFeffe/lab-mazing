extends SceneTree
var game
func _initialize(): call_deferred("run")
func snap(name):
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("../../deliverables/"+name+".png")
func move_to(x,y):
	game.player.position=Vector3(x*game.TILE,0.1,y*game.TILE)
	game.update_fog()
	game.update_camera(1)
	game.find_nearest()
	game.update_hud()
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.start_game(false,2)
	game.close_modal()
	game.playing=false
	move_to(29,6)
	await create_timer(1).timeout
	await snap("Machines-v04")
	move_to(17,16)
	await snap("Hydraulique-v04")
	game.done.installed_water_manifold=true
	for e in game.events:
		if e.id=="water_manifold":game.show_puzzle(e)
	await snap("Molettes-v04")
	game.close_modal()
	game.inventory={"socket_tool":1,"power_relay":1}
	game.show_inventory()
	await snap("Assemblages-v04")
	game.show_title()
	await snap("Menu-v04")
	quit()
