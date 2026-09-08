extends RefCounted
const UI=preload("res://ForesightControls.gd")
const PROGRAMS=["courier","chronology","redaction","protocol"]
const TESTED=["courier","chronology","redaction","protocol","feedback","policy","damping"]
const DIRS=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
static func initial(e):
	if e.mode in PROGRAMS:return [0]
	if e.mode=="gantry":return e.initial.map(func(x):return int(x))
	if e.mode=="dialogue":return [0,0]
	if e.mode=="damping":return [int(e.initial_mask),0]
	var v=[]
	for i in range(e.edges.size() if e.mode=="feedback" else e.choices.size()):v.append(0)
	if e.mode in ["feedback","policy"]:v.append(0)
	return v
static func program(v):return v.slice(0,v.size()-1)
static func walk(board,start,goal,checkpoint,commands,mirror=false):
	var p=Vector2i(start[0],start[1]);var trace=[p];var visited=p==Vector2i(checkpoint[0],checkpoint[1]);var safe=true
	for action in commands:
		var d=DIRS[action]
		if mirror:d.x=-d.x
		var next=p+d
		if next.y>=0 and next.y<board.size() and next.x>=0 and next.x<board[0].length() and board[next.y][next.x]!="#":p=next
		trace.append(p);visited=visited or p==Vector2i(checkpoint[0],checkpoint[1]);safe=safe and board[p.y][p.x]!="X"
	return {"trace":trace,"ok":visited and safe and p==Vector2i(goal[0],goal[1]),"safe":safe,"visited":visited}
static func result(e,v):
	if e.mode=="courier":
		var paths=[];var ok=true
		for i in range(e.boards.size()):
			var p=walk(e.boards[i],e.starts[i],e.goals[i],e.checkpoints[i],program(v),i==1);paths.append(p);ok=ok and p.ok
		return {"ok":ok,"paths":paths}
	if e.mode in ["chronology","redaction"]:return {"ok":program(v)==e.sequence.map(func(x):return int(x))}
	if e.mode=="protocol":
		var seen=[]
		for i in program(v):
			for d in e.dependencies[i]:
				if int(d) not in seen:return {"ok":false,"count":seen.size(),"reason":"Une condition manque avant cette opération."}
			seen.append(i)
		return {"ok":seen.size()==e.cards.size(),"count":seen.size(),"reason":""}
	if e.mode=="feedback":
		var degrees=[];var cuts=0
		for i in range(e.names.size()):degrees.append(0)
		for i in range(e.edges.size()):
			if v[i]==1:
				cuts+=1
				if i in e.protected.map(func(x):return int(x)):return {"ok":false,"reason":"Un lien protégé a été suspendu."}
			else:degrees[int(e.edges[i][1])]+=1
		var queue=[];var processed=0
		for i in range(degrees.size()):
			if degrees[i]==0:queue.append(i)
		while not queue.is_empty():
			var node=queue.pop_front();processed+=1
			for i in range(e.edges.size()):
				if v[i]==0 and int(e.edges[i][0])==node:
					var dest=int(e.edges[i][1]);degrees[dest]-=1
					if degrees[dest]==0:queue.append(dest)
		return {"ok":processed==degrees.size() and cuts==int(e.max_cuts),"reason":"Une boucle se cite elle-même." if processed<degrees.size() else ""}
	if e.mode=="policy":
		var mask=31
		for i in range(3):mask&=int(e.clause_masks[i][v[i]])
		return {"ok":mask==int(e.expected),"mask":mask}
	if e.mode=="damping":return {"ok":v[0]==int(e.goal_mask)}
	if e.mode=="manifest":
		var totals=[0,0,0];var left=0
		for i in range(e.weights.size()):
			if v[i]==0:left+=1
			else:totals[v[i]-1]+=int(e.weights[i])
		return {"ok":left==0 and totals==e.capacities.map(func(x):return int(x)) and v[2]==1 and v[0]==v[3] and v[4]==3,"totals":totals,"left":left}
	return {"ok":false}
