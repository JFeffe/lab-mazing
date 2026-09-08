extends RefCounted
static func initial(e):
	return e.initial.map(func(v):return int(v)) if e.puzzle_type=="copier" else [0,0,0] if e.puzzle_type=="overlay" else [0,0,0,0]
static func rotate(values):
	var out=[]
	for y in range(3):
		for x in range(3):out.append(int(values[(2-x)*3+y]))
	return out
static func mirror(values):
	var out=[]
	for y in range(3):
		for x in range(3):out.append(int(values[y*3+2-x]))
	return out
static func layer(e,values,i):
	var out=e.masks[i].duplicate()
	for turn in range(values[i]):out=rotate(out)
	return out
static func composite(e,values):
	var out=[0,0,0,0,0,0,0,0,0]
	for i in range(3):
		var mask=layer(e,values,i)
		for j in range(9):out[j]=int(out[j]==1 or mask[j]==1)
	return out
static func solved(e,values):
	if e.puzzle_type=="filing":
		# Actual version-B constraints, with positions indexed from zero.
		return values.count(0)==1 and values.count(1)==1 and values.count(2)==1 and values.count(3)==1 and values[1]==values[2]+1 and values[0]>values[1] and values[3]==0
	return (composite(e,values) if e.puzzle_type=="overlay" else values)==e.target.map(func(v):return int(v))
static func move(e,values,index):
	if e.puzzle_type=="copier":
		if index not in [0,1]:return
		var out=rotate(values) if index==0 else mirror(values)
		values.assign(out)
	elif index>=0 and index<values.size():values[index]=(values[index]+1)%4
static func board(g,parent,values,size_v=28):
	var center=CenterContainer.new()
	parent.add_child(center)
	var grid=GridContainer.new()
	grid.columns=3
	grid.add_theme_constant_override("h_separation",2)
	grid.add_theme_constant_override("v_separation",2)
	center.add_child(grid)
	for v in values:
		var cell=ColorRect.new()
		cell.color=Color("111827") if int(v)==1 else Color("f1ead8")
		cell.custom_minimum_size=Vector2(size_v,size_v)
		cell.mouse_filter=Control.MOUSE_FILTER_IGNORE
		grid.add_child(cell)
static func render(g,e,values):
	if e.puzzle_type=="filing":
		for i in range(4):
			var name_v=g.loc(["Lune","Miroir","Serre","Zéro"][i])
			g.modal_box.add_child(g.button(g.loc("Casier de %s : %d")%[name_v,values[i]+1],func():g.PuzzleControls.move(g,e,i)))
		return
	g.paragraph("Modèle à reproduire",17)
	board(g,g.modal_box,e.target)
	g.paragraph("Résultat actuel",17)
	board(g,g.modal_box,composite(e,values) if e.puzzle_type=="overlay" else values)
	if e.puzzle_type=="overlay":
		var row=HBoxContainer.new()
		row.add_theme_constant_override("separation",8)
		g.modal_box.add_child(row)
		for i in range(3):
			var col=VBoxContainer.new()
			col.size_flags_horizontal=Control.SIZE_EXPAND_FILL
			row.add_child(col)
			board(g,col,layer(e,values,i),18)
			var b=g.button(g.loc("Calque %s : %d°")%[["A","B","C"][i],values[i]*90],func():g.PuzzleControls.move(g,e,i))
			b.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
			col.add_child(b)
	else:
		g.modal_box.add_child(g.button("Tourner de 90° ↻",func():g.PuzzleControls.move(g,e,0)))
		g.modal_box.add_child(g.button("Miroir gauche-droite ↔",func():g.PuzzleControls.move(g,e,1)))
	g.paragraph("Chaque case noire est marquée. Les cases claires sont vides.",15)
static func sync(g,e,values):
	var root=g.event_nodes[e.id]
	if e.puzzle_type=="filing":
		for i in range(4):
			var file=root.get_node_or_null("File"+str(i))
			if file:file.position.y=.4+values[i]*.28
	else:
		var pixels=composite(e,values) if e.puzzle_type=="overlay" else values
		for i in range(9):
			var pixel=root.get_node_or_null("Pixel"+str(i))
			if pixel:pixel.material_override=g.material(Color("111827") if pixels[i]==1 else Color("f1ead8"))
