extends RefCounted
static func intro(g):
	var entry=g.chapter4_data[str(g.level)]
	g.clear_modal("CHAPITRE 4 / LE COMPLEXE DE LA CERTITUDE",g.level_name(g.level))
	g.folamour_portrait()
	g.paragraph(entry.intro,20)
	g.paragraph(entry.layout,17)
	g.modal_box.add_child(g.button("Accepter la mission",func():
		g.done["c%d_met"%g.level]=true
		g.add_journal("intro",entry.layout)
		g.close_modal(),true))
static func finish(g):
	preload("res://CertaintyDecor.gd").finish(g)
	var entry=g.chapter4_data[str(g.level)]
	g.clear_modal("CHAPITRE 4 / MISSION TERMINÉE",g.level_name(g.level))
	g.folamour_portrait()
	g.paragraph(entry.outro,20)
	var stat=g.level_stats[str(g.level)]
	g.paragraph(g.loc("Temps du niveau : %02d:%02d\nSecrets : %d / 3    •    Tentatives incorrectes : %d")%[int(g.elapsed)/60,int(g.elapsed)%60,stat.secrets,g.errors],19)
	g.paragraph(g.loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d")%[stat.puzzles,stat.shortcuts,stat.hints],17)
	if g.level<20:
		var target=g.level+1
		g.modal_box.add_child(g.button("Continuer la mission suivante",func():g.start_game(false,target,true),true))
	else:
		var count=0;var secrets=0;var elapsed=0.0
		for n in range(16,21):
			if g.level_stats.has(str(n)):
				count+=1;secrets+=g.level_stats[str(n)].secrets;elapsed+=g.level_stats[str(n)].time
		g.paragraph("CHAPITRE 4 TERMINÉ",22)
		g.paragraph(g.loc("Bilan : %d niveau(x) terminé(s), %02d:%02d d’exploration, %d secrets.")%[count,int(elapsed)/60,int(elapsed)%60,secrets],17)
		g.modal_box.add_child(g.button("Entrer dans le programme HORIZON",func():g.start_game(false,21,true),true))
	g.modal_box.add_child(g.button("Choisir un chapitre",func():g.playing=false;g.hud.hide();g.show_chapters()))
	g.modal_box.add_child(g.button("Sauvegarder et revenir au menu",g.show_title))
