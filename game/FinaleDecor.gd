extends RefCounted
static func model(g,root,e,gold,dark):
	if e.mode=="dialogue":
		g.box(root,Vector3(2.2,.15,1.1),Vector3(0,.9,0),g.material(Color("8a6851")))
		for x in [-.85,.85]:g.box(root,Vector3(.12,.9,.8),Vector3(x,.43,0),dark)
		g.box(root,Vector3(.6,.03,.4),Vector3(-.3,1,0),g.material(Color("f0e7cd")))
		var cup=CylinderMesh.new();cup.top_radius=.12;cup.bottom_radius=.1;cup.height=.23
		var mesh=MeshInstance3D.new();mesh.mesh=cup;mesh.position=Vector3(.65,1.08,0);mesh.material_override=g.material(Color("d8d5c9"));root.add_child(mesh)
	else:
		g.box(root,Vector3(1.9,.7,1.1),Vector3(0,.35,0),dark)
		for i in range(3):
			var panel=g.box(root,Vector3(.43,.28,.12),Vector3((i-1)*.54,.94,-.25),gold);panel.name="Dial%d"%i
		g.box(root,Vector3(1.7,.13,.9),Vector3(0,.78,0),gold)
static func prop(g,cell):
	var root=Node3D.new();root.position=Vector3(cell.x*g.TILE,0,cell.y*g.TILE);root.set_meta("fog_cell",g.key(cell.x,cell.y));g.world.add_child(root);g.decor.append(root);return root
static func sign_on(g,root,text,height=2):
	var label=Label3D.new();label.text=g.loc(text);label.font_size=42;label.pixel_size=.012;label.position.y=height;label.billboard=BaseMaterial3D.BILLBOARD_ENABLED;label.modulate=Color("ead5a8");label.no_depth_test=false;root.add_child(label)
static func rocket(g,cell,title):
	var root=prop(g,cell);root.set_meta("horizon_tall",true)
	var steel=g.material(Color("b7c8c5"));var dark=g.material(Color("354b5b"));var brass=g.material(Color("d8ad72"))
	g.box(root,Vector3(3,1,3),Vector3(0,.5,0),dark)
	var mesh=CylinderMesh.new();mesh.height=8;mesh.top_radius=1;mesh.bottom_radius=1;mesh.radial_segments=12
	var body=MeshInstance3D.new();body.mesh=mesh;body.position.y=5;body.material_override=steel;root.add_child(body)
	var cone=CylinderMesh.new();cone.height=3;cone.top_radius=0;cone.bottom_radius=1;cone.radial_segments=12
	var tip=MeshInstance3D.new();tip.mesh=cone;tip.position.y=10.5;tip.material_override=steel;root.add_child(tip)
	for h in [2.3,6.8]:g.box(root,Vector3(2.15,.25,2.15),Vector3(0,h,0),brass)
	for x in [-1.2,1.2]:g.box(root,Vector3(.16,10,.2),Vector3(x,5,.4),dark)
	sign_on(g,root,title,12.5);return root
