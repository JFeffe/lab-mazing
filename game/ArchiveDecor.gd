extends RefCounted
static func model(g,root,e,gold,dark):
	g.box(root,Vector3(1.8,0.85,0.8),Vector3(0,0.45,0),dark)
	g.box(root,Vector3(1.4,0.65,0.12),Vector3(0,1.15,-0.2),gold)
	g.box(root,Vector3(1.1,0.4,0.06),Vector3(0,1.15,-0.28),g.material(Color("81ced6"),true))
	for i in range(3):g.box(root,Vector3(.2,.08,.2),Vector3((i-1)*.38,.93,.2),gold)
static func setup(g):
	var storage=Node3D.new();storage.name="ArchiveStorage";g.world.add_child(storage)
	g.machine_parts.archive_storage=storage
	for row in range(3):
		for x in range(13,22):
			var shelf=Node3D.new();shelf.name="Shelf%d_%d"%[row,x]
			shelf.position=Vector3(x*g.TILE,0,[4,7,10][row]*g.TILE);storage.add_child(shelf)
			g.box(shelf,Vector3(g.TILE-.08,2.05,g.TILE-.15),Vector3(0,1,0),g.material(Color("695948")))
			for height in [.4,1.1,1.8]:
				g.box(shelf,Vector3(g.TILE,.1,g.TILE),Vector3(0,height,0),g.material(Color("c1a475")))
				for side in [-.6,0,.6]:g.box(shelf,Vector3(.4,.4,.6),Vector3(side,height+.25,-.8),g.material(Color("9dbaa9")))
			var body=g.blocker(Vector3(g.TILE,3,g.TILE),shelf.position+Vector3(0,1,0))
			shelf.set_meta("body",body)
			# Participates in the established fog and distance culling.
			shelf.set_meta("fog_cell",g.key(x,[4,7,10][row]))
			g.decor.append(shelf)
	for copy in [false,true]:
		var room=Node3D.new();room.name="CopyRoom" if copy else "OriginalRoom"
		room.position=Vector3(29*g.TILE,0,(25 if copy else 7)*g.TILE);g.world.add_child(room)
		g.machine_parts["archive_copy" if copy else "archive_original"]=room
		var mat=g.material(Color("78bed3") if copy else Color("d8b376"))
		for x in [-2,0,2]:g.box(room,Vector3(.9,.65,.9),Vector3(x,.35,-3),mat)
		var coil=Node3D.new();coil.name="Coil";room.add_child(coil)
		for i in range(4):g.box(coil,Vector3(.5,.08,.5),Vector3(0,.8+i*.12,0),g.material(Color("cd864c")))
		var lamp=g.box(room,Vector3(.6,.6,.6),Vector3(-3,1.3,1),mat);lamp.name="Lamp"
		g.box(room,Vector3(.1,1.2,.1),Vector3(-3,.6,1),mat)
		var projector=Node3D.new();projector.name="Projector";projector.position=Vector3(3,1,0);room.add_child(projector)
		g.box(projector,Vector3(.8,.6,.9),Vector3.ZERO,mat)
		g.box(projector,Vector3(.25,.25,.7),Vector3(0,0,-.55),g.material(Color("d9eeee")))
		var switch=g.box(room,Vector3(.12,.55,.12),Vector3(3,1,-3),mat);switch.name="Switch"
		var plaque=Label3D.new();plaque.name="Plaque";plaque.text=g.loc("COPIE / NORD ↑" if copy else "ORIGINAL / NORD ↑");plaque.position=Vector3(0,2,-4);plaque.font_size=50;plaque.pixel_size=.014;room.add_child(plaque)
		room.set_meta("fog_cell",g.key(29,25 if copy else 7))
		g.decor.append(room)
	set_room(g,g.machine_parts.archive_original,[1,0,1,0])
	var hatch=Node3D.new();hatch.name="PrototypeHatch";hatch.position=Vector3(23*g.TILE,0,21*g.TILE);g.world.add_child(hatch)
	g.box(hatch,Vector3(.2,2.6,2),Vector3(0,1.3,0),g.material(Color("415260")))
	var light=g.box(hatch,Vector3(.25,.2,.6),Vector3(-.15,2.5,0),g.material(Color("806759")));light.name="Light"
	g.machine_parts.archive_hatch=hatch;hatch.set_meta("fog_cell",g.key(23,21));g.decor.append(hatch)
static func sync_stacks(g,v):
	if not g.machine_parts.has("archive_storage"):return
	g.archive_blocks.clear()
	for row in range(3):
		var gap=[14,17,20][v[row]]
		for x in range(13,22):
			var shelf=g.machine_parts.archive_storage.get_node("Shelf%d_%d"%[row,x])
			var active=x!=gap
			shelf.set_meta("archive_active",active)
			shelf.visible=active and g.render_near(shelf)
			shelf.get_meta("body").collision_layer=1 if active else 0
			if active:g.archive_blocks[g.key(x,[4,7,10][row])]=true
static func set_room(g,room,v):
	room.get_node("Lamp").material_override=g.material(Color("fff0ad") if v[0]==1 else Color("414c59"),v[0]==1)
	room.get_node("Coil").position=Vector3([-2,0,2][v[1]],0,-3)
	room.get_node("Projector").rotation.y=-v[2]*PI/2
	room.get_node("Switch").rotation.x=PI*.3 if v[3]==0 else -PI*.3
static func sync_room(g,v):
	if g.machine_parts.has("archive_copy"):set_room(g,g.machine_parts.archive_copy,v)
static func finish(g):
	if not g.machine_parts.has("archive_hatch"):return
	var hatch=g.machine_parts.archive_hatch
	hatch.rotation.y=.25
	hatch.get_node("Light").material_override=g.material(Color("80dfb5"),true)

static func translate_rooms(g):
	for room in ["archive_original","archive_copy"]:
		if g.machine_parts.has(room):g.machine_parts[room].get_node("Plaque").text=g.loc("ORIGINAL / NORD ↑" if room=="archive_original" else "COPIE / NORD ↑")
