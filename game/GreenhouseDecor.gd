extends RefCounted
static func plant(g,root,pos,size=1.0):
	var p=Node3D.new()
	p.position=pos
	p.scale=Vector3.ONE*size
	root.add_child(p)
	var green=g.material(Color("619f64"))
	g.box(p,Vector3(.12,1.2,.12),Vector3(0,.7,0),green)
	for i in range(5):
		var leaf=g.box(p,Vector3(.65,.10,.26),Vector3((-.23 if i%2 else .23),.3+i*.2,0),green)
		leaf.rotation.z=-.35 if i%2 else .35
	return p
static func model(g,root,e,gold,dark):
	g.box(root,Vector3(1.9,.2,1.3),Vector3(0,.45,0),dark)
	if e.model=="growth":
		g.box(root,Vector3(1.2,.4,.8),Vector3(0,.7,0),g.material(Color("b48666")))
		var p=plant(g,root,Vector3(0,.85,0))
		p.name="Plant"
		for x in [-.7,.7]:g.box(root,Vector3(.07,1.6,.07),Vector3(x,1.2,.25),gold)
	elif e.model=="pipes":
		for i in range(4):
			var p=Node3D.new()
			p.name="Pipe"+str(i)
			p.position=Vector3((i%2-.5)*.8,.65,(i/2-.5)*.6)
			root.add_child(p)
			g.box(p,Vector3(.14,.14,.45),Vector3(0,0,-.16),gold)
			g.box(p,Vector3(.45,.14,.14),Vector3(.16,0,0),gold)
	else:
		for i in range(4):
			var v=g.box(root,Vector3(.27,.9,.4),Vector3((i-1.5)*.4,1,0),g.material([Color("93684a"),Color("cca8df"),Color("7fba72"),Color("c4e3d2")][i]))
			v.name="Ingredient"+str(i)
static func decorate(g):
	var glass=StandardMaterial3D.new()
	glass.albedo_color=Color(.37,.7,.61,.28)
	glass.transparency=BaseMaterial3D.TRANSPARENCY_ALPHA
	glass.roughness=.25
	var frame=g.material(Color("476d60"))
	for k in g.walls:
		var root=g.walls[k]
		root.get_child(0).material_override=glass
		for x in [-1.2,1.2]:g.box(root,Vector3(.10,2.25,.12),Vector3(x,1.1,0),frame)
		if int(k.split(",")[0])%4==0 and int(k.split(",")[1])%3==0:
			plant(g,root,Vector3(0,.1,0),.8)
	var bridge=g.event_nodes.g_bridge
	var vines=Node3D.new()
	vines.name="LivingBridge"
	bridge.add_child(vines)
	for i in range(7):
		g.box(vines,Vector3(.22,.12,2.15),Vector3((i-3)*.34,.08,0),g.material(Color("78aa69")))
	vines.visible=false
	bridge.get_node("Leaf").material_override=g.material(Color("466956"))
