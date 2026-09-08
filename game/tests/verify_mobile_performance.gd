extends SceneTree
func _initialize():call_deferred("run")
func run():
	var game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	for level in range(1,8):
		game.start_game(false,level)
		game.close_modal()
		var meshes={}
		var nodes=game.world.find_children("*","MeshInstance3D",true,false)
		var boxes=0
		for node in nodes:
			if node.mesh is BoxMesh:
				boxes+=1
				meshes[node.mesh.get_instance_id()]=true
		assert(meshes.size()<boxes/3,"Box resources must be shared")
		var remembered=game.seen.duplicate()
		game.update_fog()
		for cell in remembered:assert(game.seen.has(cell),"Culling erased exploration")
		assert(game.render_near(game.player))
		print("Level %d: %d boxes, %d shared meshes" %[level,boxes,meshes.size()])
		await process_frame
	print("PASS mobile resource sharing and exploration")
	quit()
