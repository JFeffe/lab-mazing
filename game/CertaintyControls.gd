extends RefCounted
const UI=preload("res://ForesightControls.gd")
const PROGRAMS=["splice","assembly"]
const NETWORKS=["tubes","conveyor","trust"]
static func initial(e):
	if e.mode in PROGRAMS:return [0]
	if e.mode in ["badges","routine"]:return [0]
	if e.mode=="gaze":return [0,0,0,0]
	if e.mode=="energy":return [0,0,0]
	if e.mode=="seal":return [0,0,0,0] # positions bitmask, seal side, cost, selection; undo frames follow
	var v=[]
	for i in range(e.edges.size() if e.mode in NETWORKS else e.choices.size()):v.append(0)
	if e.mode in NETWORKS:v.append(0)
	return v
static func program(v):return v.slice(0,v.size()-1)
static func chain(e,v,start):
	var node=start;var seen=[];var trace=[]
	while node<e.edges.size():
		trace.append(node)
		if node in seen:return {"end":-1,"trace":trace,"reason":"Boucle détectée"}
		seen.append(node);node=int(e.edges[node][v[node]])
	trace.append(node)
	return {"end":node,"trace":trace,"reason":""}
static func result(e,v):
	if e.mode in ["tubes","trust"]:
		var traces=[];var ok=true
		var starts=e.starts if e.mode=="tubes" else range(e.edges.size())
		for i in range(starts.size()):
			var r=chain(e,v,int(starts[i]));traces.append(r)
			ok=ok and r.end==int(e.goals[i])
			if e.mode=="tubes":ok=ok and int(e.via[i]) in r.trace
		return {"ok":ok,"traces":traces}
	if e.mode=="conveyor":
		var node=0;var stage=0;var seen=[];var trace=[];var reason=""
		while node!=6:
			var state=Vector2i(node,stage);trace.append(node)
			if state in seen:reason="Boucle détectée";break
			seen.append(state)
			if e.stations.has(str(node)):
				if int(e.stations[str(node)])!=stage:reason="Opération hors ordre";break
				stage+=1
			if node<3:node=int(e.edges[node][v[node]])
			elif e.fixed.has(str(node)):node=int(e.fixed[str(node)])
			else:reason="Trajet interrompu";break
		trace.append(node)
		return {"ok":node==6 and stage==3 and reason=="","traces":[{"trace":trace,"reason":reason}]}
	if e.mode=="splice":
		var node=0;var ok=program(v).size()==e.joins.size();var trace=[node]
		for i in program(v):
			if int(e.joins[i][0])!=node:ok=false
			node=int(e.joins[i][1]);trace.append(node)
		return {"ok":ok and node==4,"reason":"Raccord impossible"}
	if e.mode=="assembly":
		var seen=[];var ok=program(v).size()==e.cards.size()
		for i in program(v):
			for dep in e.dependencies[i]:
				if int(dep) not in seen:ok=false
			seen.append(i)
		return {"ok":ok,"reason":"Dépendance manquante"}
	if e.mode=="gaze":
		var ok=true
		for gate in e.world_gates:ok=ok and v[int(gate.channel)] in gate.allowed.map(func(x):return int(x))
		return {"ok":ok}
	return {"ok":false}
static func solved(g,e,v):
	if e.has("observations"):
		for id in e.observations:
			if not g.done.has(id):return false
	match e.mode:
		"badges":return v[0]==2
		"routine":return v[0]==1
		"energy":return v[0]+v[1]==5 and v[1]+v[2]==4 and v[0]+v[2]==3
		"seal":return v[0]==15 and v[1]==1 and v[2]<=int(e.budget)
	if e.has("target"):return v==e.target.map(func(x):return int(x))
	return v.back()==1 and result(e,v).ok
static func can_move(g,e):
	if not e.has("world_gates"):return true
	var center=Vector2(e.cell[0],e.cell[1])*g.TILE
	return Vector2(g.player.position.x,g.player.position.z).distance_to(center)<1.8*g.TILE
static func move(e,v,index):
	if e.mode in PROGRAMS:
		if index==98:v[v.size()-1]=1
		elif index==99:
			if v.size()>1:v.remove_at(v.size()-2)
			v[v.size()-1]=0
		elif index in range(e.cards.size()) and index not in program(v) and v.size()-1<int(e.max_commands):
			v.insert(v.size()-1,index);v[v.size()-1]=0
	elif e.mode in ["badges","routine"]:
		if index in range(3):v[0]=index
	elif e.mode=="gaze":
		if index==98:v[3]=1
		elif index in range(3):v[index]=(v[index]+1)%4;v[3]=0
	elif e.mode in NETWORKS:
		if index==98:v[v.size()-1]=1
		elif index in range(e.edges.size()):v[index]=1-v[index];v[v.size()-1]=0
	elif e.mode=="energy":
		if index in range(3) and v[0]+v[1]+v[2]<int(e.budget):v[index]+=1
		elif index in range(100,103) and v[index-100]>0:v[index-100]-=1
	elif e.mode=="seal":
		if index in range(4):
			if int(bool(v[0]&(1<<index)))==v[1]:v[3]^=1<<index
		elif index==98:
			var count=0;var cost=0;var legal=true
			for i in range(4):
				if v[3]&(1<<i):
					count+=1;cost=maxi(cost,int(e.times[i]));legal=legal and int(bool(v[0]&(1<<i)))==v[1]
			if count in [1,2] and legal:
				var old=v.slice(0,3);v[0]^=v[3];v[1]=1-v[1];v[2]+=cost;v[3]=0;v.append_array(old)
		elif index==99 and v.size()>4:
			var old=v.slice(v.size()-3);v.resize(v.size()-3)
			for i in range(3):v[i]=old[i]
			v[3]=0
	elif index in range(e.choices.size()):v[index]=(v[index]+1)%e.choices[index].size()
