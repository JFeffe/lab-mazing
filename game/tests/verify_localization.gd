extends SceneTree
var game
var failed=false
func _initialize(): call_deferred("run")
func check(ok,message):
	if not ok: failed=true;push_error(message)
func event(id):
	for e in game.events:
		if e.id==id: return e
	return {}
func texts(node):
	var result=[]
	if node is Label or node is Button: result.append(node.text)
	for child in node.get_children(): result.append_array(texts(child))
	return result
func state():
	return JSON.stringify([game.level,game.inventory,game.done,game.journal,game.journal_order,game.walked,game.open_shortcuts,game.dial_settings,game.level_stats,game.elapsed,game.player.position])
func run():
	game=load("res://Main.tscn").instantiate()
	root.add_child(game)
	game.test_mode=true
	game.localization.choose("en",false)
	game.show_title()
	check("THE LABYRINTH" in texts(game.modal_box),"English title missing")
	check("Langue / Language" in texts(game.modal_box),"Language option missing")
	for number in [1,2,3,4,5,6,7,8]:
		game.start_game(false,number)
		for e in game.events:
			for field in ["title","text","question","success","action","installed_text"]:
				if e.has(field) and not e[field].is_empty():
					check(game.localization.english.has(e[field]),"Missing translation: "+e.id+"."+field)
			game.add_journal(e.id,e.title+"\n"+e.text)
			check(game.loc(game.journal[e.id])==game.loc(e.title)+"\n"+game.loc(e.text),"Saved journal translation: "+e.id)
			if e.has("success"):
				check(game.loc(e.title+"\n"+e.success)==game.loc(e.title)+"\n"+game.loc(e.success),"Success journal: "+e.id)
		game.show_journal()
		check("NEWEST FIRST" in texts(game.modal_box),"Journal heading")
		for sc in game.shortcuts:
			check(game.loc("Raccourci "+sc.id+" révélé — passage ouvert !")=="Shortcut "+sc.id+" revealed — passage open!","Shortcut toast")
		game.show_map()
		check("Your progress" in texts(game.modal_box),"Map heading")
	game.start_game(false,2)
	# Exercise actual menu callbacks and preserve progress, partial puzzle and old French journal.
	game.inventory={"copper_coil":1,"ceramic_core":1}
	game.done.installed_water_manifold=true
	game.dial_settings.water_manifold=[2,0,1]
	game.add_journal("gauge_tank",event("gauge_tank").title+"\n"+event("gauge_tank").text)
	var previous=state()
	game.show_language(true)
	for child in game.modal_box.get_children():
		if child is Button and child.text=="Français": child.pressed.emit();await process_frame;break
	check(game.localization.language=="fr" and state()==previous,"French switch changes progress")
	game.show_language(true)
	for child in game.modal_box.get_children():
		if child is Button and child.text=="English": child.pressed.emit();await process_frame;break
	check(game.localization.language=="en" and state()==previous,"English switch changes progress")
	check("Bag" in texts(game.hud) and "EXPLORATION MAP" in texts(game.hud),"Persistent HUD did not refresh")
	game.show_puzzle(event("water_manifold"))
	var rendered=texts(game.modal_box)
	check("RETURN\n2" in rendered and "SUPPLY\n0" in rendered and "DRAIN\n1" in rendered,"Translated dial labels / preserved values")
	game.submit_answer()
	check(game.feedback.text=="The mechanism rejects this code. Check the clues you have collected.","Wrong-answer feedback")
	game.dial_settings.water_manifold=[2,3,1]
	game.submit_answer()
	check(game.done.has("water_gate"),"English hydraulic puzzle cannot open gate")
	game.show_inventory()
	check("Copper coil\n" in "\n".join(texts(game.modal_box)),"Inventory translation")
	game.show_journal()
	check(game.loc(game.journal.gauge_tank).begins_with("Tank pressure gauge\nTANK"),"Old French journal did not translate")
	check(game.journal.gauge_tank.begins_with("Manomètre"),"Canonical journal was modified")
	# Preference survives a fresh instance independently of game saves; restore test environment.
	var path=game.localization.SETTINGS
	var existed=FileAccess.file_exists(path)
	var old=FileAccess.get_file_as_bytes(path) if existed else PackedByteArray()
	game.localization.choose("en",true)
	var fresh=load("res://Localization.gd").new()
	check(fresh.language=="en","Language preference not persisted")
	if existed:
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_buffer(old);file.close()
	else: DirAccess.remove_absolute(path)
	game.localization.choose("fr",false)
	check(game.loc(game.journal.gauge_tank)==game.journal.gauge_tank,"French round trip")
	print("LOCALIZATION: ","FAIL" if failed else "PASS"," — both levels, existing journals, menu callbacks, state retention, dials, preference persistence")
	quit(1 if failed else 0)
