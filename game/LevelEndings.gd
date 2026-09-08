extends RefCounted
# Presentation is authored separately from generated puzzles. IDs, prerequisites,
# items and completion flags stay compatible with existing saves.
const DATA=preload("res://data/endings.json")
static func apply(g):
	var entry=DATA.data[str(g.level)]
	for e in g.events:
		if e.id!=entry.id:continue
		e.cell=entry.cell.duplicate()
		e.presentation=entry.presentation
		if entry.has("offset"):e.ending_offset=entry.offset
		e.erase("wall_face")
		if entry.has("wall_face"):e.wall_face=entry.wall_face
		if is_doctor(e):
			for field in ["title","text","action","objective","success"]:
				e[field]=entry[field][0]
static func is_doctor(e):return e.get("presentation","")=="folamour"
static func ready(g,e):
	for id in e.get("prerequisites",[]):
		if not g.done.has(id):return false
	return not e.has("requires") or g.done.has("installed_"+e.id) or g.held_all(e.requires)
static func show_dialogue(g,e):
	g.current_event=e
	g.clear_modal(e.ref+" / "+g.loc("CONVERSATION"),e.title)
	g.folamour_portrait()
	g.paragraph(e.text,19)
	# The final reasoning puzzle is a conversation with this same doctor,
	# standing at the desk, followed by the invitation to leave together.
	if g.level==25 and not g.done.has("c25_p3"):
		g.paragraph("Folamour attend votre réponse au bureau.",17)
		g.modal_box.add_child(g.button("Poursuivre la conversation",func():
			for puzzle in g.events:
				if puzzle.id=="c25_p3":g.show_puzzle(puzzle),true))
	elif not ready(g,e):
		g.paragraph("Avant de conclure, il reste à préparer :",17)
		for id in e.get("prerequisites",[]):
			if not g.done.has(id):g.paragraph("— "+g.item_name(id),16)
		if not g.done.has("installed_"+e.id):
			for id in e.get("requires",[]):
				if g.inventory.get(id,0)<1:g.paragraph("— "+g.item_name(id),16)
	else:
		g.modal_box.add_child(g.button(e.action,func():
			if e.has("requires") and not g.done.has("installed_"+e.id):g.install_items(e)
			else:g.complete(e),true))
	g.modal_box.add_child(g.button("Revenir explorer",g.close_modal))
