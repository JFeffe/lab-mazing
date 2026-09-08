extends RefCounted
const Decor=preload("res://FinaleDecor.gd")
static func stage(g):
	var count=0
	for i in range(1,4):
		if g.done.has("c%d_p%d"%[g.level,i]):count+=1
	return count
static func status(g):
	if g.level==24:return ["HORIZON · Étape 3 / 3 · Autorisations actives","HORIZON · Étape 2 / 3 · Reprises automatiques","HORIZON · Étape 1 / 3 · Arrêt à transmettre","HORIZON · Étape 0 / 3 · Immobilisé"][stage(g)]
	if g.level==25:return ["MIROIR · Réexamen des certitudes","MIROIR · Hypothèses séparées des faits","MIROIR · Incertitude reconnue","MIROIR · Arrêt confirmé · Sorties ouvertes"][stage(g)]
	return ["HORIZON · Inspection à blanc","HORIZON · Menace présumée","HORIZON · Responsabilité en débat"][g.level-21]
static func intro(g):
	var entry=g.chapter5_data[str(g.level)]
	g.clear_modal("CHAPITRE 5 / PROGRAMME HORIZON",g.level_name(g.level))
	g.folamour_portrait();g.paragraph(entry.intro,20);g.paragraph(entry.layout,17)
	if g.level==24:g.paragraph("Annonce : « L’annulation de l’urgence nécessite le maintien de l’urgence. »",18)
	g.modal_box.add_child(g.button("Accepter la mission",func():
		g.done["c%d_met"%g.level]=true;g.add_journal("intro",entry.intro+"\n\n"+entry.layout);g.close_modal(),true))
static func checkpoint(g,e):
	if g.level!=24 or not e.has("puzzle_type"):return
	var line=["Annonce : « L’annulation de l’urgence nécessite le maintien de l’urgence. »","Annonce : « Les copies sont suspendues. Merci de ne pas les remplacer par vos impressions. »","Annonce : « Le secours du secours ne répond plus. Le service y voit un signe encourageant. »","Annonce : « Arrêt confirmé. L’immobilité sera maintenue jusqu’à nouvel avis des personnes concernées. »"][stage(g)]
	g.add_journal("horizon_stage_"+str(stage(g)),line)
	g.clear_modal("HORIZON",status(g));g.paragraph(line,20);g.paragraph(e.success,18)
	g.modal_box.add_child(g.button("Reprendre",g.close_modal,true))
static func finish(g):
	var entry=g.chapter5_data[str(g.level)]
	g.clear_modal("CHAPITRE 5 / MISSION TERMINÉE",g.level_name(g.level))
	if g.level!=25:g.folamour_portrait()
	g.paragraph(entry.outro,20)
	var stat=g.level_stats[str(g.level)]
	g.paragraph(g.loc("Temps du niveau : %02d:%02d\nSecrets : %d / 3    •    Tentatives incorrectes : %d")%[int(g.elapsed)/60,int(g.elapsed)%60,stat.secrets,g.errors],18)
	g.paragraph(g.loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d")%[stat.puzzles,stat.shortcuts,stat.hints],17)
	if g.level<25:
		var target=g.level+1
		g.modal_box.add_child(g.button("Continuer la mission suivante",func():g.start_game(false,target,true),true))
	else:
		var count=0;var secrets=0;var elapsed=0.0
		for n in range(21,26):
			if g.level_stats.has(str(n)):count+=1;secrets+=g.level_stats[str(n)].secrets;elapsed+=g.level_stats[str(n)].time
		g.paragraph("CHAPITRE 5 TERMINÉ",22)
		g.paragraph(g.loc("Bilan : %d niveau(x) terminé(s), %02d:%02d d’exploration, %d secrets.")%[count,int(elapsed)/60,int(elapsed)%60,secrets],17)
		g.paragraph("L’AVENTURE EST TERMINÉE",23)
		g.paragraph("Cinq chapitres, vingt-cinq niveaux. Le laboratoire a enfin une sortie.",18)
		g.paragraph("« "+g.loc("Vous quittez une zone entièrement sécurisée. Bonne chance avec le reste.")+" »",20)
		g.modal_box.add_child(g.button("Regarder la surface",func():Decor.surface(g);g.close_modal(),true))
	g.modal_box.add_child(g.button("Choisir un chapitre",func():g.playing=false;g.hud.hide();g.show_chapters()))
	g.modal_box.add_child(g.button("Sauvegarder et revenir au menu",g.show_title))
