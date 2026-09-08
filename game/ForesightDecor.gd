extends RefCounted
static func model(g,root,e,gold,dark):
	g.box(root,Vector3(1.9,.8,1.1),Vector3(0,.4,0),dark)
	var count=6 if e.mode=="echoes" else 4 if e.mode in ["budget","lockers","identity","logic"] else 3
	for i in range(count):
		var part=Node3D.new();part.name="Indicator%d"%i;root.add_child(part)
		part.position=Vector3((i-(count-1)*.5)*1.65/count,1.1,0)
		if e.mode=="tanks":
			g.box(part,Vector3(.38,1.2,.4),Vector3(0,.25,0),dark)
			var fill=g.box(part,Vector3(.28,1,.44),Vector3(0,.25,0),gold);fill.name="Fill"
		elif e.mode in ["cameras","identity"]:
			g.box(part,Vector3(.35,.3,.5),Vector3.ZERO,dark)
			g.box(part,Vector3(.2,.2,.1),Vector3(0,0,-.3),gold)
		elif e.mode=="clocks":
			g.box(part,Vector3(.46,.5,.12),Vector3.ZERO,gold)
			var hand=g.box(part,Vector3(.035,.2,.05),Vector3(0,.1,-.1),dark);hand.name="Hand"
		else:
			var lamp=g.box(part,Vector3(.25,.3,.3),Vector3.ZERO,gold);lamp.name="Lamp"
	if e.mode in ["courier","duet","film","ordering","audit"]:
		for i in range(5):g.box(root,Vector3(.25,.08,.25),Vector3((i-2)*.32,.84,.35),gold)
static func setup(g):
	# Attach props to the tops of existing walls: no invisible obstacles on walkable cells.
	for y in range(2,33,4):
		for x in range(2,33,4):
			if g.grid[y][x]!=0:continue
			var prop=Node3D.new();prop.position=Vector3(x*g.TILE,2.4,y*g.TILE);g.world.add_child(prop)
			var metal=g.material(Color("728e9e"));var light=g.material(Color("b4d9c5"),true)
			match g.level:
				11:
					for i in range(3):g.box(prop,Vector3(.7,.35,.6),Vector3((i%2)*.7,.2+i*.32,0),g.material(Color("ac9376")))
				12:
					for i in range(4):g.box(prop,Vector3(.9,.08,.65),Vector3(i*.03,.12+i*.12,0),g.material(Color("d0c7a3")))
				13:
					g.box(prop,Vector3(.1,.7,.1),Vector3(0,.3,0),metal)
					g.box(prop,Vector3(.7,.35,.8),Vector3(0,.8,0),metal)
					g.box(prop,Vector3(.3,.2,.1),Vector3(0,.8,-.45),light)
				14:
					g.box(prop,Vector3(.5,.4,2),Vector3(0,.2,0),metal)
					for i in [-.6,.6]:g.box(prop,Vector3(.7,.1,.2),Vector3(0,.45,i),light)
				15:
					g.box(prop,Vector3(.18,2,.18),Vector3(0,1,0),metal)
					g.box(prop,Vector3(1.3,.8,.2),Vector3(0,2,0),metal)
					g.box(prop,Vector3(1.05,.55,.05),Vector3(0,2,-.13),light)
			prop.set_meta("fog_cell",g.key(x,y));g.decor.append(prop)
static func sync(g,e,v):
	if not g.event_nodes.has(e.id):return
	var root=g.event_nodes[e.id]
	for i in range(root.get_child_count()):
		var part=root.get_node_or_null("Indicator%d"%i)
		if part==null:continue
		if e.mode=="cameras":part.rotation.y=-v[i]*PI/2
		elif e.mode=="clocks":part.get_node("Hand").rotation.z=-(v[i]+int(e.readings[i]))*TAU/12
		elif e.mode=="tanks":part.get_node("Fill").scale.y=maxf(.03,float(v[i])/int(e.capacities[i]))
		else:
			var lamp=part.get_node_or_null("Lamp")
			if lamp:
				var on=g.done.has(e.id) or (i<v.size() and v[i]>0)
				if e.mode=="echoes":on=bool(preload("res://ForesightControls.gd").echo_result(e,preload("res://ForesightControls.gd").program(v)).lamps&(1<<i))
				lamp.material_override=g.material(Color("a4e4c5") if on else Color("536b7b"),on)
