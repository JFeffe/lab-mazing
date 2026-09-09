extends RefCounted
const DATA=preload("res://data/subject16.json")
const PLACEMENTS=preload("res://data/collectibles.json")
static func blank():return {"collection":{},"observations":{},"visited":{}}
static func chapter(level):return int((level-1)/5)+1
static func theme(level):return DATA.data.chapters[str(chapter(level))]
static func apply(g):
	for item in PLACEMENTS.data[str(g.level)]:
		var e=item.duplicate(true)
		e.kind="collectible";e.title=theme(g.level).collectible[0]+" · "+e.ref
		e.text="Collectible facultatif du dossier du sujet 16."
		g.events.append(e)
static func has(g,e):return g.dossier.collection.has(e.id)
static func count(g,level):
	var total=0
	for item in PLACEMENTS.data[str(level)]:
		if has(g,item):total+=1
	return total
static func chapter_count(g,c):
	var total=0
	for n in range((c-1)*5+1,c*5+1):total+=count(g,n)
	return total
static func collect(g,e):
	if has(g,e):return
	g.dossier.collection[e.id]=true
	g.sync_event(e)
	g.toast(g.loc("Souvenir classé : %s · %d / 10")%[g.loc(theme(g.level).collectible[0]),count(g,g.level)])
	if is_instance_valid(g.soundscape):g.soundscape.effect(g,"pickup")
	if count(g,g.level) in [1,5,10]:react(g,"collect",str(count(g,g.level)))
	if chapter_count(g,chapter(g.level)) in [10,25,50]:g.toast("Nouvelle archive disponible dans le dossier du sujet 16.")
	g.find_nearest();g.update_hud();g.save_game()
static func react(g,kind,tag=""):
	var id=str(g.level)+"_"+kind+"_"+tag
	if g.dossier.observations.has(id):return
	var line=DATA.data.reactions[kind][chapter(g.level)-1][0]
	g.dossier.observations[id]=line
	if g.folamour_comments:
		g.reaction_text=line;g.reaction_time=7.0
static func update(g,delta):
	if not g.playing or g.modal_open:return
	g.reaction_time=maxf(0,g.reaction_time-delta)
	if is_instance_valid(g.folamour_line):
		g.folamour_line.text="Folamour : "+g.loc(g.reaction_text)
		g.folamour_line.visible=g.folamour_comments and g.reaction_time>0
	if g.errors>g.last_observed_errors:
		for threshold in [1,5]:
			if g.last_observed_errors<threshold and g.errors>=threshold:react(g,"error",str(threshold))
		g.last_observed_errors=g.errors
	if is_instance_valid(g.folamour) and g.folamour.visible and g.player.position.distance_to(g.folamour.position)<g.TILE*4:
		react(g,"greeting")
		if g.decorative_motion:
			var model=g.folamour.get_node_or_null("DocteurFolamour")
			if model:
				var distance=g.player.position-g.folamour.position
				if Vector2(distance.x,distance.z).length()>0.5:model.rotation.y=lerp_angle(model.rotation.y,atan2(-distance.x,-distance.z),minf(1,delta*3))
	if g.decorative_motion:
		g.decor_time+=delta
		for actor in g.animated_doctors:
			if not is_instance_valid(actor) or not actor.is_visible_in_tree():continue
			actor.position.y=sin(g.decor_time*1.7)*0.022
			for child in actor.get_children():
				if str(child.name).begins_with("ArmPivot"):
					child.rotation.z=sin(g.decor_time*1.1+float(child.get_meta("side")))*(.18 if g.reaction_time>0 else .055)
