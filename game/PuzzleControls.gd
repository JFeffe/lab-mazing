extends RefCounted
# All moves are reversible; partial states live in the normal checkpoint.
static func initial(e):
	match e.puzzle_type:
		"jugs": return [0,0]
		"hanoi", "rotors": return [0,0,0]
		"balance": return [0,0,0,0]
		"sequence": return []
		"circuit": return e.initial.map(func(v): return int(v))
	return []
static func state(g,e):
	if not g.puzzle_states.has(e.id): g.puzzle_states[e.id]=initial(e)
	g.puzzle_states[e.id]=g.puzzle_states[e.id].map(func(v): return int(v))
	return g.puzzle_states[e.id]
static func available(g,e):
	if g.done.has(e.id): return false
	if e.has("requires") and not g.done.has("installed_"+e.id): return false
	for id in e.get("prerequisites",[]):
		if not g.done.has(id): return false
	return true
static func solved(g,e):
	var values=state(g,e)
	match e.puzzle_type:
		"jugs": return values[0]==4
		"hanoi": return values==[2,2,2]
		"rotors": return values==e.target.map(func(v): return int(v))
		"balance":
			var left=0
			var right=0
			for i in range(4):
				if values[i]==1: left+=e.weights[i]
				if values[i]==2: right+=e.weights[i]
			return values.count(1)==2 and values.count(2)==2 and left-right==1
		"sequence": return values==e.sequence.map(func(v): return int(v))
		"circuit": return values==[1,1,1,1,1]
	return false
static func render(g,e):
	var values=state(g,e)
	match e.puzzle_type:
		"jugs":
			g.paragraph(g.loc("Grand : %d / 5 L • Petit : %d / 3 L") % values,20)
			var actions=["Remplir le grand", "Remplir le petit", "Vider le grand", "Vider le petit", "Transvaser grand → petit", "Transvaser petit → grand"]
			for i in range(6):g.modal_box.add_child(g.button(actions[i],func(): move(g,e,i)))
		"hanoi":
			for peg in range(3):
				var discs=[]
				for disc in range(2,-1,-1):
					if values[disc]==peg:discs.append(str(disc+1))
				g.paragraph(["A","B","C"][peg]+g.loc(" (bas → haut) : ")+(" / ".join(discs) if not discs.is_empty() else g.loc("vide")),18)
			for i in range(6):
				var pair=[[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]][i]
				var b=g.button(["A","B","C"][pair[0]]+" → "+["A","B","C"][pair[1]],func(): move(g,e,i))
				b.disabled=not legal_transfer(values,pair[0],pair[1])
				g.modal_box.add_child(b)
		"rotors":
			var directions=["NORD","EST","SUD","OUEST"]
			for i in range(3):g.paragraph(["A","B","C"][i]+" : "+g.loc(directions[values[i]]),20)
			for i in range(3):g.modal_box.add_child(g.button(g.loc("Commande ")+["I : A + B","II : B + C","III : A + C"][i],func(): move(g,e,i)))
		"balance":
			var left=0
			var right=0
			for i in range(4):
				if values[i]==1:left+=e.weights[i]
				if values[i]==2:right+=e.weights[i]
			g.paragraph(g.loc("Gauche : %d kg / %d masses\nDroite : %d kg / %d masses") % [left,values.count(1),right,values.count(2)],19)
			g.paragraph("Touchez une masse : réserve → gauche → droite → réserve.",15)
			for i in range(4):
				var place=g.loc(["RÉSERVE","GAUCHE","DROITE"][int(values[i])])
				g.modal_box.add_child(g.button(str(int(e.weights[i]))+" kg : "+place,func(): move(g,e,i)))
		"sequence":
			var names=[]
			for i in values:names.append(g.loc(e.symbols[int(i)]))
			g.paragraph(g.loc("Séquence : ")+(" → ".join(names) if not names.is_empty() else g.loc("vide")),18)
			var grid=GridContainer.new()
			grid.columns=2
			grid.add_theme_constant_override("h_separation",8)
			grid.add_theme_constant_override("v_separation",8)
			g.modal_box.add_child(grid)
			for i in range(e.symbols.size()):
				var b=g.button(e.symbols[i],func(): move(g,e,i))
				b.size_flags_horizontal=Control.SIZE_EXPAND_FILL
				b.disabled=values.has(i)
				grid.add_child(b)
			var undo=g.button("Retirer le dernier symbole",func(): move(g,e,-1))
			undo.disabled=values.is_empty()
			g.modal_box.add_child(undo)
		"circuit":
			var lamps=[]
			for i in range(5):lamps.append(["A","B","C","D","E"][i]+" : "+g.loc("ALLUMÉ" if values[i]==1 else "ÉTEINT"))
			g.paragraph("\n".join(lamps),17)
			for i in range(4):
				var targets=[]
				for j in range(5):
					if e.masks[i][j]==1:targets.append(["A","B","C","D","E"][j])
				g.modal_box.add_child(g.button(g.loc("Levier ")+["I","II","III","IV"][i]+" : "+" + ".join(targets),func(): move(g,e,i)))
	g.modal_box.add_child(g.button("Valider l’essai",func(): submit(g,e),true))
	g.modal_box.add_child(g.button("Réinitialiser cet essai",func(): move(g,e,-2)))
	g.feedback=g.paragraph("",15)
	g.modal_box.add_child(g.button("Consulter le journal",func(): g.show_journal(e)))
