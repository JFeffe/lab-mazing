extends RefCounted
const TYPES=["stacks","reports","twin"]
const DIRECTIONS=["OUEST","CENTRE","EST"]
static func initial(e):
	return [0,0,0] if e.puzzle_type=="stacks" else [0,0,0,0] if e.puzzle_type=="reports" else [0,2,3,1,0]
static func solved(e,v):
	if e.puzzle_type=="stacks":return v==[2,0,1]
	if e.puzzle_type=="reports":return v==[1,1,1,2]
	return v==[1,0,1,0,1]
static func matches(v):
	var count=0
	for i in range(4):
		if v[i]==[1,0,1,0][i]:count+=1
	return count
static func can_move(g,e):
	if e.puzzle_type!="stacks":return true
	# A journal or resumed panel must never move shelving through the player.
	return not (g.player.position.x>12*g.TILE and g.player.position.x<22*g.TILE and g.player.position.z<12*g.TILE)
static func move(e,v,index):
	if e.puzzle_type=="stacks":
		if index in range(3):
			for row in [[0,1],[1,2],[0,2]][index]:v[row]=(v[row]+1)%3
	elif e.puzzle_type=="reports":
		if index in range(4):v[index]=(v[index]+1)%3
	else:
		if index in range(4):v[index]=(v[index]+1)%[2,3,4,2][index];v[4]=0
		elif index==4:v[4]=1
static func ready_button(g,text,callback):
	var b=g.button("",callback);b.text=text;b.remove_meta("source_text");return b
static func render(g,e,v):
	if e.puzzle_type=="stacks":
		var plan=preload("res://ArchivePlanView.gd").new()
		plan.values=v.duplicate();plan.custom_minimum_size=Vector2(0,170)
		g.modal_box.add_child(plan)
		for i in range(3):g.paragraph_ready(g.loc("Rangée %s : ouverture %s")%[["A","B","C"][i],g.loc(DIRECTIONS[v[i]])],17)
		for i in range(3):g.modal_box.add_child(g.button(["Commande I : A + B","Commande II : B + C","Commande III : A + C"][i],func():g.PuzzleControls.move(g,e,i)))
	elif e.puzzle_type=="reports":
		for t in ["Rapport A : Boréal, 14 h 27, bobine de cuivre.","Rapport B : Boréal, 14 h 17, bobine de cuivre.","Rapport C : Cobalt, 14 h 17, prisme de verre."]:g.paragraph(t,17)
		var labels=["Rapport sélectionné : %s","Registre : %s","Horloge : %s","Objet : %s"]
		var options=[["A","B","C"],["Cobalt","Boréal","Aster"],["14:27","14:17","14:07"],["Prisme de verre","Disque","Bobine de cuivre"]]
		for i in range(4):g.modal_box.add_child(ready_button(g,g.loc(labels[i])%g.loc(options[i][v[i]]),func():g.PuzzleControls.move(g,e,i)))
	else:
		var labels=["Lampe : %s","Bobine : socle %s","Projecteur : %s","Ventilation : %s"]
		var options=[["ÉTEINT","ALLUMÉ"],["GAUCHE","CENTRE","DROITE"],["NORD","EST","SUD","OUEST"],["ABAISSÉ","LEVÉ"]]
		for i in range(4):g.modal_box.add_child(ready_button(g,g.loc(labels[i])%g.loc(options[i][v[i]]),func():g.PuzzleControls.move(g,e,i)))
		g.modal_box.add_child(g.button("Tester la copie",func():g.PuzzleControls.move(g,e,4)))
		if v[4]==1:g.paragraph_ready(g.loc("Correspondances : %d / 4")%matches(v),18)
		else:g.paragraph("Réglages modifiés : test requis.",16)
static func sync(g,e,v):
	if e.puzzle_type=="stacks":preload("res://ArchiveDecor.gd").sync_stacks(g,v)
	if e.puzzle_type=="twin":preload("res://ArchiveDecor.gd").sync_room(g,v)
