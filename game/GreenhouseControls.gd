extends RefCounted
const DIRS=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
static func initial(e):
	return [0,0,0,0] if e.puzzle_type in ["pipes","blend"] else [0,0,0]
static func ports(turn):return [turn%4,(turn+1)%4]
static func flowing(values):
	# Follow actual port connectivity from the inlet, rejecting leaks and cycles.
	var cell=Vector2i(0,0)
	var incoming=3
	var visited=[]
	while true:
		var i=cell.y*2+cell.x
		if i in visited or incoming not in ports(values[i]):return []
		visited.append(i)
		var p=ports(values[i])
		var outgoing=p[1] if p[0]==incoming else p[0]
		if i==1 and outgoing==1:return visited if visited.size()==4 else []
		cell+=DIRS[outgoing]
		if cell.x<0 or cell.x>1 or cell.y<0 or cell.y>1:return []
		incoming=(outgoing+2)%4
static func totals(e,values):
	var result=[0,0,0]
	for i in range(4):
		for j in range(3):result[j]+=values[i]*int(e.properties[i][j])
	return result
static func solved(e,values):
	if e.puzzle_type=="pipes":return flowing(values).size()==4
	if e.puzzle_type=="growth":return values==[1,2,1]
	return values.reduce(func(a,b):return a+b,0)==3 and totals(e,values)==e.target.map(func(v):return int(v))
static func move(e,values,index):
	if index<0 or index>=values.size():return
	values[index]=(values[index]+1)%(4 if e.puzzle_type=="pipes" else 2 if e.puzzle_type=="growth" and index==2 else 3)
static func render(g,e,values):
	if e.puzzle_type=="pipes":
		g.paragraph("Entrée : ouest de A. Sortie : est de B.\nA et B en haut ; C et D en bas.",17)
		var board=GridContainer.new()
		board.columns=2
		g.modal_box.add_child(board)
		for i in range(4):
			var p=ports(values[i])
			var names=["NORD","EST","SUD","OUEST"]
			var b=g.button(["A","B","C","D"][i]+"\n"+["↑","→","↓","←"][p[0]]+" "+names[p[0]]+"\n"+["↑","→","↓","←"][p[1]]+" "+names[p[1]],func():g.PuzzleControls.move(g,e,i))
			b.size_flags_horizontal=Control.SIZE_EXPAND_FILL
			b.custom_minimum_size.y=100
			board.add_child(b)
		g.paragraph("Touchez un coude pour le tourner d’un quart de tour.",16)
	elif e.puzzle_type=="growth":
		var labels=["Lumière : "+["OMBRE","DOUCE","FORTE"][values[0]],g.loc("Arrosage : %d / 2 doses")%values[1],"Treillis : "+("DÉPLOYÉ" if values[2]==1 else "REPLIÉ")]
		for i in range(3):g.modal_box.add_child(g.button(labels[i],func():g.PuzzleControls.move(g,e,i)))
		g.paragraph("Touchez chaque réglage pour le modifier. La croissance est validée seulement lorsque les trois conditions sont réunies.",16)
	else:
		var sum_v=totals(e,values)
		g.paragraph(g.loc("Arôme : %d / 3 • Amertume : %d / 2 • Stabilité : %d / 2")%sum_v,18)
		g.paragraph(g.loc("Mesures utilisées : %d / 3")%values.reduce(func(a,b):return a+b,0),18)
		for i in range(4):
			g.modal_box.add_child(g.button(e.ingredients[i]+" : "+str(values[i])+" / 2",func():g.PuzzleControls.move(g,e,i)))
		g.paragraph("Chaque pression ajoute une mesure ; après deux, la quantité revient à zéro. Les réserves restent installées.",16)
static func sync(g,e,values):
	var root=g.event_nodes[e.id]
	if e.puzzle_type=="pipes":
		for i in range(4):
			var part=root.get_node_or_null("Pipe"+str(i))
			if part:part.rotation.y=values[i]*PI/2
	elif e.puzzle_type=="growth":
		var plant=root.get_node_or_null("Plant")
		if plant:plant.scale=Vector3.ONE*(1.5 if g.done.has(e.id) else .45)
	else:
		for i in range(4):
			var liquid=root.get_node_or_null("Ingredient"+str(i))
			if liquid:liquid.scale.y=.12+values[i]*.35
