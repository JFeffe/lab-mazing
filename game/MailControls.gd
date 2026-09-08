extends RefCounted
static func ready_button(g,text,callback):
	var b=g.button("",callback)
	b.text=text
	b.remove_meta("source_text")
	return b
static func initial(e):
	return [0,0,0,0,0,0,0,2] if e.puzzle_type=="parcels" else [0,0,0,0] if e.puzzle_type=="mailnet" else [0,0,0]
static func weight_result(e,values):
	var difference=0
	for i in range(6):
		var weight=11 if i==int(e.heavy) else 10
		if values[i]==1:difference+=weight
		elif values[i]==2:difference-=weight
	return signi(difference)
static func trace(values):
	var route=[0,1]
	if values[0]==0:return route+[2]
	route.append(3)
	if values[1]==1:return route+[4]
	route.append(5)
	return route+[7 if values[2]==1 else 6]
static func solved(e,values):
	if e.puzzle_type=="parcels":return values[6]==int(e.heavy)
	if e.puzzle_type=="mailnet":return values[3]==1 and trace(values).back()==7
	return values==e.target.map(func(v):return int(v))
static func move(e,values,index):
	if e.puzzle_type=="parcels":
		if index in range(6):values[index]=(values[index]+1)%3;values[7]=3
		elif index==6:values[7]=weight_result(e,values)
		elif index==7:values[6]=(values[6]+1)%6
	elif e.puzzle_type=="mailnet":
		if index in range(3):values[index]=1-values[index];values[3]=0
		elif index==3:values[3]=1
	elif index in range(3):values[index]=(values[index]+1)%(4 if index==2 else 3)
static func render(g,e,values):
	if e.puzzle_type=="parcels":
		var grid=GridContainer.new()
		grid.columns=2
		g.modal_box.add_child(grid)
		for i in range(6):
			var place=g.loc(["RÉSERVE","GAUCHE","DROITE"][values[i]])
			var b=ready_button(g,g.loc("Colis %s : %s")%[["A","B","C","D","E","F"][i],place],func():g.PuzzleControls.move(g,e,i))
			b.size_flags_horizontal=Control.SIZE_EXPAND_FILL
			grid.add_child(b)
		g.modal_box.add_child(g.button("Peser les colis",func():g.PuzzleControls.move(g,e,6)))
		var result="Dernière pesée : gauche plus lourd." if values[7]==1 else "Dernière pesée : droite plus lourd." if values[7]==-1 else "Dernière pesée : équilibre." if values[7]==0 else "Aucune pesée effectuée." if values[7]==2 else "Placement modifié : pesez à nouveau."
		g.paragraph(result,18)
		g.modal_box.add_child(ready_button(g,g.loc("Colis choisi : %s")%["A","B","C","D","E","F"][values[6]],func():g.PuzzleControls.move(g,e,7)))
	elif e.puzzle_type=="mailnet":
		var view=preload("res://MailNetworkView.gd").new()
		view.custom_minimum_size=Vector2(0,285)
		view.names=[g.loc("DÉPART CAPSULE"),"A",g.loc("RETOUR"),"B",g.loc("RETOUR"),"C",g.loc("RETOUR"),g.loc("EXPÉDITION")]
		view.path=trace(values) if values[3]==1 else []
		g.modal_box.add_child(view)
		for i in range(3):g.modal_box.add_child(ready_button(g,g.loc("Aiguillage %s : branche %d")%[["A","B","C"][i],values[i]+1],func():g.PuzzleControls.move(g,e,i)))
		g.modal_box.add_child(g.button("Lancer la capsule",func():g.PuzzleControls.move(g,e,3)))
		g.paragraph("La capsule est prête au départ." if values[3]==0 else "Essai réussi : la capsule atteint EXPÉDITION. Validez." if trace(values).back()==7 else "Mauvaise destination : la capsule revient au départ.",17)
	else:
		var labels=[g.loc("Destinataire : %s")%g.loc(["Mme Faraday","Dr Folamour","M. Foucault"][values[0]]),g.loc("Aile : %s")%g.loc(["NORD","EST","OUEST"][values[1]]),g.loc("Bureau : %d")%(values[2]+1)]
		for i in range(3):g.modal_box.add_child(ready_button(g,labels[i],func():g.PuzzleControls.move(g,e,i)))
static func sync(g,e,values):
	var root=g.event_nodes[e.id]
	if e.puzzle_type=="parcels":
		var beam=root.get_node_or_null("MailBeam")
		if beam:beam.rotation.z=-.12*values[7] if abs(values[7])<=1 else 0
		for i in range(6):
			var parcel=root.get_node_or_null("Parcel"+str(i))
			if parcel:
				var place=values[i]
				parcel.position=Vector3((i-2.5)*.26,.22,.72) if place==0 else Vector3(-.6 if place==1 else .6,.9,(i%3-1)*.25)
