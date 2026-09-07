extends RefCounted
# All moves are reversible; partial states live in the normal checkpoint.
static func initial(e):
	match e.puzzle_type:
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
		var messages={"balance":"Répartition refusée : deux masses par plateau, gauche plus lourd de 1 kg. Les masses restent disponibles.","sequence":"Ordre refusé. Vérifiez les trois rapports ; chaque symbole doit apparaître une seule fois.","circuit":"Circuit incomplet : les cinq voyants doivent être allumés simultanément."}
		g.feedback.text=g.loc(messages[e.puzzle_type])
		g.chime(170)
		g.save_game()
static func sync(g,e):
	var values=state(g,e)
	var root=g.event_nodes[e.id]
	if e.puzzle_type=="balance":
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
