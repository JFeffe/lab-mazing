extends SceneTree
var game
var failed=false
func _initialize():call_deferred("run")
func check(ok,message):
	if not ok:failed=true;push_error(message)
func event(id):
	for e in game.events:
		if e.id==id:return e
	return {}
func buttons(node):
	var found=[]
	for child in node.get_children():
		if child is Button:found.append(child)
		found.append_array(buttons(child))
	return found
func press(token):
	for b in buttons(game.modal_box):
		if b.text==game.loc(token) and not b.disabled:
			b.pressed.emit();await process_frame;return
	check(false,"Missing button "+token)
func action(index):
	for b in buttons(game.modal_box):
		if b.get_meta("foresight_action",-500)==index and not b.disabled:
			b.pressed.emit();await process_frame;return
	check(false,"Missing action %d in %s"%[index,game.current_event.get("id","?")])
func run():
	game=load("res://Main.tscn").instantiate();root.add_child(game);game.test_mode=true
	game.localization.choose("en",false)
	game.start_game(false,10);game.elapsed=123;game.show_win()
	await press("Entrer au département de la prévoyance")
	var solutions=JSON.parse_string(FileAccess.get_file_as_string("res://tests/chapter3_solutions.json"))
	for number in range(11,16):
		check(game.level==number and game.level_stats.has(str(number-1)),"Campaign transition %d"%number)
		check(game.inventory.is_empty(),"Inventory reset")
		check(is_instance_valid(game.folamour),"Physical Folamour")
		await press("Accepter la mission")
		check(game.done.has("c%d_met"%number),"Intro checkpoint")
		game.close_modal();game.playing=false
		var controls=game.PuzzleControls
		# Both sector gates physically block movement in both directions.
		for e in game.events:
			if e.kind!="door":continue
			var direction=Vector3.RIGHT if e.axis=="x" else Vector3.BACK
			var center=Vector3(e.cell[0]*game.TILE,.1,e.cell[1]*game.TILE)
			for sign_v in [-1,1]:
				game.player.position=center-direction*sign_v*game.TILE
				for frame in range(45):
					await physics_frame;game.player.velocity=direction*sign_v*game.MOVE_SPEED;game.player.velocity.y=-2;game.player.move_and_slide()
				check((game.player.position-center).dot(direction)*sign_v<0,"Gate bypass "+e.id)
		game.player.position=Vector3(game.start_cell.x*game.TILE,.1,game.start_cell.y*game.TILE)
		for step in JSON.parse_string(FileAccess.get_file_as_string("res://tests/route_level%d.json"%number)):
			var e=event(step.id)
			for cell in step.route:
				var target=Vector3(cell[0]*game.TILE,0,cell[1]*game.TILE);var frames=0
				while Vector2(game.player.position.x-target.x,game.player.position.z-target.z).length()>.08:
					await physics_frame
					var offset=target-game.player.position;offset.y=0
					game.player.velocity=offset.normalized()*min(game.MOVE_SPEED,offset.length()*30);game.player.velocity.y=-2;game.player.move_and_slide();game.record_walk();frames+=1
					if frames>120:push_error("Blocked route %s to %s"%[cell,e.id]);quit(1);return
			await physics_frame;game.find_nearest();check(game.nearest.get("id","")==e.id,"Unreachable interaction "+e.id)
			if e.kind in ["clue","pickup"]:game.interact(e)
			else:
				game.show_puzzle(e)
				if e.has("requires"):game.install_items(e)
				if e.has("puzzle_type"):
					controls.submit(game,e);check(not game.done.has(e.id),"Initial state accepted "+e.id)
					# A hint preview and all three tiers in both languages leave the experiment intact.
					for language in ["fr","en"]:
						game.localization.choose(language,false);game.hints.erase(e.id);game.show_puzzle(e)
						var before=JSON.stringify([game.done,game.inventory,game.puzzle_states,game.errors])
						await press("Indice facultatif");check(not game.hints.has(e.id),"Hint preview leaked solution")
						for token in ["Afficher une piste","Afficher la méthode","Révéler la solution"]:await press(token)
						check(game.hints[e.id]==3 and before==JSON.stringify([game.done,game.inventory,game.puzzle_states,game.errors]),"Hints mutate puzzle "+e.id)
					game.show_puzzle(e)
					var steps=[]
					for entry in solutions[str(number)]:
						if entry.id==e.id:steps=entry.actions
					await action(int(steps[0]));var partial=controls.state(game,e).duplicate()
					game.test_mode=false;game.save_game();game.test_mode=true;game.start_game(true);game.close_modal();game.playing=false
					check(game.level==number and controls.state(game,e)==partial,"Partial save "+e.id)
					game.show_puzzle(e);await press("Réinitialiser cet essai")
					check(controls.state(game,e)==controls.initial(e),"Reset "+e.id)
					if e.has("requires"):check(game.done.has("installed_"+e.id) and game.inventory[e.requires[0]]==0,"Reset duplicates kit")
					for i in steps:await action(int(i))
					check(controls.solved(game,e),"Documented solution "+e.id)
					var solved_state=controls.state(game,e).duplicate()
					if e.mode in controls.Foresight.PROGRAMS:
						await action(99);check(not controls.solved(game,e),"Editing must invalidate simulation")
						game.puzzle_states[e.id]=solved_state;game.show_puzzle(e)
					elif e.mode=="tanks":
						await action(99);check(controls.state(game,e).slice(0,3)==[1,4,3],"Undo tank transfer")
						await action(4);check(controls.solved(game,e),"Redo tank transfer")
					await press("Valider l’essai")
				elif e.kind=="exit":await press(e.action)
			check(game.done.has(e.id),"Failed action "+e.id)
			if e.kind!="exit":game.close_modal()
			print("CHAPTER3 ROUTE ",e.id," PASS")
		check(game.won and game.level_stats[str(number)].secrets==3 and game.level_stats[str(number)].puzzles==3,"Level completion %d"%number)
		game.test_mode=false;game.save_game();game.test_mode=true;game.start_game(true);await process_frame
		check(game.won and game.level==number and game.level_stats.has("10"),"Finished resume")
		if number<15:await press("Continuer la mission suivante")
	check(game.level_stats.size()==6,"Campaign totals lost")
	game.show_chapters()
	for n in range(11,16):
		var found=false
		for b in buttons(game.modal_box):
			if b.text==game.level_name(n):found=true
		check(found,"Missing chapter selection %d"%n)
	print("CHAPTER3 PHYSICS + 15 SOLUTIONS + SAVES + HINTS + TRANSITIONS: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
