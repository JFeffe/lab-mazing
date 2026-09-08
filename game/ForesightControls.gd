extends RefCounted
const PROGRAMS=["courier","ordering","film","duet","echoes"]
const DIRS=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
static func initial(e):
	match e.mode:
		"assay":return [0,1,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1]
		"clocks":return [0,0,0]
		"identity":return [0,0]
		"tanks":return [8,0,0]
		"prevention","audit","logic":return [0,0,0,0,0]
		"cameras","lockers","budget":return [0,0,0,0]
	return [0]
static func program(v):return v.slice(0,v.size()-1)
static func measurement(function,input):
	return input+2 if function==0 else input*2 if function==1 else 6-input
static func coverage(e,v):
	var seen={}
	for i in range(e.cameras.size()):
		var p=Vector2i(e.cameras[i][0],e.cameras[i][1])+DIRS[v[i]]
		while p.x>=0 and p.x<5 and p.y>=0 and p.y<5 and e.board[p.y][p.x]!="#":
			seen[p]=true;p+=DIRS[v[i]]
	return seen
static func walk(board,start,goal,checkpoint,commands,reverse=false):
	var p=Vector2i(start[0],start[1]);var trace=[p];var visited=p==Vector2i(checkpoint[0],checkpoint[1])
	for action in commands:
		var next=p+DIRS[action]*(-1 if reverse else 1)
		if next.x>=0 and next.x<5 and next.y>=0 and next.y<5 and board[next.y][next.x]!="#":p=next
		trace.append(p)
		visited=visited or p==Vector2i(checkpoint[0],checkpoint[1])
	return {"path":trace,"checkpoint":visited,"arrived":p==Vector2i(goal[0],goal[1])}
static func echo_result(e,commands):
	var lamps=0;var queue=[-1,-1];var frames=[]
	for action in commands:
		var old=queue.pop_front()
		if old>=0:
			var mask=int(e.masks[old]);lamps^=((mask<<1)&63)|(mask>>5)
		if action<3:lamps^=int(e.masks[action])
		queue.append(action if action<3 else -1)
		frames.append(lamps)
	return {"ok":lamps==63 and queue==[-1,-1],"frames":frames,"lamps":lamps,"pending":int(queue[0]>=0)+int(queue[1]>=0)}
static func result(e,v):
	var mode=e.mode
	if mode in ["ordering","film"]:return {"ok":program(v)==e.sequence.map(func(x):return int(x))}
	if mode=="echoes":return echo_result(e,program(v))
	if mode in ["courier","duet"]:
		var a=walk(e.board,e.start,e.goal,e.checkpoint,program(v));var answer={"ok":a.arrived and a.checkpoint,"a":a}
		if mode=="duet":
			var b=walk(e.board_b,e.start_b,e.goal_b,e.checkpoint_b,program(v),true)
			answer.b=b;answer.ok=answer.ok and b.arrived and b.checkpoint
		return answer
	if mode=="cameras":
		var seen=coverage(e,v);var count=0
		for p in e.targets:
			if seen.has(Vector2i(p[0],p[1])):count+=1
		return {"ok":count==e.targets.size(),"count":count}
	if mode=="prevention":return {"ok":v[0]==1 and v[1]==0 and v[2]==1 and v[3]==0}
	if mode=="logic":
		var claims=[v[1]==0,v[2]==1 and v[3]==1,v[0]==1,v[0]==0 and v[2]==0];var ok=v.slice(0,4).count(1)==2
		for i in range(4):ok=ok and (v[i]==1)==claims[i]
		return {"ok":ok}
	return {"ok":false}
static func solved(e,v):
	match e.mode:
		"assay":return v[2]==7 and v.slice(3,6)==[1,2,0]
		"lockers":return v==[3,2,1,0]
		"clocks":
			for i in range(3):
				if (v[i]+int(e.readings[i]))%12!=0:return false
			return true
		"identity":return v[0]==2 and v[1]==7
		"budget":return v==[3,2,4,3]
		"tanks":return v.slice(0,3)==[4,4,0]
		"audit":return v==[1,0,0,0,1]
	return v.back()==1 and result(e,v).ok
