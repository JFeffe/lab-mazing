extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func check(ok,message):
	if not ok:failed=true;push_error(message)
func write_save(data):
	var file=FileAccess.open(game.SAVE,FileAccess.WRITE)
	file.store_string(JSON.stringify(data));file.close()
func run():
	game=load("res://Main.tscn").instantiate();root.add_child(game);game.test_mode=true
	var audit=JSON.parse_string(FileAccess.get_file_as_string("res://tests/return_links_audit.json"))
	for row in audit.levels:
		game.start_game(false,int(row.level));game.close_modal();game.playing=false
		game.test_mode=false;game.save_game();game.test_mode=true
		var saved=game.read_save()
		saved.inventory={"retained_test_item":2};saved.done={"retained_test_progress":true}
		saved.hints={"retained_test_hint":2};saved.puzzle_states={"retained_test_puzzle":[1,2,0]}
		saved.subject16.collection={"retained_test_collectible":true}
		saved.walked={};saved.open_shortcuts={};saved.journal={};saved.journal_order=[]
		# Reproduce a v0.21 checkpoint standing inside an existing secret door.
		if not row.before.is_empty():
			var old=row.before[0]
			for side in old.sides:saved.walked[game.key(side[0],side[1])]=true
			saved.open_shortcuts[old.id]=true
			saved.position=[old.cell[0]*game.TILE,.1,old.cell[1]*game.TILE]
		# An already walked new door must unlock on resume without a fresh step.
		if not row.added_ids.is_empty():
			for sc in game.shortcuts:
				if sc.id==row.added_ids[0]:
					for side in sc.sides:saved.walked[game.key(side[0],side[1])]=true
		# Visibility of both sides alone must never grant any remaining door.
		for sc in game.shortcuts:
			for side in sc.sides:saved.seen[game.key(side[0],side[1])]=true
		write_save(saved);game.start_game(true);game.close_modal();game.playing=false
		check(game.inventory.get("retained_test_item")==2 and game.done.has("retained_test_progress") and game.hints.get("retained_test_hint")==2,"Items, progress or hints lost on additive upgrade %d"%game.level)
		# Loading a level also initializes its untouched mechanisms. Check that the
		# persisted partial trial survives without rejecting those legitimate keys.
		check(game.puzzle_states.get("retained_test_puzzle",[]).map(func(v):return int(v))==[1,2,0],"Partial puzzle lost on additive upgrade")
		check(game.dossier.collection==saved.subject16.collection,"Collection lost on additive upgrade")
		check(game.player.position.distance_to(Vector3(saved.position[0],.1,saved.position[2]))<.01,"Existing checkpoint moved on additive upgrade")
		for sc in game.shortcuts:
			var eligible=true
			for side in sc.sides:eligible=eligible and saved.walked.has(game.key(side[0],side[1]))
			check(game.open_shortcuts.has(sc.id)==eligible,"Two-side save discovery failed %d %s"%[game.level,sc.id])
		var opened=game.open_shortcuts.duplicate();var journal_order=game.journal_order.duplicate()
		game.test_mode=false;game.save_game();game.test_mode=true
		game.start_game(true);game.close_modal();game.playing=false
		check(game.open_shortcuts==opened and game.journal_order==journal_order,"Second resume loses door or duplicates journal")
		print("RETURN SAVE %02d: PASS"%int(row.level))
	print("ADDITIVE RETURN SAVES: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