static func add(g,e,text,index,parent=null):
	var b=UI.ready_button(g,text,func():g.PuzzleControls.move(g,e,index));b.set_meta("certainty_action",index)
	(parent if parent else g.modal_box).add_child(b);return b
static func view(g,e,v):
	var panel=preload("res://CertaintyView.gd").new();panel.event=e;panel.values=v.duplicate();panel.game=g
	panel.custom_minimum_size=Vector2(0,245 if e.mode!="trust" else 290);g.modal_box.add_child(panel)
static func render(g,e,v):
	if e.has("observations"):
		var count=0
		for id in e.observations:
			if g.done.has(id):count+=1
		g.paragraph_ready(g.loc("Registres consultés : %d / 3")%count,18)
	if e.mode in ["badges","routine","gaze"]:
		view(g,e,v)
		if e.mode=="gaze":
			for i in range(3):add(g,e,["A","B","C"][i]+" : "+g.loc(["NORD","EST","SUD","OUEST"][v[i]]),i)
			add(g,e,g.loc("Tester la simulation"),98)
		else:
			for i in range(3):add(g,e,("✓ " if v[0]==i else "")+g.loc(e.labels[i]),i)
		for gate in e.world_gates:g.paragraph_ready(g.loc("Porte %s : %s")%[gate.label,g.loc("OUVERT" if v[int(gate.channel)] in gate.allowed.map(func(x):return int(x)) or g.done.has(e.id) else "FERMÉ")],16)
	elif e.mode in NETWORKS:
		view(g,e,v)
		g.paragraph("Réseau : sorties 0 / 1",17)
		for i in range(e.edges.size()):
			g.paragraph_ready(e.names[i]+" : 0 → "+e.names[int(e.edges[i][0])]+" / 1 → "+e.names[int(e.edges[i][1])],16)
			add(g,e,e.names[i]+" → "+e.names[int(e.edges[i][v[i]])]+"  ["+str(v[i])+"]",i)
		if e.mode=="conveyor":g.paragraph_ready("D → 1  /  M → 2  /  R → 3  /  C → S",16)
		add(g,e,g.loc("Tester les trajets"),98)
		if v.back()==1:
			for r in result(e,v).traces:
				var names=[]
				for node in r.trace:names.append(e.names[int(node)])
				g.paragraph_ready(" → ".join(names),17)
				if r.reason!="":g.paragraph(r.reason,16)
	elif e.mode in PROGRAMS:
		var names=[]
		for i in program(v):names.append(g.loc(e.cards[i]))
		g.paragraph_ready(g.loc("Programme : %s")%(" → ".join(names) if names.size()>0 else g.loc("vide")),17)
		for i in range(e.cards.size()):add(g,e,g.loc(e.cards[i]),i).disabled=i in program(v)
		add(g,e,g.loc("Retirer le dernier ordre"),99).disabled=v.size()==1
		add(g,e,g.loc("Tester la simulation"),98)
		if v.back()==1 and not result(e,v).ok:g.paragraph(result(e,v).reason,17)
	elif e.mode=="energy":
		view(g,e,v)
		g.paragraph_ready(g.loc("Réserve : %d / %d")%[int(e.budget)-v[0]-v[1]-v[2],int(e.budget)],18)
		for i in range(3):
			g.paragraph_ready(["A","B","C"][i]+" : "+str(v[i]),18)
			var row=HBoxContainer.new();row.add_theme_constant_override("separation",10);g.modal_box.add_child(row)
			for action in [100+i,i]:add(g,e,"−" if action>=100 else "+",action,row).size_flags_horizontal=Control.SIZE_EXPAND_FILL
		g.paragraph_ready(g.loc("Presse : %d / 5")%(v[0]+v[1]),17)
		g.paragraph_ready(g.loc("Refroidissement : %d / 4")%(v[1]+v[2]),17)
		g.paragraph_ready(g.loc("Guidage : %d / 3")%(v[0]+v[2]),17)
	elif e.mode=="seal":
		view(g,e,v)
		g.paragraph_ready(g.loc("Temps utilisé : %d / %d")%[v[2],int(e.budget)],18)
		g.paragraph_ready(g.loc("Sceau : %s")%g.loc("Côté bureaux" if v[1]==0 else "Côté conseil"),17)
		for i in range(4):
			var here=int(bool(v[0]&(1<<i)))==v[1]
			add(g,e,("✓ " if v[3]&(1<<i) else "")+["A","B","C","D"][i]+" · "+str(int(e.times[i]))+" · "+g.loc("Côté conseil" if v[0]&(1<<i) else "Côté bureaux"),i).disabled=not here
		var selected=0
		for i in range(4):
			if v[3]&(1<<i):selected+=1
		add(g,e,g.loc("Traverser"),98).disabled=selected not in [1,2]
		add(g,e,g.loc("Annuler la traversée"),99).disabled=v.size()==4
		if v[2]>int(e.budget):g.paragraph("Budget dépassé : annuler une traversée ou réinitialiser.",17)
	else:
		for i in range(e.choices.size()):add(g,e,g.loc(e.labels[i])+" : "+g.loc(e.choices[i][v[i]]),i)
	if e.mode in NETWORKS+PROGRAMS+["gaze"]:
		g.paragraph("Essai à refaire après modification." if v.back()==0 else "Conforme" if result(e,v).ok else "Non conforme",17)
static func sync(g,e,v):
	preload("res://CertaintyDecor.gd").sync(g,e,v)