static func move(g,e,index):
	if not available(g,e):return
	var values=state(g,e)
	if index==-2:g.puzzle_states[e.id]=initial(e)
	elif e.puzzle_type=="jugs" and index in range(6):
		match index:
			0: values[0]=5
			1: values[1]=3
			2: values[0]=0
			3: values[1]=0
			4:
				var amount=mini(values[0],3-values[1])
				values[0]-=amount
				values[1]+=amount
			5:
				var amount=mini(values[1],5-values[0])
				values[1]-=amount
				values[0]+=amount
	elif e.puzzle_type=="hanoi" and index in range(6):
		var pair=[[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]][index]
		if legal_transfer(values,pair[0],pair[1]):values[values.find(pair[0])]=pair[1]
	elif e.puzzle_type=="rotors" and index in range(3):
		for i in range(3):values[i]=(values[i]+int(e.masks[index][i]))%4
	elif e.puzzle_type=="balance" and index>=0 and index<4: values[index]=(int(values[index])+1)%3
	elif e.puzzle_type=="sequence":
		if index==-1 and not values.is_empty():values.pop_back()
		elif index>=0 and index<e.symbols.size() and not values.has(index):values.append(index)
	elif e.puzzle_type=="circuit" and index>=0 and index<4:
		for i in range(5):values[i]=int(values[i])^int(e.masks[index][i])
	var scroll=g.modal_scroll.scroll_vertical
	g.show_puzzle(e)
	g.modal_scroll.set_deferred("scroll_vertical",scroll)
	g.sync_event(e)
	g.save_game()
static func submit(g,e):
	if not available(g,e):return
	if solved(g,e):g.complete(e)
	else:
		g.errors+=1
		var messages={"jugs":"Dosage refusé : il faut exactement 4 L dans le grand réservoir.","hanoi":"Transfert incomplet : les trois disques doivent être sur C.","rotors":"Instable : visez A vers EST, B vers SUD et C vers OUEST.","balance":"Répartition refusée : deux masses par plateau, gauche plus lourd de 1 kg. Les masses restent disponibles.","sequence":"Ordre refusé. Vérifiez les trois rapports ; chaque symbole doit apparaître une seule fois.","circuit":"Circuit incomplet : les cinq voyants doivent être allumés simultanément."}
		g.feedback.text=g.loc(messages[e.puzzle_type])
		g.chime(170)
		g.save_game()
static func sync(g,e):
	var values=state(g,e)
	var root=g.event_nodes[e.id]
	if e.puzzle_type=="jugs":
		for i in range(2):
			var liquid=root.get_node_or_null("Liquid"+str(i))
			if liquid:
				liquid.scale.y=maxf(0.01,float(values[i])/float([5,3][i]))
				liquid.position.y=0.3+liquid.scale.y*0.5
	elif e.puzzle_type=="hanoi":
		for disc in range(3):
			var part=root.get_node_or_null("Disc"+str(disc))
			var height=0
			for below in range(disc+1,3):
				if values[below]==values[disc]:height+=1
			if part:part.position=Vector3((values[disc]-1)*0.75,0.4+height*0.22,0)
	elif e.puzzle_type=="rotors":
		for i in range(3):
			var rotor=root.get_node_or_null("Rotor"+str(i))
			if rotor:rotor.rotation.y=values[i]*PI/2
	elif e.puzzle_type=="balance":
		var difference=0
		for i in range(4):
			if values[i]==1:difference+=e.weights[i]
			if values[i]==2:difference-=e.weights[i]
		var beam=root.get_node_or_null("BalanceBeam")
		if beam:
			beam.rotation.z=clampf(float(difference)*0.035,-0.22,0.22)
			var slots=[0,0,0]
			for i in range(4):
				var weight=root.get_node_or_null("PlacedWeight"+str(i))
				if not weight:continue
				weight.visible=g.done.has("installed_"+e.id)
				var side=int(values[i])
				if side==0:weight.position=Vector3((i-1.5)*0.3,0.33,0.35)
				else:
					weight.position=beam.position+beam.basis*Vector3(-0.7 if side==1 else 0.7,-0.33,(-0.15+slots[side]*0.3))
					slots[side]+=1
	elif e.puzzle_type=="circuit":
		for i in range(5):
			var lamp=root.get_node_or_null("CircuitLamp"+str(i))
			if lamp:lamp.material_override=g.material(Color("83e7ac") if values[i]==1 else Color("30444e"),values[i]==1)

static func legal_transfer(values,source,destination):
	var disc=values.find(source)
	var top=values.find(destination)
	return disc!=-1 and (top==-1 or disc<top)