static func show(g):
	g.clear_modal("SUJET 16 / ARCHIVES",g.loc("Dossier du sujet 16"))
	g.paragraph(g.loc("Collection totale : %d / 250")%g.dossier.collection.size(),23)
	g.paragraph("Les collectibles sont facultatifs. Ils ne sont jamais dépensés et ne bloquent aucune énigme.",16)
	var summary=g.Guidance.summary(g)
	if not g.won:
		var previous=g.level_stats.get(str(g.level),{})
		summary.puzzles-=int(previous.get("puzzles",0))
		summary.shortcuts-=int(previous.get("shortcuts",0))
		summary.hints-=int(previous.get("hints",0))
		for e in g.events:
			if g.Guidance.is_challenge(e) and g.done.has(e.id):summary.puzzles+=1
		summary.shortcuts+=g.open_shortcuts.size()
		for value in g.hints.values():summary.hints+=int(value)
	g.paragraph(g.loc("Niveaux terminés : %d / 25")%g.level_stats.size(),17)
	g.paragraph(g.loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d")%[summary.puzzles,summary.shortcuts,summary.hints],16)
	g.paragraph("Dossier conservé avec la sauvegarde de cette aventure. Une nouvelle partie le remet à zéro.",14)
	g.modal_box.add_child(g.button("Album des découvertes",func():show_album(g)))
	g.modal_box.add_child(g.button("Observations de Folamour",func():show_observations(g)))
	g.paragraph("Rapport de progression",19)
	for c in range(1,6):
		var total=chapter_count(g,c)
		g.paragraph(g.loc("Chapitre %d : %d / 50")%[c,total],19)
		for n in range((c-1)*5+1,c*5+1):
			var l=n
			if not g.dossier.visited.has(str(l)) and not g.level_stats.has(str(l)):continue
			g.paragraph(g.loc("Niveau %d : %d / 10")%[(l-1)%5+1,count(g,l)]+" · "+g.level_name(l),15)
			if g.level_stats.has(str(l)):
				g.modal_box.add_child(g.button("Rejouer pour compléter la collection",func():confirm_replay(g,l)))
	g.modal_box.add_child(g.button("Retour au bilan" if g.won else "Reprendre",func():g.show_win() if g.won else g.close_modal(),true))
static func confirm_replay(g,level):
	g.clear_modal("SUJET 16",g.loc("Rejouer ce niveau ?"));g.paragraph(g.level_name(level),21)
	g.paragraph("Les énigmes de ce niveau recommenceront. Votre collection et les bilans des niveaux seront conservés. La progression du niveau actuel sera remplacée.")
	g.modal_box.add_child(g.button("Rejouer",func():g.start_game(false,level,true),true))
	g.modal_box.add_child(g.button("Retour",func():show(g)))
static func show_album(g):
	g.clear_modal("SUJET 16",g.loc("Album des découvertes"))
	g.paragraph("Une archive se révèle à 10, 25 et 50 trouvailles dans chaque chapitre.",16)
	for c in range(1,6):
		var entry=DATA.data.chapters[str(c)];var total=chapter_count(g,c)
		g.paragraph(g.loc(entry.name[0]),21)
		g.paragraph(g.loc(entry.collectible[0])+" · "+str(total)+" / 50",17)
		for i in range(3):
			g.paragraph(g.loc(entry.archives[i][0]) if total>=[10,25,50][i] else g.loc("Archive encore scellée.")+" ("+str([10,25,50][i])+")",16)
	if g.dossier.collection.size()==250:g.paragraph("Collection complète : curiosité officiellement excessive.",21)
	g.modal_box.add_child(g.button("Retour",func():show(g),true))
static func show_observations(g):
	g.clear_modal("SUJET 16",g.loc("Observations de Folamour"))
	var unique=[]
	for text in g.dossier.observations.values():
		if not unique.has(text):unique.append(text);g.paragraph("« "+g.loc(text)+" »",18)
	if unique.is_empty():g.paragraph("Aucune observation pour le moment.")
	g.modal_box.add_child(g.button("Retour",func():show(g),true))

static func finish_button(g):
	g.paragraph(g.loc("Souvenirs de ce niveau : %d / 10")%count(g,g.level),17)
	g.modal_box.add_child(g.button("Dossier du sujet 16",func():show(g)))
