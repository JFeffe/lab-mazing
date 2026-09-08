extends RefCounted

static func translated(game, pair):
	return pair[1] if game.localization.language=="en" else pair[0]

static func hint_steps(game,e):
	var authored=game.guidance_data.hints.get(e.id,[])
	if not authored.is_empty():
		return authored.map(func(pair):return translated(game,pair))
	var sources=[]
	if e.has("controlled_by"): sources.append(e.controlled_by)
	sources.append_array(e.get("prerequisites",[]))
	for item in e.get("requires",[]):
		for source in game.events:
			if source.get("resource","")==item or source.get("grants",{}).has(item):
				if not sources.has(source.id):sources.append(source.id)
	var names=[]
	for id in sources:
		for source in game.events:
			if source.id==id:names.append(str(source.get("ref",""))+" — "+game.loc(source.title))
	return [game.loc("Comparez les pièces demandées avec les descriptions du sac et du journal."),game.loc("Un objet assemblé provient d’un établi ou d’une autre expérience. Les portes commandées à distance n’ont pas de code."),game.loc("Étapes à consulter :")+"\n"+"\n".join(names)]

static func objective(game):
	if game.won:return game.loc("Niveau terminé. Le bilan permet de poursuivre ou de revenir au menu.")
	var lines=[]
	if game.level==5 and not game.done.has("f_assembly"):
		if not game.done.has("f_dosing"):lines.append(translated(game,game.guidance_data.objectives.f_dosing))
		if not game.done.has("f_tower"):lines.append(translated(game,game.guidance_data.objectives.f_tower))
		if not lines.is_empty():return "\n\n".join(lines)
	var stages=game.guidance_data.stages[str(game.level)]
	for stage in stages:
		var complete=true
		for id in stage[0]:
			if not game.done.has(id):complete=false
		if not complete:
			for e in game.events:
				if e.id==stage[1] and game.LevelEndings.is_doctor(e):return game.loc(e.objective)
			return translated(game,game.guidance_data.objectives[stage[1]])
	return game.loc("Rejoignez la sortie du niveau pour valider votre réussite.")

static func is_challenge(e):
	return e.has("answer") or e.has("puzzle_type") or e.kind=="craft" or (e.kind=="mechanism" and e.has("requires")) or (e.kind=="door" and e.has("requires"))

static func summary(game):
	var result={"time":0.0,"puzzles":0,"shortcuts":0,"hints":0,"levels":game.level_stats.size(),"tracked":0}
	for stat in game.level_stats.values():
		result.time+=float(stat.get("time",0))
		result.hints+=int(stat.get("hints",0))
		if stat.has("puzzles") and stat.has("shortcuts"):
			result.tracked+=1
			result.puzzles+=int(stat.puzzles)
			result.shortcuts+=int(stat.shortcuts)
	return result