static func solved(g,e,v):
	for id in e.get("observations",[]):
		if not g.done.has(id):return false
	match e.mode:
		"gantry":return v==[0,0,0]
		"manifest":return result(e,v).ok
		"offsets":return v[1]-2==-1 and v[0]-v[1]==3 and v[0]-v[2]==1
		"quorum":return v.count(1)==3 and v[4]==1 and (v[0]==0 or v[2]==1) and (v[2]==0 or v[0]==1) and (v[1]==0 or v[3]==1) and not (v[3]==1 and v[4]==1)
		"epistemic":return v==e.target.map(func(x):return int(x))
		"intervals":
			for i in range(e.ranges.size()):
				var a=e.ranges[i][0];var b=e.ranges[i][1]
				if v[2*i]!=maxi(int(a[0]),int(b[0])) or v[2*i+1]!=mini(int(a[1]),int(b[1])):return false
			return true
		"dialogue":return v[0]==3
	return v.back()==1 and result(e,v).ok
static func can_move(g,e):
	if not e.has("world_gates"):return true
	return Vector2(g.player.position.x,g.player.position.z).distance_to(Vector2(e.cell[0],e.cell[1])*g.TILE)<1.8*g.TILE
static func move(e,v,index):
	if e.mode in PROGRAMS:
		if index==98:v[v.size()-1]=1
		elif index==99:
			if v.size()>1:v.remove_at(v.size()-2)
			v[v.size()-1]=0
		elif index>=0 and index<(4 if e.mode=="courier" else e.cards.size()) and v.size()-1<int(e.max_commands):
			if e.mode!="courier" and index in program(v):return
			v.insert(v.size()-1,index);v[v.size()-1]=0
	elif e.mode=="gantry":
		var control=index-100 if index>=100 else index
		if control in range(3):
			for i in range(3):v[i]=posmod(v[i]+int(e.masks[control][i])*(-1 if index>=100 else 1),3)
	elif e.mode=="dialogue":
		if index==99:v[0]=maxi(0,v[0]-1);v[1]=0
		elif v[0]<3 and index in range(3):
			if index==int(e.correct[v[0]]):v[0]+=1;v[1]=0
			else:v[1]=1
	elif e.mode=="damping":
		if index==98:v[1]=1
		elif index in range(e.masks.size()):v[0]^=int(e.masks[index]);v[1]=0
	elif e.mode=="feedback":
		if index==98:v[v.size()-1]=1
		elif index in range(e.edges.size()):v[index]=1-v[index];v[v.size()-1]=0
	else:
		if e.mode=="policy" and index==98:v[v.size()-1]=1
		elif index in range(e.choices.size()):
			v[index]=(v[index]+1)%e.choices[index].size()
			if e.mode=="policy":v[v.size()-1]=0
static func add(g,e,text,index,parent=null):
	var b=UI.ready_button(g,text,func():g.PuzzleControls.move(g,e,index));b.set_meta("finale_action",index)
	(parent if parent else g.modal_box).add_child(b);return b
static func view(g,e,v):
	var panel=preload("res://FinaleView.gd").new();panel.game=g;panel.event=e;panel.values=v.duplicate()
	panel.custom_minimum_size=Vector2(0,255 if e.mode=="courier" else 165);g.modal_box.add_child(panel)
