extends RefCounted
const NAMES=["Aster","Boréal","Cobalt","Delta","Écho","Fermi"]
const TOPICS=["Ouverture","Démonstration","Rapport","Vote"]
const SIGNALS=["Caméra","Micro","Archives vidéo","Projecteur","Écrans","Amplificateur"]
static func initial(e):return [0,0,0,0,0,0] if e.puzzle_type=="seating" else [0,0,0,0,0] if e.puzzle_type=="conference" else [0,0,0,0]
static func neighbours(a,b):return (a-b+6)%6 in [1,5]
static func signal_route(values,start):
	var route=[start]
	while route.back()<4:
		var next=[3,2,4,5][values[route.back()]]
		if next in route:return route+[next,-1]
		route.append(next)
	return route
static func solved(e,v):
	if e.puzzle_type=="seating":
		var unique={}
		for seat in v:unique[seat]=true
		return unique.size()==6 and v[0]==0 and v[1]==3 and v[3]==(v[0]+1)%6 and v[4]==(v[3]+3)%6 and neighbours(v[5],v[1]) and not neighbours(v[5],v[4]) and not neighbours(v[2],v[3])
	if e.puzzle_type=="schedule":
		var occupied={}
		for i in range(4):
			for slot in range(v[i],v[i]+int(e.durations[i])):
				if slot>5 or occupied.has(slot):return false
				occupied[slot]=true
		return occupied.size()==6 and v[0]==0 and v[3]==5 and v[2]+int(e.durations[2])<=v[1]
	var unique={}
	for i in range(4):unique[v[i]]=true
	return v[4]==1 and unique.size()==4 and signal_route(v,0)==[0,2,3,4] and signal_route(v,1)==[1,5]
static func move(e,v,index):
	if e.puzzle_type=="conference":
		if index in range(4):v[index]=(v[index]+1)%4;v[4]=0
		elif index==4:v[4]=1
	elif index>=0 and index<v.size():v[index]=(v[index]+1)%6
static func ready_button(g,text,callback):
	var b=g.button("",callback);b.text=text;b.remove_meta("source_text");return b
static func time_label(slot):return "09:%02d"%(slot*10)
static func route_text(g,v,start):
	var names=[]
	for node in signal_route(v,start):names.append(g.loc("Boucle détectée") if node==-1 else g.loc(SIGNALS[node]))
	return " → ".join(names)
static func render(g,e,v):
	if e.puzzle_type=="seating":
		var board=preload("res://MeetingSeatingView.gd").new()
		board.custom_minimum_size=Vector2(0,220)
		for seat in range(6):
			var guests=[]
			for i in range(6):
				if v[i]==seat:guests.append(g.loc(NAMES[i]))
			board.labels.append(str(seat+1)+"\n"+(" / ".join(guests) if not guests.is_empty() else "—"))
		g.modal_box.add_child(board)
		g.paragraph("PORTE / places dans le sens horaire",15)
		for i in range(6):g.modal_box.add_child(ready_button(g,g.loc("Invité %s : place %d")%[g.loc(NAMES[i]),v[i]+1],func():g.PuzzleControls.move(g,e,i)))
	elif e.puzzle_type=="schedule":
		for slot in range(6):
			var topics=[]
			for i in range(4):
				if slot>=v[i] and slot<v[i]+int(e.durations[i]):topics.append(g.loc(TOPICS[i]))
			g.paragraph_ready(time_label(slot)+" • "+(" / ".join(topics) if not topics.is_empty() else g.loc("Libre")),15)
		for i in range(4):g.modal_box.add_child(ready_button(g,g.loc("%s : %s (%d min)")%[g.loc(TOPICS[i]),time_label(v[i]),int(e.durations[i])*10],func():g.PuzzleControls.move(g,e,i)))
		for i in range(4):
			if v[i]+int(e.durations[i])>6:g.paragraph("Hors séance : une intervention dépasse 10 h 00.",15);break
	else:
		for i in range(4):g.modal_box.add_child(ready_button(g,g.loc("%s → entrée %s")%[g.loc(SIGNALS[i]),["A","B","C","D"][v[i]]],func():g.PuzzleControls.move(g,e,i)))
		g.modal_box.add_child(g.button("Tester la conférence",func():g.PuzzleControls.move(g,e,4)))
		if v[4]==1:
			g.paragraph_ready(g.loc("Image : %s")%route_text(g,v,0),17)
			g.paragraph_ready(g.loc("Son : %s")%route_text(g,v,1),17)
		else:g.paragraph("Branchements modifiés : relancez le test.",16)
static func sync(g,e,v):
	var root=g.event_nodes[e.id]
	if e.puzzle_type=="conference":
		for i in range(6):
			var face=root.get_node_or_null("ScreenFace"+str(i))
			if face:face.visible=g.won
		var indicator=root.get_node_or_null("ConferenceSignal")
		if indicator:indicator.material_override=g.material(Color("8adeb2") if g.done.has(e.id) else Color("705657"))
	# Completed preparations light up separate indicators inside the meeting room.
	if g.event_nodes.has("r_conference"):
		var room=g.event_nodes.r_conference
		for i in range(2):
			var light=room.get_node_or_null("Preparation"+str(i))
			if light:light.material_override=g.material(Color("8adeb2") if g.done.has(["r_seating","r_schedule"][i]) else Color("705657"))
