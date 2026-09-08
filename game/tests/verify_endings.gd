extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func check(ok,message):
	if not ok:failed=true;push_error(message)
func has_action(e):
	for child in game.modal_box.get_children():
		if child is Button and child.text==game.loc(e.action) and not child.disabled:return true
	return false
func run():
	game=load("res://Main.tscn").instantiate();root.add_child(game);game.test_mode=true
	for level in range(1,26):
		game.start_game(false,level);game.close_modal()
		var endings=game.events.filter(func(e):return e.kind=="exit")
		check(endings.size()==1,"One ending per level %d"%level)
		var e=endings[0];var node=game.event_nodes[e.id]
		var c=Vector2i(e.cell[0],e.cell[1])
		check(game.floor_at(c.x,c.y),"Ending on a wall %d"%level)
		for other in game.events:
			if other.id!=e.id:check(other.cell!=e.cell,"Overlapping ending %d"%level)
		if level<5:
			check(game.door_bodies.has(e.id),"Missing physical exit %d"%level)
			if e.has("wall_face"):
				check(not game.floor_at(c.x+int(e.wall_face[0]),c.y+int(e.wall_face[1])),"Wall mount has no wall")
			else:
				check(not game.floor_at(c.x-1,c.y) and not game.floor_at(c.x+1,c.y),"Threshold floats in a room")
			continue
		check(game.LevelEndings.is_doctor(e) and game.folamour==node,"Ending is not Folamour %d"%level)
		check(node.get_node_or_null("DocteurFolamour")!=null,"No doctor model %d"%level)
		check(not game.door_bodies.has(e.id) and node.get_node_or_null("Leaf")==null,"Doctor still has a door %d"%level)
		check(not e.has("wall_face"),"Doctor embedded in wall")
		check(node.get_node("PickArea").get_meta("event_id")==e.id,"Click target is not the ending")
		var before=game.inventory.duplicate()
		game.complete(e)
		check(not game.won and game.inventory==before,"Premature ending %d"%level)
		for id in e.prerequisites:game.done[id]=true
		for id in e.get("requires",[]):game.inventory[id]=1
		for missing in e.prerequisites:
			game.done.erase(missing)
			game.show_puzzle(e)
			check(not has_action(e),"Missing prerequisite accepted %d / %s"%[level,missing])
			game.complete(e);check(not game.won,"Completion bypass %d"%level)
			game.done[missing]=true
		for missing in e.get("requires",[]):
			game.inventory[missing]=0;game.show_puzzle(e)
			check(not has_action(e),"Missing delivery accepted %d"%level)
			game.inventory[missing]=1
		for language in ["fr","en"]:
			game.localization.choose(language,false);game.show_puzzle(e)
			check(has_action(e),"No translated final action %d"%level)
			for field in ["title","text","action","objective"]:check(game.localization.english.has(e[field]),"Untranslated ending")
		game.close_modal()
		# Existing saves keep their IDs/items and rebuild the new actor on resume.
		game.player.position=Vector3(c.x*game.TILE,.1,c.y*game.TILE)
		game.test_mode=false;game.save_game();game.test_mode=true;game.start_game(true);game.close_modal()
		check(not game.won and game.LevelEndings.ready(game,e),"Ready save changed %d"%level)
		for y in range(game.grid.size()):
			for x in range(game.grid.size()):game.seen[game.key(x,y)]=true
		check(game.Navigator.passable(game,c),"Doctor blocks passage %d"%level)
		# Use the same routing and automatic interaction as clicking/touching him.
		var origin=c
		for dir in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
			if game.Navigator.passable(game,c+dir):origin=c+dir;break
		game.player.position=Vector3(origin.x*game.TILE,.1,origin.y*game.TILE)
		game.request_event(e)
		var frames=0
		while not game.modal_open and frames<180:
			await physics_frame;frames+=1
		check(game.modal_open and has_action(e),"Doctor cannot be reached by click %d"%level)
		game.close_modal();game.find_nearest();game.update_hud()
		check(game.nearest.get("id","")==e.id and game.interact_button.text==game.loc("Parler"),"No Talk action %d"%level)
		game.interact(e)
		for b in game.modal_box.get_children():
			if b is Button and b.text==game.loc(e.action):b.pressed.emit();await process_frame;break
		check(game.won and game.done.has(e.id) and game.level_stats.has(str(level)),"Dialogue did not finish %d"%level)
		for id in e.get("requires",[]):check(game.inventory[id]==0,"Delivery not consumed once")
		game.complete(e)
		for id in e.get("requires",[]):check(game.inventory[id]==0,"Duplicate delivery consumption")
		game.test_mode=false;game.save_game();game.test_mode=true;game.start_game(true);await process_frame
		check(game.won and game.done.has(e.id),"Finished save lost %d"%level)
		print("ENDING %d: PASS"%level)
	print("ALL 25 ENDINGS / DIALOGUES / NAVIGATION / SAVES: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