static func setup(g):
	g.folamour=g.make_folamour(g.world)
	g.folamour.position=Vector3(17*g.TILE,0,28*g.TILE) if g.level==25 else Vector3(g.start_cell.x*g.TILE,0,(g.start_cell.y-1)*g.TILE)
	for e in g.events:
		for i in range(e.get("world_gates",[]).size()):
			var gate=e.world_gates[i];var node=prop(g,Vector2i(gate.cell[0],gate.cell[1]));node.name="FinaleAccess%d"%i
			g.box(node,Vector3(g.TILE-.1,1.6,g.TILE-.1),Vector3(0,.8,0),g.material(Color("c19266")))
			var body=StaticBody3D.new();body.collision_layer=1;node.add_child(body)
			var collider=CollisionShape3D.new();var shape=BoxShape3D.new();shape.size=Vector3(g.TILE,2,g.TILE);collider.shape=shape;collider.position.y=1;body.add_child(collider)
			node.set_meta("body",body);g.machine_parts["finale_gate%d"%i]=node
	if g.level==21:
		for i in range(3):rocket(g,Vector2i(17,[8,20,32][i]),["PATIENCE","TENDRESSE","MODÉRATION"][i])
	elif g.level==22:
		for cell in [Vector2i(2,4),Vector2i(32,4),Vector2i(2,30),Vector2i(32,30),Vector2i(8,10),Vector2i(26,24)]:
			var root=prop(g,cell);root.set_meta("radar",true)
			g.box(root,Vector3(3,.3,3),Vector3(0,2.3,0),g.material(Color("263d51")))
			for i in range(3):g.box(root,Vector3(.2,.1,2.5),Vector3((i-1)*.8,2.5,0),g.material(Color("9bd4c3"),true))
			var sweep=g.box(root,Vector3(2.7,.1,.12),Vector3(0,2.6,0),g.material(Color("e8b379"),true));sweep.name="Sweep"
	elif g.level==23:
		for i in range(5):
			var cell=[Vector2i(5,5),Vector2i(17,5),Vector2i(29,5),Vector2i(15,15),Vector2i(19,15)][i]
			var root=prop(g,cell);g.make_folamour(root);sign_on(g,root,'ABCDE'[i],2.9)
			g.box(root,Vector3(1.8,.15,1),Vector3(0,.8,1),g.material(Color("7f645c")))
	elif g.level==24:
		for i in range(3):
			var root=rocket(g,Vector2i([5,7,9][i],5),["PATIENCE","TENDRESSE","MODÉRATION"][i]);root.scale=Vector3.ONE*.8;root.set_meta("horizon_lift",true);root.set_meta("fog_cell",g.key([5,7,9][i],3))
		for cell in [Vector2i(14,10),Vector2i(23,16),Vector2i(17,20),Vector2i(5,20)]:
			var root=prop(g,cell);g.box(root,Vector3(1.2,3,.7),Vector3(0,1.5,0),g.material(Color("394b59")))
			var light=g.box(root,Vector3(.8,.25,.3),Vector3(0,2.8,-.5),g.material(Color("e39b71"),true));light.name="Alert"
	elif g.level==25:
		for x in [11,23]:
			for y in [26,32]:
				var root=prop(g,Vector2i(x,y));g.box(root,Vector3(1.2,5,1.2),Vector3(0,2.5,0),g.material(Color("526475")))
		var plant=prop(g,Vector2i(20,30));g.box(plant,Vector3(.65,.65,.65),Vector3(0,.3,0),g.material(Color("ac8b6d")))
		for i in range(3):g.box(plant,Vector3(.8,.13,.3),Vector3(.1*i,.8+i*.3,0),g.material(Color("81aa81")))
		# A complete exterior tableau is created once and shown only after the ending.
		var outside=Node3D.new();outside.name="Surface";outside.position=Vector3(17*g.TILE,0,41*g.TILE);g.world.add_child(outside);g.machine_parts.surface=outside;outside.hide()
		g.box(outside,Vector3(26,.4,18),Vector3(0,-.3,0),g.material(Color("93a794")))
		g.box(outside,Vector3(6,.1,18),Vector3(0,0,0),g.material(Color("c3bca9")))
		for x in [-8,8]:
			g.box(outside,Vector3(6,5,8),Vector3(x,2.5,0),g.material(Color("b39d83")))
			for y in [1.7,3.5]:g.box(outside,Vector3(.12,1,1),Vector3(x-signf(x)*3.05,y,-1),g.material(Color("c6dce0"),true))
		var actor=g.make_folamour(outside);actor.position=Vector3(0,0,1);actor.rotation.y=PI
		for x in [-3.3,3.3]:
			g.box(outside,Vector3(.15,1.2,.15),Vector3(x,.6,2),g.material(Color("7b7056")))
			g.box(outside,Vector3(.9,.3,.9),Vector3(x,1.2,2),g.material(Color("749c6f")))
static func sync(g,e,v):
	if e.has("world_gates"):
		g.archive_blocks.clear()
		for i in range(e.world_gates.size()):
			var gate=e.world_gates[i];var active=not g.done.has(e.id) and v[int(gate.channel)] not in gate.allowed.map(func(x):return int(x));var node=g.machine_parts.get("finale_gate%d"%i)
			if not is_instance_valid(node):continue
			node.set_meta("archive_active",active);node.visible=active and g.render_near(node);node.get_meta("body").collision_layer=1 if active else 0
			if active:g.archive_blocks[g.key(gate.cell[0],gate.cell[1])]=true
	if g.event_nodes.has(e.id):
		for i in range(3):
			var dial=g.event_nodes[e.id].get_node_or_null("Dial%d"%i)
			if dial:dial.material_override=g.material(Color("9cd4b1") if g.done.has(e.id) else Color("d3ae78"),true)
static func update(g,delta):
	if not g.playing:return
	var stage_v=0
	for i in range(1,4):
		if g.done.has("c%d_p%d"%[g.level,i]):stage_v+=1
	for root in g.decor:
		if not root.visible:continue
		if root.has_meta("horizon_tall"):
			var diff=root.position-g.player.position;var hides_player=diff.x+diff.z>0 and absf(diff.x-diff.z)<7 and Vector2(diff.x,diff.z).length()<13
			root.scale.y=lerpf(root.scale.y,.22 if hides_player else .8 if g.level==24 else 1.0,minf(1,delta*5))
		if g.modal_open or g.won or not g.soundscape.focused:continue
		if root.has_meta("radar"):root.get_node("Sweep").rotation.y=g.elapsed*.3
		if root.has_meta("horizon_lift"):root.position.y=lerpf(root.position.y,.3*stage_v if stage_v<3 else 0,minf(1,delta*2))
		var alert=root.get_node_or_null("Alert")
		if alert:alert.material_override=g.material(Color("9cd4b1") if stage_v==3 else Color("e39b71"),true)
static func surface(g):
	g.machine_parts.surface.show()
	var at=g.machine_parts.surface.position
	g.camera.position=at+Vector3(12,15,15);g.camera.look_at(at+Vector3(0,1,0));g.camera.size=24
	for child in g.world.get_children():
		if child is WorldEnvironment:child.environment.background_color=Color("849b9c");child.environment.ambient_light_energy=.7
	g.title_label.text=g.loc("L’AVENTURE EST TERMINÉE")
	g.status_label.text=g.loc("Vous quittez une zone entièrement sécurisée. Bonne chance avec le reste.")
	g.action_label.text="";g.nearest={}
	g.interact_button.disabled=false;g.interact_button.text=g.loc("Revoir la conclusion")