static func render(g,e,v):
	if e.mode=="gantry":
		view(g,e,v);var count=0
		for id in e.observations:
			if g.done.has(id):count+=1
		g.paragraph_ready(g.loc("Mesures consultées : %d / 3")%count,18)
		for i in range(3):
			g.paragraph_ready(g.loc("Pont %s : cran %d")%['ABC'[i],v[i]],17)
			var row=HBoxContainer.new();row.add_theme_constant_override("separation",10);g.modal_box.add_child(row)
			for action in [100+i,i]:add(g,e,['I','II','III'][i]+(" −" if action>=100 else " +"),action,row).size_flags_horizontal=Control.SIZE_EXPAND_FILL
	elif e.mode=="dialogue":
		for i in range(v[0]):
			g.paragraph_ready(g.loc(e.questions[i]),18);g.paragraph_ready("— "+g.loc(e.answers[i][int(e.correct[i])]),18);g.paragraph_ready(g.loc(e.responses[i]),18)
		if v[0]<3:
			g.paragraph_ready(g.loc("Étape %d / 3")%(v[0]+1),16);g.paragraph_ready(g.loc(e.questions[v[0]]),21)
			for i in range(3):add(g,e,g.loc(e.answers[v[0]][i]),i)
		else:g.paragraph("Le dialogue est terminé. Vous pouvez valider.",18)
		if v[1]==1:g.paragraph("Cette réponse contredit le mandat ou les constats. Folamour attend une autre proposition.",17)
		add(g,e,g.loc("Reprendre la dernière réponse"),99).disabled=v[0]==0
	elif e.mode in PROGRAMS:
		if e.mode=="courier":
			view(g,e,v);g.paragraph("D : départ · * : tampon · R : retour · X : interdit",16)
		var names=[]
		for i in program(v):names.append((g.loc(['NORD','EST','SUD','OUEST'][i]).left(1) if e.mode=="courier" else g.loc(e.cards[i])))
		g.paragraph_ready(g.loc("Programme : %s")%(" → ".join(names) if names else g.loc("vide")),18)
		if e.mode=="courier":
			var row=HBoxContainer.new();g.modal_box.add_child(row)
			for i in range(4):add(g,e,g.loc(['NORD','EST','SUD','OUEST'][i]).left(1),i,row).size_flags_horizontal=Control.SIZE_EXPAND_FILL
		else:
			for i in range(e.cards.size()):add(g,e,g.loc(e.cards[i]),i).disabled=i in program(v)
		add(g,e,g.loc("Retirer le dernier ordre"),99).disabled=v.size()==1
	elif e.mode=="feedback":
		for i in range(e.edges.size()):
			var edge=e.edges[i];add(g,e,g.loc(e.names[int(edge[0])])+" → "+g.loc(e.names[int(edge[1])])+" : "+g.loc("Retenu" if v[i]==0 else "Suspendu"),i)
	elif e.mode=="damping":
		view(g,e,v)
		for i in range(e.masks.size()):
			var names=[]
			for j in range(6):
				if int(e.masks[i])&(1<<j):names.append('ABCDEF'[j])
			add(g,e,['I','II','III','IV'][i]+" : "+" / ".join(names),i)
	else:
		for i in range(e.choices.size()):add(g,e,g.loc(e.labels[i])+" : "+g.loc(e.choices[i][v[i]]),i)
		if e.mode=="manifest":
			var r=result(e,v);g.paragraph_ready(g.loc("Dépôt restant : %d")%r.left,17)
			for i in range(3):g.paragraph_ready(g.loc(e.choices[0][i+1])+" : "+str(r.totals[i])+" / "+str(int(e.capacities[i])),17)
		if e.mode=="intervals":
			for i in range(3):g.paragraph_ready(g.loc(e.labels[2*i]).split(" · ")[0]+" : ["+str(v[2*i])+", "+str(v[2*i+1])+"]",17)
	if e.mode in TESTED:
		add(g,e,g.loc("Tester la procédure"),98)
		if v.back()==0:g.paragraph("La procédure reste à tester.",17)
		else:
			var r=result(e,v);g.paragraph("Procédure conforme" if r.ok else "Procédure à corriger",18)
			if e.mode=="protocol":g.paragraph_ready(g.loc("Étapes exécutées : %d")%r.count,17)
			if r.get("reason","")!="":g.paragraph(r.reason,17)
			if e.mode=="policy":
				for i in range(e.cases.size()):g.paragraph_ready(g.loc(e.cases[i])+" : "+g.loc("AUTORISÉ" if r.mask&(1<<i) else "REFUSÉ"),16)
			if e.mode=="courier":
				for i in range(r.paths.size()):g.paragraph_ready(g.loc("CAPSULE %s")%('AB'[i])+" : "+g.loc("Procédure conforme" if r.paths[i].ok else "Procédure à corriger"),16)
static func sync(g,e,v):preload("res://FinaleDecor.gd").sync(g,e,v)