static func move(e,v,index):
	var mode=e.mode
	if mode in PROGRAMS:
		if index==98:v[v.size()-1]=1
		elif index==99:
			if v.size()>1:v.remove_at(v.size()-2)
			v[v.size()-1]=0
		elif index>=0 and index<(e.cards.size() if e.has("cards") else 4) and v.size()-1<int(e.max_commands):
			if e.has("cards") and index in program(v):return
			v.insert(v.size()-1,index);v[v.size()-1]=0
	elif mode=="assay":
		if index in [0,1]:v[index]=(v[index]+1)%3
		elif index==2:
			v[6+v[0]*3+v[1]]=measurement(int(e.functions[v[0]]),v[1]+1)
			if v[1]!=1:v[2]|=1<<v[0]
		elif index in [3,4,5]:v[index]=(v[index]+1)%3
	elif mode=="lockers":
		if index in range(4):v[index]=(v[index]+1)%4
	elif mode=="clocks":
		if index in range(3):v[index]=(v[index]+1)%12
		elif index in range(100,103):v[index-100]=(v[index-100]+11)%12
	elif mode=="identity":
		if index in range(4):v[0]=index
		elif index in range(4,7):v[1]|=1<<(index-4)
	elif mode=="budget":
		var used=0
		for x in v:used+=x
		if index in range(4) and used<int(e.budget):v[index]+=1
		elif index in range(100,104) and v[index-100]>0:v[index-100]-=1
	elif mode=="tanks":
		if index==99 and v.size()>3:
			var previous=v.slice(v.size()-3);v.resize(v.size()-3)
			for i in range(3):v[i]=previous[i]
		elif index in range(6):
			var pair=[[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]][index];var a=pair[0];var b=pair[1]
			var amount=mini(v[a],int(e.capacities[b])-v[b])
			if amount>0:
				# The newest three values are the previous tank state.
				var old=v.slice(0,3);v[a]-=amount;v[b]+=amount;v.append_array(old)
	else:
		var count=3 if mode=="cameras" else 5 if mode=="audit" else 4
		if index==98 and mode!="audit":v[v.size()-1]=1
		elif index in range(count):
			v[index]=(v[index]+1)%(4 if mode=="cameras" else 2)
			if mode!="audit":v[v.size()-1]=0
static func ready_button(g,text,callback):
	var b=g.button("",callback);b.text=text;b.remove_meta("source_text");return b
static func add(g,e,text,index,parent=null):
	var b=ready_button(g,text,func():g.PuzzleControls.move(g,e,index));b.set_meta("foresight_action",index)
	(parent if parent else g.modal_box).add_child(b);return b
static func number_row(g,e,title,index):
	g.paragraph_ready(title,18)
	var row=HBoxContainer.new();row.add_theme_constant_override("separation",10);g.modal_box.add_child(row)
	for action in [index+100,index]:
		var b=add(g,e,"−" if action>=100 else "+",action,row);b.size_flags_horizontal=Control.SIZE_EXPAND_FILL
static func board(g,e,v,second=false):
	var view=preload("res://ForesightView.gd").new();view.event=e;view.values=v.duplicate();view.second=second
	view.custom_minimum_size=Vector2(0,250);g.modal_box.add_child(view)
