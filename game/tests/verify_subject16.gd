extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func check(ok,message):
	if not ok:failed=true;push_error(message)
func all_text(node):
	var text=""
	if node is Label or node is Button:text+=node.text+"\n"
	for child in node.get_children():text+=all_text(child)
	return text
func run():
	root.size=Vector2i(1280,800)
	game=load("res://Main.tscn").instantiate();root.add_child(game);game.test_mode=true
	for n in range(1,26):
		game.start_game(false,n,n>1);game.close_modal();await process_frame
		var items=game.events.filter(func(e):return e.kind=="collectible")
		check(items.size()==10,"Ten collectibles level %d"%n)
		for e in game.events:
			if e.kind in ["door","oneway"]:game.done[e.id]=true;game.sync_event(e)
		for y in range(game.grid.size()):
			for x in range(game.grid.size()):game.seen[game.key(x,y)]=true
		var inventory=game.inventory.duplicate(true);var done=game.done.duplicate(true)
		for e in items:
			var c=Vector2i(e.cell[0],e.cell[1]);var origin=c
			for d in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
				if game.Navigator.passable(game,c+d):origin=c+d;break
			game.player.position=Vector3(origin.x*game.TILE,.1,origin.y*game.TILE)
			game.update_fog();game.find_nearest();game.update_hud()
			check(game.event_nodes[e.id].visible,"Hidden accessible collectible "+e.id)
			game.request_event(e)
			var frames=0
			while not game.Subject16.has(game,e) and frames<180:
				await physics_frame;frames+=1
			check(game.Subject16.has(game,e),"Cannot click/walk/collect "+e.id)
			check(not game.modal_open,"Collectible interrupts walking with modal")
			check(not game.event_nodes[e.id].visible and game.event_nodes[e.id].get_node("PickArea").collision_layer==0,"Collectible stays interactive")
			var before=game.dossier.collection.size();game.interact(e)
			check(game.dossier.collection.size()==before,"Duplicate reward")
		check(game.inventory==inventory and game.done==done,"Optional collection altered puzzle state")
		check(game.Subject16.count(game,n)==10 and game.dossier.collection.size()==n*10,"Campaign collection lost")
		print("COLLECTION %02d: 10 / 10 via navigation"%n)
	game.Subject16.show_album(game)
	check(all_text(game.modal_box).contains("Collection complète"),"Full collection archive locked")
	# Save round-trip, visited chapters, old-save migration and replay retention.
	game.close_modal();game.test_mode=false;game.save_game();game.test_mode=true
	game.start_game(true);game.close_modal()
	check(game.dossier.collection.size()==250,"Collection save lost")
	game.start_game(false,1,true);game.close_modal()
	check(game.dossier.collection.size()==250 and game.Subject16.count(game,1)==10,"Replay lost collection")
	var e=game.events.filter(func(v):return v.kind=="collectible")[0]
	check(not game.event_nodes[e.id].visible,"Collected reward respawned after replay")
	game.test_mode=false;game.save_game();game.test_mode=true
	var old=game.read_save();old.erase("subject16");old.erase("decorative_motion");old.erase("folamour_comments")
	var f=FileAccess.open(game.SAVE,FileAccess.WRITE);f.store_string(JSON.stringify(old));f.close()
	game.start_game(true);game.close_modal()
	check(game.dossier.collection.is_empty() and game.level==1,"Legacy save not migrated")
	# Concrete layouts and actual translated dossier panels on phone and desktop.
	for dimensions in [Vector2i(390,844),Vector2i(844,390),Vector2i(1280,800)]:
		root.size=dimensions
		for lang in ["fr","en"]:
			game.localization.choose(lang,false)
			for panel in ["show","show_album","show_observations"]:
				game.Subject16.call(panel,game)
				for i in range(4):await process_frame
				check(game.modal_box.size.x<=game.get_viewport().get_visible_rect().size.x,"Dossier width overflow "+panel)
				check(game.modal_scroll.size.y<=game.get_viewport().get_visible_rect().size.y,"Dossier height overflow")
				if lang=="en":check(not all_text(game.modal_box).contains("facultatif"),"Untranslated dossier")
	game.localization.choose("fr",false);game.start_game(false,5);game.close_modal()
	root.size=Vector2i(844,390)
	for i in range(4):await process_frame
	game.close_modal();game.folamour_line.text="Folamour : Une observation supplémentaire pour compléter votre dossier, sujet 16.";game.folamour_line.show();game.reaction_time=8.0
	for i in range(4):await process_frame
	check(game.hud.get_child(0).get_global_rect().end.y<game.get_viewport().get_visible_rect().size.y-234,"HUD leaves too little visible maze in landscape")
	game.reaction_time=0;game.folamour_comments=false;game.Subject16.react(game,"collect","test")
	check(game.reaction_time==0 and not game.dossier.observations.is_empty(),"Disabled comments lost archive")
	var actor=game.folamour.get_node("DocteurFolamour");game.folamour.show()
	game.player.position=game.folamour.position+Vector3(game.TILE,0,0)
	game.decorative_motion=true;game.Subject16.update(game,1.0)
	check(absf(actor.position.y)>0 and absf(actor.rotation.y)>0,"Folamour idle / gaze absent")
	var pos=actor.position;var rot=actor.rotation;game.decorative_motion=false;game.Subject16.update(game,1.0)
	check(actor.position==pos and actor.rotation==rot,"Motion setting ignored")
	game.start_game(false,1);game.close_modal()
	check(game.dossier.collection.is_empty() and game.dossier.observations.is_empty(),"New adventure did not reset dossier")
	print("SUBJECT 16: ","FAIL" if failed else "PASS"," / 250 physical pickups / save migration / replay / UI / Folamour")
	quit(1 if failed else 0)
