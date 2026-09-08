extends RefCounted
static func model(g,root,e,gold,dark):
	g.box(root,Vector3(1.9,.8,1.15),Vector3(0,.4,0),dark)
	for i in range(3):
		var dial=g.box(root,Vector3(.4,.3,.4),Vector3((i-1)*.58,1.02,0),gold);dial.name="Dial%d"%i
	g.box(root,Vector3(1.8,.08,.2),Vector3(0,.9,-.5),gold)
static func setup(g):
	for e in g.events:
		for i in range(e.get("world_gates",[]).size()):
			var gate=e.world_gates[i];var node=Node3D.new();node.name="Access%d"%i
			node.position=Vector3(gate.cell[0]*g.TILE,0,gate.cell[1]*g.TILE);g.world.add_child(node)
			g.box(node,Vector3(g.TILE-.1,1.8,g.TILE-.1),Vector3(0,.9,0),g.material(Color("8c7770")))
			var body=StaticBody3D.new();body.collision_layer=1;node.add_child(body)
			var collider=CollisionShape3D.new();var shape=BoxShape3D.new();shape.size=Vector3(g.TILE,2,g.TILE);collider.shape=shape;collider.position.y=1;body.add_child(collider)
			node.set_meta("body",body);node.set_meta("fog_cell",g.key(gate.cell[0],gate.cell[1]));g.decor.append(node)
			g.machine_parts["certainty_gate%d"%i]=node
	# Distinct silhouettes mounted on existing walls; no added floor collision.
	for y in range(2,33,5):
		for x in range(2,33,5):
			if g.grid[y][x]!=0:continue
			var prop=Node3D.new();prop.position=Vector3(x*g.TILE,2.1,y*g.TILE);g.world.add_child(prop)
			var dark=g.material(Color("455667"));var accent=g.material([Color("d3b481"),Color("9bc9a1"),Color("99c7da"),Color("d59b70"),Color("bca4cc")][g.level-16])
			match g.level:
				16:
					for i in range(3):g.box(prop,Vector3(.3,.3,1.8),Vector3(i*.45,0,0),accent)
				17:
					g.box(prop,Vector3(1.5,1.2,1.1),Vector3(0,.6,0),dark)
					var shutter=g.box(prop,Vector3(.8,.7,.06),Vector3(0,.8,-.6),accent);shutter.name="Shutter"
				18:
					g.box(prop,Vector3(.1,1.2,.1),Vector3(0,.6,0),dark)
					g.box(prop,Vector3(.65,.4,.8),Vector3(0,1.2,0),accent)
				19:
					g.box(prop,Vector3(2.4,.2,.9),Vector3(0,.2,0),dark)
					for i in range(5):g.box(prop,Vector3(.25,.16,.9),Vector3((i-2)*.4,.4,0),accent)
				20:
					g.box(prop,Vector3(.3,2,.3),Vector3(0,1,0),dark)
					g.box(prop,Vector3(1.2,.8,.15),Vector3(0,2,0),accent)
			prop.set_meta("fog_cell",g.key(x,y));g.decor.append(prop)
	if g.level==17:
		for i in range(3):
			var resident=g.make_folamour(g.world);resident.name="Resident%d"%i;resident.scale=Vector3.ONE*.75
			resident.position=Vector3(13*g.TILE,0,[5,17,29][i]*g.TILE);resident.set_meta("fog_cell",g.key(13,[5,17,29][i]));g.decor.append(resident)
	if g.level==20:
		for pos in [Vector2i(17,7),Vector2i(5,7),Vector2i(5,27),Vector2i(29,7)]:
			var copy=g.make_folamour(g.world);copy.position=Vector3(pos.x*g.TILE,0,pos.y*g.TILE);copy.set_meta("fog_cell",g.key(pos.x,pos.y));g.decor.append(copy)
		# Huge stylised silhouettes beyond the walls. Revealed at chapter completion.
		var hangar=Node3D.new();hangar.name="Horizon";g.world.add_child(hangar);g.machine_parts.horizon=hangar;hangar.visible=false
		for x in [10,17,24]:
			var silo=Node3D.new();silo.position=Vector3(x*g.TILE,0,-5*g.TILE);hangar.add_child(silo)
			g.box(silo,Vector3(3,12,3),Vector3(0,6,0),g.material(Color("bbc6c4")))
			var cone=CylinderMesh.new();cone.top_radius=0;cone.bottom_radius=2;cone.height=4
			var tip=MeshInstance3D.new();tip.mesh=cone;tip.position.y=14;tip.material_override=g.material(Color("bbc6c4"));silo.add_child(tip)
static func sync(g,e,v):
	if e.has("world_gates"):
		g.archive_blocks.clear()
		for i in range(e.world_gates.size()):
			var gate=e.world_gates[i];var active=not g.done.has(e.id) and v[int(gate.channel)] not in gate.allowed.map(func(x):return int(x))
			var node=g.machine_parts.get("certainty_gate%d"%i)
			if not is_instance_valid(node):continue
			node.set_meta("archive_active",active);node.visible=active and g.render_near(node);node.get_meta("body").collision_layer=1 if active else 0
			if active:g.archive_blocks[g.key(gate.cell[0],gate.cell[1])]=true
		if e.mode=="routine":
			for prop in g.decor:
				var shutter=prop.get_node_or_null("Shutter")
				if shutter:shutter.rotation.y=[0,PI*.5,PI*.15][v[0]]
				if prop.name.begins_with("Resident"):
					var i=int(str(prop.name).trim_prefix("Resident"));prop.rotation.y=(v[0]-i)*PI*.5
	if g.event_nodes.has(e.id):
		var root=g.event_nodes[e.id]
		for i in range(3):
			var dial=root.get_node_or_null("Dial%d"%i)
			if dial:
				dial.rotation.y=(v[i] if i<v.size() else 0)*PI*.5
				dial.material_override=g.material(Color("9cddbc") if g.done.has(e.id) else Color("cead78"))
static func finish(g):
	if g.level==20 and g.machine_parts.has("horizon"):
		g.machine_parts.horizon.visible=true
		g.camera.position=Vector3(17*g.TILE,31,-22*g.TILE);g.camera.look_at(Vector3(17*g.TILE,7,-5*g.TILE))