static func render(g,e,v):
	var mode=e.mode
	if mode in PROGRAMS:
		if e.has("board"):
			g.paragraph("D : départ · S : sortie · * : station · Nord en haut",15)
			board(g,e,v)
			if mode=="duet":board(g,e,v,true)
		var labels=e.cards if e.has("cards") else ["I","II","III","ATTENDRE"] if mode=="echoes" else ["NORD","EST","SUD","OUEST"]
		var names=[]
		for action in program(v):names.append(g.loc(labels[action]))
		g.paragraph_ready(g.loc("Programme : %s")%(" → ".join(names) if not names.is_empty() else g.loc("vide")),17)
		g.paragraph_ready(g.loc("Ordres : %d / %d")%[v.size()-1,int(e.max_commands)],15)
		for i in range(labels.size()):
			var b=add(g,e,g.loc(labels[i]),i)
			b.disabled=v.size()-1>=int(e.max_commands) or (e.has("cards") and i in program(v))
		add(g,e,g.loc("Retirer le dernier ordre"),99).disabled=v.size()==1
		add(g,e,g.loc("Tester la simulation"),98)
		if v.back()==1:
			var r=result(e,v)
			if mode in ["duet","courier"]:
				for key in (["a","b"] if mode=="duet" else ["a"]):g.paragraph_ready(g.loc("Équipe %s : arrivée %s · station %s")%[key.to_upper(),g.loc("OUI" if r[key].arrived else "NON"),g.loc("OUI" if r[key].checkpoint else "NON")],17)
			if mode=="echoes":
				board(g,e,v)
				for i in range(r.frames.size()):
					var bits=[]
					for bit in range(6):bits.append("1" if r.frames[i]&(1<<bit) else "0")
					g.paragraph_ready(g.loc("Tour %d : %s")%[i+1,"  ".join(bits)],16)
				g.paragraph_ready(g.loc("Échos en attente : %d")%r.pending,16)
			g.paragraph("Conforme" if r.ok else "Non conforme",18)
		else:g.paragraph("Essai à refaire après modification.",15)
	elif mode=="assay":
		add(g,e,g.loc("Appareil : %s")%["A","B","C"][v[0]],0)
		add(g,e,g.loc("Entrée : %d")%(v[1]+1),1)
		add(g,e,g.loc("Mesurer"),2)
		var count=0
		for device in range(3):
			for input in range(3):
				if v[6+device*3+input]>=0:
					count+=1;g.paragraph_ready(g.loc("Mesure %s : %d → %d")%[["A","B","C"][device],input+1,v[6+device*3+input]],16)
		if count==0:g.paragraph("Aucune mesure enregistrée.",16)
		for i in range(3):add(g,e,g.loc("%s : fonction %s")%[["A","B","C"][i],g.loc(["Ajouter deux","Doubler","Complément à six"][v[i+3]])],i+3)
	elif mode=="lockers":
		for slot in range(4):
			var held=[]
			for i in range(4):
				if v[i]==slot:held.append(g.loc(e.labels[i]))
			g.paragraph_ready(g.loc("Casier %d : %s")%[slot+1," / ".join(held) if not held.is_empty() else "—"],17)
		for i in range(4):add(g,e,g.loc("%s : casier %d")%[g.loc(e.labels[i]),v[i]+1],i)
	elif mode=="clocks":
		for i in range(3):number_row(g,e,g.loc("Décalage %s : %d · cadran %d")%[["A","B","C"][i],v[i],(v[i]+int(e.readings[i]))%12],i)
	elif mode=="identity":
		for i in range(3):
			add(g,e,g.loc("Lire : %s")%g.loc(["Matière","Vêtement","Badge"][i]),4+i)
			if v[1]&(1<<i):
				for who in range(4):g.paragraph_ready(g.loc(e.people[who])+" : "+g.loc(e.observations[i][who]),16)
		for i in range(4):add(g,e,("✓ " if v[0]==i else "")+g.loc("Choix : %s")%g.loc(e.people[i]),i)
	elif mode in ["budget","tanks"]:
		var caps=e.capacities if mode=="tanks" else [e.budget,e.budget,e.budget,e.budget]
		var labels=["A","B","C"] if mode=="tanks" else e.labels
		board(g,e,v)
		if mode=="budget":
			var used=0
			for x in v:used+=x
			g.paragraph_ready(g.loc("Réserve : %d / %d")%[int(e.budget)-used,int(e.budget)],18)
		for i in range(labels.size()):
			var title=g.loc("%s : %d / %d")%[g.loc(labels[i]),v[i],int(caps[i])]
			if mode=="budget":number_row(g,e,title,i)
			else:g.paragraph_ready(title,18)
		if mode=="tanks":
			for i in range(6):add(g,e,["A → B","A → C","B → A","B → C","C → A","C → B"][i],i)
			add(g,e,g.loc("Annuler le transvasement"),99).disabled=v.size()==3
	else:
		if mode=="cameras":
			board(g,e,v)
			for i in range(3):add(g,e,["A","B","C"][i]+" : "+g.loc(["NORD","EST","SUD","OUEST"][v[i]]),i)
		elif mode=="logic":
			for i in range(4):
				g.paragraph(e.statements[i],17)
				add(g,e,["A","B","C","D"][i]+" : "+g.loc("VRAI" if v[i]==1 else "FAUX"),i)
		else:
			if mode=="audit":board(g,e,v)
			for i in range(e.labels.size()):add(g,e,g.loc(e.labels[i])+" : "+g.loc(("Conserver" if v[i]==1 else "Écarter") if mode=="audit" else ("OUI" if v[i]==1 else "NON")),i)
		if mode!="audit":
			add(g,e,g.loc("Tester la simulation"),98)
			if v.back()==1:
				if mode=="cameras":g.paragraph_ready(g.loc("Cibles couvertes : %d / %d")%[result(e,v).count,e.targets.size()],18)
				if mode=="prevention":
					var checks=[v[0]==1,v[2]==1,v[0]==1 and v[3]==0,v[1]==0]
					for i in range(4):g.paragraph_ready(g.loc(["Alimentation de secours : %s","Vanne protégée : %s","Ventilation maintenue : %s","Alerte audible : %s"][i])%g.loc("OUI" if checks[i] else "NON"),17)
				g.paragraph("Conforme" if result(e,v).ok else "Non conforme",18)
			else:g.paragraph("Essai à refaire après modification.",15)
static func sync(g,e,v):
	preload("res://ForesightDecor.gd").sync(g,e,v)
