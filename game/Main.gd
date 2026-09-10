extends Node3D
const Subject16=preload("res://Subject16.gd")
const ChapterIdentity=preload("res://ChapterIdentity.gd")
var dossier=Subject16.blank()
var decorative_motion=true
var folamour_comments=true
var animated_doctors=[]
var decor_time=0.0
var reaction_text=""
var reaction_time=0.0
var last_observed_errors=0
var folamour_line:Label
const LevelEndings=preload("res://LevelEndings.gd")
const TILE=2.6
const MOVE_SPEED=9.1
const SHORTCUT_LAYOUT_REVISION=2
const SAVE="user://experience16_v4.json"
const LEGACY_SAVE="user://experience16_v2.json"
const ForesightChapter=preload("res://ForesightChapter.gd")
const FinaleChapter=preload("res://FinaleChapter.gd")
var chapter5_data=JSON.parse_string(FileAccess.get_file_as_string("res://data/chapter5.json"))
const CertaintyChapter=preload("res://CertaintyChapter.gd")
var chapter4_data=JSON.parse_string(FileAccess.get_file_as_string("res://data/chapter4.json"))
var chapter3_data=JSON.parse_string(FileAccess.get_file_as_string("res://data/chapter3.json"))
const Guidance=preload("res://Guidance.gd")
var guidance_data=JSON.parse_string(FileAccess.get_file_as_string("res://data/guidance.json"))
var soundscape
var localization=preload("res://Localization.gd").new()
var ui_layer:CanvasLayer
var toast_source=""
const MapWidget=preload("res://MapView.gd")
const PuzzleControls=preload("res://PuzzleControls.gd")
var puzzle_states={}
const Navigator=preload("res://Navigation.gd")
var move_path=[]
var click_event={}
var destination_marker:Node3D
var stuck_time=0.0
var ui_mobile=false
var last_window_size=Vector2i.ZERO
var interact_button:Button
var modal_scroll:ScrollContainer
var signal_lights={}
var decor=[]
var ambience:AudioStreamPlayer
var ambience_zone=-1
var material_cache={}
var folamour:Node3D
var level=1
var level_stats={}
var level_data={}
var start_cell=Vector2i(9,1)
var world:Node3D
var item_catalog={}
var dial_settings={}
var machine_parts={}
var grid=[]
var events=[]
var seen={}
var done={}
var journal={}
var journal_order=[]
var walked={}
var shortcuts=[]
var open_shortcuts={}
var shortcut_cells={}
var shortcut_nodes={}
var wall_bodies={}
var hints={}
var inventory={}
var elapsed=0.0
var errors=0
var playing=false
var won=false
var modal_open=false
var nearest={}
var current_event={}
var player:CharacterBody3D
var avatar:Node3D
var camera:Camera3D
var walls={}
var floors={}
var event_nodes={}
var door_bodies={}
var archive_blocks={}
var creature_bodies={}
var hud:Control
var overlay:Control
var modal_box:VBoxContainer
var title_label:Label
var status_label:Label
var action_label:Label
var toast_label:Label
var mini_map
var code_entry:LineEdit
var feedback:Label
var zoom=22.0
var auto_timer=0.0
var save_status=""
var fog_timer=0.0
var toast_timer=0.0
var accent=Color("e9be72")
var audio:AudioStreamPlayer
var rng=RandomNumberGenerator.new()
var muted=false
var test_mode=false
var box_mesh_cache={}

func _ready():
	rng.seed=16
	test_mode="--verify" in OS.get_cmdline_user_args() or "--verify-machines" in OS.get_cmdline_user_args() or "--screenshot" in OS.get_cmdline_user_args()
	configure_viewport()
	setup_input()
	set_level(1)
	build_ui()
	audio=AudioStreamPlayer.new()
	add_child(audio)
	ambience=AudioStreamPlayer.new()
	ambience.volume_db=-26
	add_child(ambience)
	soundscape=preload("res://LabAudio.gd").new()
	add_child(soundscape)
	muted=soundscape.preference_muted
	get_window().size_changed.connect(window_resized)
	if "--verify" in OS.get_cmdline_user_args() or "--verify-machines" in OS.get_cmdline_user_args():
		start_game(false,2 if "--verify-machines" in OS.get_cmdline_user_args() else 1)
		verify_game()
	elif "--screenshot" in OS.get_cmdline_user_args():
		start_game(false)
		close_modal()
		capture_preview()
	else: show_title()

func setup_input():
	var bindings={"north":[KEY_W,KEY_Z,KEY_UP],"south":[KEY_S,KEY_DOWN],"west":[KEY_A,KEY_Q,KEY_LEFT],"east":[KEY_D,KEY_RIGHT],"interact":[KEY_E],"map":[KEY_M,KEY_TAB],"inventory":[KEY_I],"journal":[KEY_J],"pause":[KEY_ESCAPE]}
	for action in bindings:
		InputMap.add_action(action)
		for code in bindings[action]:
			var ev=InputEventKey.new()
			ev.physical_keycode=code
			InputMap.action_add_event(action,ev)

func material(color,glow=false):
	var cache_key=str(color)+str(glow)
	if material_cache.has(cache_key): return material_cache[cache_key]
	var m=StandardMaterial3D.new()
	m.albedo_color=color
	m.roughness=0.95
	if glow:
		m.emission_enabled=true
		m.emission=color
		m.emission_energy_multiplier=0.4
	material_cache[cache_key]=m
	return m

func box(parent,dimensions,pos,mat):
	var mesh=MeshInstance3D.new()
	if not box_mesh_cache.has(dimensions):
		var shape=BoxMesh.new()
		shape.size=dimensions
		box_mesh_cache[dimensions]=shape
	mesh.mesh=box_mesh_cache[dimensions]
	mesh.position=pos
	mesh.material_override=mat
	parent.add_child(mesh)
	return mesh

func blocker(dimensions,pos):
	var body=StaticBody3D.new()
	body.position=pos
	var c=CollisionShape3D.new()
	var s=BoxShape3D.new()
	s.size=dimensions
	c.shape=s
	body.add_child(c)
	world.add_child(body)
	return body

func build_world():
	var env=WorldEnvironment.new()
	var settings=Environment.new()
	settings.background_mode=Environment.BG_COLOR
	settings.background_color=Color(Subject16.theme(level).background)
	settings.ambient_light_source=Environment.AMBIENT_SOURCE_COLOR
	settings.ambient_light_color=Color(Subject16.theme(level).ambient)
	settings.ambient_light_energy=0.38
	settings.tonemap_mode=Environment.TONE_MAPPER_FILMIC
	env.environment=settings
	world.add_child(env)
	var sun=DirectionalLight3D.new()
	sun.rotation_degrees=Vector3(-55,-30,0)
	sun.light_color=Color(Subject16.theme(level).sun)
	sun.light_energy=0.72
	sun.shadow_enabled=not OS.has_feature("web")
	world.add_child(sun)
	var palettes=[Color("648a83"),Color("7b83a4"),Color("9e8174")] if level==1 else [Color("9e8460"),Color("527f8e"),Color("858371")]
	if level in range(11,16):palettes=[[Color("ab8e68"),Color("809a96"),Color("8797b2")],[Color("a2a084"),Color("8e9cae"),Color("8cab98")],[Color("6c97a2"),Color("8f85a4"),Color("88a798")],[Color("849fa2"),Color("b49a6d"),Color("8e8eae")],[Color("9582a8"),Color("8c9c98"),Color("ae986f")]][level-11]
	if level==10: palettes=[Color("a48a64"),Color("638ba5"),Color("819990")]
	if level==9: palettes=[Color("7e8ba5"),Color("aa9276"),Color("749e94")]
	if level==8: palettes=[Color("ac9679"),Color("829cac"),Color("8a9e80")]
	if level==7: palettes=[Color("9aa7b0"),Color("b19c7b"),Color("839c9a")]
	if level==6: palettes=[Color("729d77"),Color("82aaa0"),Color("af986d")]
	if level==5: palettes=[Color("659b9d"),Color("ac9070"),Color("8982a9")]
	if level==4: palettes=[Color("a18d72"),Color("788ba2"),Color("6b968d")]
	if level==3: palettes=[Color("7789a5"),Color("638f94"),Color("93839e")]
	if level in range(16,21):palettes=[[Color("b59e79"),Color("8c9c99"),Color("869bb5")],[Color("96b09a"),Color("b4a27d"),Color("8d9cab")],[Color("779daa"),Color("9f94ae"),Color("91b9ae")],[Color("ac8964"),Color("909eaa"),Color("b19d7a")],[Color("aa91b7"),Color("829c95"),Color("b4a080")]][level-16]
	if level>=21:palettes=[[Color("a5a08b"),Color("858e9f"),Color("a28d7b")],[Color("7896a8"),Color("859a9e"),Color("9da893")],[Color("a693aa"),Color("9b927d"),Color("859c90")],[Color("a5816d"),Color("98918c"),Color("8f9f9b")],[Color("8c9b9d"),Color("98a798"),Color("b4a48e")]][level-21]
	for i in range(3):palettes[i]=palettes[i].lerp(Color(Subject16.theme(level).palettes[i]),0.65)
	for y in range(grid.size()):
		for x in range(grid.size()):
			var k=key(x,y)
			var col=palettes[zone(y,x)]
			if floor_at(x,y):
				floors[k]=box(world,Vector3(TILE-0.05,0.25,TILE-0.05),Vector3(x*TILE,-0.15,y*TILE),material(col*(0.94+float((x+y)%3)*0.045)))
				floors[k].visible=false
			else:
				var near_floor=false
				for dy in range(-1,2):
					for dx in range(-1,2):
						if floor_at(x+dx,y+dy): near_floor=true
				if not near_floor: continue
				var root=Node3D.new()
				root.position=Vector3(x*TILE,0,y*TILE)
				world.add_child(root)
				box(root,Vector3(TILE,2.15,TILE),Vector3(0,1,0),material(col.darkened(0.43)))
				box(root,Vector3(TILE+0.02,0.12,TILE+0.02),Vector3(0,2.12,0),material(col.lightened(0.07)))
				if (x+y)%4==0: box(root,Vector3(TILE+0.04,0.11,TILE+0.04),Vector3(0,0.6,0),material(col.lightened(0.25)))
				wall_bodies[k]=blocker(Vector3(TILE,3,TILE),Vector3(x*TILE,1,y*TILE))
				walls[k]=root
				root.visible=false
	blocker(Vector3(100,1,100),Vector3(44,-0.7,44))
	var span=grid.size()*TILE
	for edge in [-TILE*0.5-0.2,span-TILE*0.5+0.2]:
		blocker(Vector3(0.4,5,span+1),Vector3(edge,2,(span-TILE)/2))
		blocker(Vector3(span+1,5,0.4),Vector3((span-TILE)/2,2,edge))
	player=CharacterBody3D.new()
	player.position=Vector3(start_cell.x*TILE,0.1,start_cell.y*TILE)
	var c=CollisionShape3D.new()
	var capsule=CapsuleShape3D.new()
	capsule.radius=0.3
	capsule.height=1.45
	c.shape=capsule
	c.position.y=0.73
	player.add_child(c)
	world.add_child(player)
	avatar=Node3D.new()
	player.add_child(avatar)
	box(avatar,Vector3(0.62,0.73,0.44),Vector3(0,0.83,0),material(Color("eaa855")))
	box(avatar,Vector3(0.48,0.48,0.47),Vector3(0,1.44,0),material(Color("ead3ac")))
	box(avatar,Vector3(0.52,0.18,0.49),Vector3(0,1.71,0.03),material(Color("483c39")))
	box(avatar,Vector3(0.51,0.43,0.24),Vector3(0,0.9,0.31),material(Color("3a5660")))
	for x in [-0.18,0.18]:
		box(avatar,Vector3(0.22,0.45,0.25),Vector3(x,0.25,0),material(Color("324450")))
		box(avatar,Vector3(0.24,0.15,0.36),Vector3(x,0.08,-0.04),material(Color("222e39")))
		box(avatar,Vector3(0.07,0.07,0.025),Vector3(x*0.68,1.46,-0.245),material(Color("273342")))
	var marker=MeshInstance3D.new()
	var ring=TorusMesh.new()
	ring.inner_radius=0.42
	ring.outer_radius=0.48
	marker.mesh=ring
	marker.material_override=material(accent,true)
	marker.position.y=0.025
	player.add_child(marker)
	camera=Camera3D.new()
	camera.projection=Camera3D.PROJECTION_ORTHOGONAL
	camera.size=zoom
	camera.far=180
	world.add_child(camera)
	for e in events: build_event(e)
	build_shortcuts()
	build_readability_decor()
	if level==2: build_machine_decor()
	if level==6:preload("res://GreenhouseDecor.gd").decorate(self)
	update_camera(1)

func build_event(e):
	var root=Node3D.new()
	root.position=Vector3(e.cell[0]*TILE,0,e.cell[1]*TILE)
	if e.has("ending_offset"):
		root.position+=Vector3(e.ending_offset[0],0,e.ending_offset[1])
	# Mount the exit just in front of the adjacent wall, keeping its discovery cell.
	if e.has("wall_face"):
		root.position+=Vector3(e.wall_face[0],0,e.wall_face[1])*TILE*0.45
	world.add_child(root)
	event_nodes[e.id]=root
	var gold=material(accent,true)
	var dark=material(Color("243d48"))
	if e.kind=="collectible":
		ChapterIdentity.model(self,root,e)
	elif LevelEndings.is_doctor(e):
		folamour=root
		make_folamour(root)
	elif e.kind in ["door","oneway","exit"]:
		var horizontal=e.get("axis","y")=="x"
		if horizontal: root.rotation.y=PI/2
		for side in [-1,1]: box(root,Vector3(0.19,2.7,0.28),Vector3(side*1.16,1.3,0),dark)
		box(root,Vector3(2.5,0.2,0.3),Vector3(0,2.66,0),gold)
		var leaf=box(root,Vector3(TILE-0.3,2.4,0.22),Vector3(0,1.17,0),material(Color("3a6775")))
		leaf.name="Leaf"
		box(leaf,Vector3(0.15,1.8,0.02),Vector3(0,0,0.1),gold)
		door_bodies[e.id]=blocker(Vector3(TILE+0.04,2.7,TILE+0.04) if e.kind=="oneway" else (Vector3(0.38,2.7,TILE+0.04) if horizontal else Vector3(TILE+0.04,2.7,0.38)),root.position+Vector3(0,1.2,0))
		if e.kind=="oneway":
			for z in [-TILE,TILE]:
				for side in [-1,1]:
					var arrow=box(root,Vector3(0.12,0.045,0.7),Vector3(side*0.22,0.03,z),gold)
					arrow.rotation.y=side*PI/4
	elif e.kind=="pickup":
		box(root,Vector3(0.75,0.18,0.75),Vector3(0,0.08,0),dark)
		if e.get("appearance", "artifact")=="weight":
			box(root,Vector3(0.55,0.4+float(e.mass)*0.06,0.55),Vector3(0,0.8,0),gold)
			var number=Label3D.new()
			number.text=str(int(e.mass))+" kg"
			number.position=Vector3(0,1.3,0)
			number.billboard=BaseMaterial3D.BILLBOARD_ENABLED
			number.font_size=32
			root.add_child(number)
		elif e.get("appearance", "artifact")=="seed":
			preload("res://GreenhouseDecor.gd").plant(self,root,Vector3(0,.2,0),.7)
		elif e.get("appearance", "artifact")=="cup":
			box(root,Vector3(.5,.6,.5),Vector3(0,.7,0),material(Color("f0e4c5")))
			box(root,Vector3(.20,.35,.14),Vector3(.34,.7,0),gold)
		elif e.get("appearance", "artifact")=="magnet":
			for x in [-0.25,0.25]: box(root,Vector3(0.18,0.65,0.2),Vector3(x,0.85,0),material(Color("dc7869")))
			box(root,Vector3(0.68,0.2,0.2),Vector3(0,0.55,0),gold)
		elif e.get("appearance", "artifact")=="key":
			box(root,Vector3(0.13,0.7,0.13),Vector3(0,0.9,0),gold)
			box(root,Vector3(0.4,0.28,0.14),Vector3(0,1.27,0),gold)
			box(root,Vector3(0.3,0.13,0.14),Vector3(0.1,0.62,0),gold)
		elif e.id.begins_with("disc_"):
			var disc=MeshInstance3D.new()
			var shape=CylinderMesh.new()
			shape.top_radius=0.42
			shape.bottom_radius=0.42
			shape.height=0.12
			disc.mesh=shape
			disc.position.y=1
			disc.rotation.x=PI/2
			var colors={"disc_sun":Color("e9be72"),"disc_moon":Color("c9e2e8"),"disc_star":Color("b5a3df")}
			disc.material_override=material(colors[e.id],true)
			root.add_child(disc)
		elif e.id=="fuse":
			box(root,Vector3(0.24,0.7,0.24),Vector3(0,0.9,0),material(Color("eee4d3")))
			for y in [0.55,1.25]: box(root,Vector3(0.28,0.14,0.28),Vector3(0,y,0),gold)
		elif e.get("appearance", "artifact")=="artifact":
			var crystal=box(root,Vector3(0.47,0.65,0.47),Vector3(0,1,0),material(Color("b49ada"),true))
			crystal.rotation_degrees=Vector3(20,45,20)
		else:
			for i in range(min(e.get("amount",1),4)): box(root,Vector3(0.45,0.12,0.45),Vector3(0,0.4+i*0.15,0),gold)
	elif e.has("model"):
		if e.model=="finale":preload("res://FinaleDecor.gd").model(self,root,e,gold,dark)
		elif e.model=="certainty":preload("res://CertaintyDecor.gd").model(self,root,e,gold,dark)
		elif e.model=="foresight":preload("res://ForesightDecor.gd").model(self,root,e,gold,dark)
		elif e.model in ["stacks","reports","twin"]:preload("res://ArchiveDecor.gd").model(self,root,e,gold,dark)
		elif e.model in ["seating","schedule","conference"]:preload("res://MeetingDecor.gd").model(self,root,e,gold,dark)
		elif e.model in ["parcels","mailnet","address"]:preload("res://MailDecor.gd").model(self,root,e,gold,dark)
		elif e.model in ["overlay","filing","copier"]:preload("res://OfficeDecor.gd").model(self,root,e,gold,dark)
		elif e.model in ["pipes","growth","blend"]:preload("res://GreenhouseDecor.gd").model(self,root,e,gold,dark)
		else:build_machine(root,e,gold,dark)
	elif e.kind=="creature":
		creature_bodies[e.id]=blocker(Vector3(1.4,1.5,1.4),root.position+Vector3(0,0.7,0))
		box(root,Vector3(1.2,0.8,0.8),Vector3(0,0.8,0),material(Color("6b7387")))
		box(root,Vector3(0.8,0.72,0.68),Vector3(0,1.12,-0.57),material(Color("929bb0")))
		for x in [-0.42,0.42]:
			box(root,Vector3(0.22,0.6,0.22),Vector3(x,0.3,0.15),dark)
			box(root,Vector3(0.19,0.35,0.2),Vector3(x*0.7,1.58,-0.48),gold)
			box(root,Vector3(0.11,0.11,0.04),Vector3(x*0.52,1.23,-0.93),gold)
	else:
		box(root,Vector3(0.85,1,0.6),Vector3(0,0.5,0),dark)
		box(root,Vector3(0.75,0.55,0.08),Vector3(0,1.12,-0.27),material(Color("93d4cf"),true))
	var label=Label3D.new()
	label.text="◇" if e.kind=="collectible" else ("Folamour · " if LevelEndings.is_doctor(e) else "")+e.get("ref","?")
	label.position.y=3.0 if e.kind in ["door","exit","oneway"] or e.has("model") else 1.95
	label.billboard=BaseMaterial3D.BILLBOARD_ENABLED
	label.font_size=38
	label.pixel_size=0.011
	label.modulate=Color("fff4d9")
	label.outline_modulate=Color("182831")
	label.outline_size=8
	root.add_child(label)
	root.visible=false
	add_event_signals(root,e)

func build_shortcuts():
	for sc in shortcuts:
		var k=key(sc.cell[0],sc.cell[1])
		var center=Vector3(sc.cell[0]*TILE,0,sc.cell[1]*TILE)
		floors[k]=box(world,Vector3(TILE,0.25,TILE),center+Vector3(0,-0.15,0),material(Color("83bcb0")))
		floors[k].visible=false
		var root=Node3D.new()
		root.position=center
		if sc.axis=="x": root.rotation.y=PI/2
		world.add_child(root)
		var mat=material(Color("86d6c1"),true)
		for side in [-1,1]: box(root,Vector3(0.16,2.4,0.23),Vector3(side*1.2,1.15,0),mat)
		box(root,Vector3(TILE,0.17,0.23),Vector3(0,2.38,0),mat)
		var tag=Label3D.new()
		tag.text=sc.id
		tag.position.y=2.7
		tag.billboard=BaseMaterial3D.BILLBOARD_ENABLED
		tag.font_size=34
		tag.pixel_size=0.011
		root.add_child(tag)
		root.visible=false
		shortcut_nodes[sc.id]=root
func sync_shortcuts():
	shortcut_cells.clear()
	for sc in shortcuts:
		var opened=open_shortcuts.has(sc.id)
		var k=key(sc.cell[0],sc.cell[1])
		if opened: shortcut_cells[k]=true
		wall_bodies[k].collision_layer=0 if opened else 1
		walls[k].visible=seen.has(k) and not opened
		floors[k].visible=opened
		shortcut_nodes[sc.id].visible=opened
func record_walk():
	var c=Vector2i(roundi(player.position.x/TILE),roundi(player.position.z/TILE))
	if not floor_at(c.x,c.y): return
	var k=key(c.x,c.y)
	if walked.has(k): return
	walked[k]=true
	for sc in shortcuts:
		if open_shortcuts.has(sc.id): continue
		if walked.has(key(sc.sides[0][0],sc.sides[0][1])) and walked.has(key(sc.sides[1][0],sc.sides[1][1])):
			open_shortcuts[sc.id]=true
			seen[key(sc.cell[0],sc.cell[1])]=true
			sync_shortcuts()
			add_journal(sc.id,"Raccourci "+sc.id+" révélé\nVous avez parcouru les deux côtés du mur. Ce passage reste ouvert dans les deux sens et apparaît sur la carte.")
			if is_instance_valid(toast_label): toast("Raccourci "+sc.id+" révélé — passage ouvert !")
			if is_instance_valid(soundscape):soundscape.effect(self,"door")
			if is_instance_valid(mini_map): mini_map.queue_redraw()
			save_game()
func add_journal(id,text):
	journal[id]=text
	journal_order.erase(id)
	journal_order.append(id)
func recent_journal_keys():
	var keys=journal_order.duplicate()
	keys.reverse()
	return keys

func label(text,font_size=18,color=Color("e1e9e8")):
	var l=Label.new()
	l.text=loc(text)
	l.mouse_filter=Control.MOUSE_FILTER_IGNORE
	l.set_meta("source_text",text)
	l.add_theme_font_size_override("font_size",font_size)
	l.add_theme_color_override("font_color",color)
	return l
func style(color,border=Color("3e5961")):
	var s=StyleBoxFlat.new()
	s.bg_color=color
	s.set_border_width_all(1)
	s.border_color=border
	s.set_corner_radius_all(10)
	s.content_margin_left=12 if ui_mobile else 22
	s.content_margin_right=12 if ui_mobile else 22
	s.content_margin_top=14
	s.content_margin_bottom=14
	return s
func button(text,callback,primary=false):
	var b=Button.new()
	b.text=loc(text)
	b.set_meta("source_text",text)
	b.custom_minimum_size.y=56 if ui_mobile else 44
	b.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	b.mouse_default_cursor_shape=Control.CURSOR_POINTING_HAND
	b.add_theme_stylebox_override("normal",style(Color("dcb875") if primary else Color("203642")))
	b.add_theme_stylebox_override("hover",style(Color("efd49d") if primary else Color("365663"),accent))
	b.add_theme_stylebox_override("pressed",style(Color("caa46a") if primary else Color("172b36")))
	b.add_theme_color_override("font_color",Color("14242d") if primary else Color("e4ede9"))
	b.pressed.connect(callback,CONNECT_DEFERRED)
	return b
func content_width():
	return minf(676.0,get_viewport().get_visible_rect().size.x-84.0)
func configure_viewport():
	last_window_size=get_window().size
	ui_mobile=mini(last_window_size.x,last_window_size.y)<720 or DisplayServer.is_touchscreen_available()
	# Keep UI sharp; cap only the 3D buffer on high-density touch screens.
	Engine.max_fps=30 if ui_mobile else 60
	get_viewport().scaling_3d_scale=clampf(1152.0/maxf(last_window_size.x,last_window_size.y),0.25,0.85) if ui_mobile else 1.0
	if ui_mobile:
		var width=480 if last_window_size.x<last_window_size.y else 960
		get_window().content_scale_size=Vector2i(width,roundi(float(width)*last_window_size.y/maxi(1,last_window_size.x)))
	else: get_window().content_scale_size=Vector2i(1440,900)
func window_resized():
	if get_window().size==last_window_size: return
	call_deferred("rebuild_layout")
func rebuild_layout():
	if get_window().size==last_window_size: return
	configure_viewport()
	stop_navigation()
	if is_instance_valid(ui_layer):
		remove_child(ui_layer)
		ui_layer.queue_free()
	build_ui()
	if won: show_win()
	elif playing:
		update_hud()
		show_pause()
	else: show_title()
func build_ui():
	ui_layer=CanvasLayer.new()
	add_child(ui_layer)
	var base=Control.new()
	base.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	base.mouse_filter=Control.MOUSE_FILTER_IGNORE
	var theme_v=Theme.new()
	theme_v.default_font=load("res://assets/Interface.ttf")
	theme_v.default_font_size=20 if ui_mobile else 18
	base.theme=theme_v
	ui_layer.add_child(base)
	hud=Control.new()
	hud.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	hud.mouse_filter=Control.MOUSE_FILTER_IGNORE
	base.add_child(hud)
	var top=PanelContainer.new()
	top.position=Vector2(12,12)
	top.custom_minimum_size=Vector2(minf(570,get_viewport().get_visible_rect().size.x-24),84)
	top.add_theme_stylebox_override("panel",style(Color("132733e8")))
	hud.add_child(top)
	var stack=VBoxContainer.new()
	top.add_child(stack)
	title_label=label("01 / OBSERVATION",19,accent)
	title_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	stack.add_child(title_label)
	status_label=label("",14)
	status_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	stack.add_child(status_label)
	var dossier_row=HBoxContainer.new()
	dossier_row.add_theme_constant_override("separation",8)
	stack.add_child(dossier_row)
	var objective_button=button("Objectif actuel",show_objective)
	objective_button.custom_minimum_size.y=38
	objective_button.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	dossier_row.add_child(objective_button)
	var dossier_button=button("Dossier du sujet 16",func():Subject16.show(self))
	dossier_button.custom_minimum_size.y=38
	dossier_button.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	dossier_row.add_child(dossier_button)
	folamour_line=label("",14,accent)
	folamour_line.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	folamour_line.hide()
	stack.add_child(folamour_line)
	var mp=PanelContainer.new()
	mp.set_anchors_and_offsets_preset(Control.PRESET_TOP_RIGHT)
	mp.position=Vector2(-234,12)
	mp.custom_minimum_size=Vector2(220,240)
	mp.add_theme_stylebox_override("panel",style(Color("132733e8")))
	hud.add_child(mp)
	var ms=VBoxContainer.new()
	mp.add_child(ms)
	ms.add_child(label("PLAN D'EXPLORATION",12,accent))
	mini_map=MapWidget.new()
	mini_map.game=self
	mini_map.custom_minimum_size=Vector2(176,176)
	ms.add_child(mini_map)
	mp.visible=not ui_mobile
	var bottom=PanelContainer.new()
	bottom.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	bottom.offset_left=12
	bottom.offset_right=-12
	bottom.offset_top=-174 if ui_mobile else -150
	bottom.offset_bottom=-12
	bottom.add_theme_stylebox_override("panel",style(Color("132733ef")))
	hud.add_child(bottom)
	var rows=VBoxContainer.new()
	rows.add_theme_constant_override("separation",8)
	bottom.add_child(rows)
	var action_row=HBoxContainer.new()
	rows.add_child(action_row)
	action_label=label("Cliquez / touchez le sol pour explorer",16)
	action_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	action_label.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	action_row.add_child(action_label)
	interact_button=button("Examiner",func():
		if won and level==25:FinaleChapter.finish(self)
		elif not nearest.is_empty():interact(nearest)
	,true)
	interact_button.custom_minimum_size.x=125
	interact_button.add_theme_font_size_override("font_size",16)
	interact_button.autowrap_mode=TextServer.AUTOWRAP_OFF
	action_row.add_child(interact_button)
	var nav=HBoxContainer.new()
	nav.add_theme_constant_override("separation",7)
	rows.add_child(nav)
	for pair in [["Sac",show_inventory],["Journal",show_journal],["Carte",show_map],["Pause",show_pause]]:
		var b=button(pair[0],pair[1])
		b.size_flags_horizontal=Control.SIZE_EXPAND_FILL
		nav.add_child(b)
	toast_label=label("",17,Color("fff0ca"))
	toast_label.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	toast_label.offset_left=20
	toast_label.offset_right=-20
	toast_label.offset_top=-250 if ui_mobile else -215
	toast_label.offset_bottom=-185 if ui_mobile else -160
	toast_label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	toast_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	hud.add_child(toast_label)
	overlay=Control.new()
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	base.add_child(overlay)
	var shade=ColorRect.new()
	shade.color=Color(0.025,0.055,0.075,0.87)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(shade)
	modal_scroll=ScrollContainer.new()
	modal_scroll.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	modal_scroll.horizontal_scroll_mode=ScrollContainer.SCROLL_MODE_DISABLED
	overlay.add_child(modal_scroll)
	var center=CenterContainer.new()
	center.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	center.size_flags_vertical=Control.SIZE_EXPAND_FILL
	center.custom_minimum_size.y=get_viewport().get_visible_rect().size.y
	modal_scroll.add_child(center)
	var margin=MarginContainer.new()
	for side in ["left","right","top","bottom"]: margin.add_theme_constant_override("margin_"+side,12)
	center.add_child(margin)
	var panel=PanelContainer.new()
	panel.custom_minimum_size.x=content_width()+44
	panel.add_theme_stylebox_override("panel",style(Color("142b37"),Color("55716d")))
	margin.add_child(panel)
	modal_box=VBoxContainer.new()
	modal_box.custom_minimum_size.x=content_width()
	modal_box.add_theme_constant_override("separation",10)
	panel.add_child(modal_box)

func clear_modal(kicker,heading):
	for child in modal_box.get_children():
		modal_box.remove_child(child)
		child.queue_free()
	stop_navigation()
	modal_open=true
	modal_scroll.scroll_vertical=0
	overlay.show()
	modal_box.add_child(label(kicker,13,accent))
	var heading_label=label(heading,25 if ui_mobile else 30)
	heading_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	modal_box.add_child(heading_label)
func paragraph(text,size_v=18):
	var l=label(text,size_v)
	l.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	l.custom_minimum_size.x=content_width()
	modal_box.add_child(l)
	return l
func close_modal():
	overlay.hide()
	modal_open=false
	current_event={}
	if playing: save_game()
func has_save(): return not read_save().is_empty()
func read_save():
	for path in [SAVE,SAVE+".bak",LEGACY_SAVE]:
		if not FileAccess.file_exists(path): continue
		var parser=JSON.new()
		if parser.parse(FileAccess.get_file_as_string(path))!=OK: continue
		var data=parser.data
		if data is Dictionary and int(data.get("version",0)) in [2,4] and int(data.get("level",1)) in range(1,26): return data
	return {}
func show_title():
	DisplayServer.window_set_title(loc("LE LABYRINTHE")+" — Folamour")
	playing=false
	hud.hide()
	clear_modal("DOCTEUR FOLAMOUR / EXPÉRIENCES","LE LABYRINTHE")
	paragraph("Le laboratoire vous attend.\nLes machines aussi.",22)
	paragraph("Cinq labyrinthes forment le chapitre 1, du laboratoire au défi final de Folamour. Objets à assembler, énigmes à manipuler et indices à recouper. Aucune limite de temps.")
	paragraph("Le chapitre 2 propose cinq missions : les serres, les photocopies, le courrier, la réunion et les archives.",17)
	paragraph("Le chapitre 5 conclut HORIZON. Les cinq chapitres et leurs vingt-cinq niveaux sont disponibles.",17)
	var saved=read_save()
	if not saved.is_empty():
		modal_box.add_child(button("Continuer la partie",func(): start_game(true),true))
		paragraph(loc("Sauvegarde : %s • %02d:%02d") % [level_name(int(saved.get("level",1))),int(saved.get("elapsed",0))/60,int(saved.get("elapsed",0))%60],16)
		if saved.get("won",false) and int(saved.get("level",1))<5: paragraph("Niveau terminé : reprenez pour accéder à la suite.",16)
	modal_box.add_child(button("Choisir un chapitre",show_chapters,not has_save()))
	modal_box.add_child(button("Sélection de niveau / test",show_level_select))
	paragraph("Clic gauche, clic droit ou toucher sur le sol pour vous déplacer. Touchez un objet pour l’examiner.\nWASD / ZQSD / flèches : marcher • E : interagir\nI : sac • J : journal • M : carte • Échap : pause",15)
	paragraph("VERSION 0.23.1 · POUR VOTRE TRANQUILLITÉ DÉFINITIVE",13)
	modal_box.add_child(button("Langue / Language",func(): show_language(false)))
	modal_box.add_child(button("Réglages audio",func(): show_audio(false)))
	if not OS.has_feature("web"): modal_box.add_child(button("Quitter",func(): get_tree().quit()))
func show_chapters():
	clear_modal("CHAPITRES","Choisir son chapitre")
	paragraph("Chapitre 1 — Le labyrinthe de Folamour",22)
	paragraph("Niveaux 1 → 2 → 3 → 4 → 5. Une aventure complète, jusqu’au prototype ZÉRO et à la rencontre de Folamour.")
	var saved=read_save()
	if not saved.is_empty() and int(saved.get("level",1))<=5:
		modal_box.add_child(button("Reprendre le chapitre 1",func(): start_game(true),true))
	modal_box.add_child(button("Commencer le chapitre 1",func(): confirm_new(1)))
	paragraph("Chapitre 2 — Le stage non rémunéré",22)
	paragraph("Cinq missions disponibles : les serres, les photocopies, le courrier, la réunion et les archives.",17)
	if not saved.is_empty() and int(saved.get("level",1)) in range(6,11):
		modal_box.add_child(button("Reprendre le chapitre 2",func(): start_game(true),true))
	modal_box.add_child(button(level_name(6),func(): confirm_new(6)))
	modal_box.add_child(button(level_name(7),func(): confirm_new(7)))
	modal_box.add_child(button(level_name(8),func(): confirm_new(8)))
	modal_box.add_child(button(level_name(9),func(): confirm_new(9)))
	modal_box.add_child(button(level_name(10),func(): confirm_new(10)))
	paragraph("Chapitre 3 — Le département de la prévoyance",22)
	if not saved.is_empty() and int(saved.get("level",1)) in range(11,16):
		modal_box.add_child(button("Reprendre le chapitre 3",func():start_game(true),true))
	for n in range(11,16):modal_box.add_child(button(level_name(n),func():confirm_new(n)))
	paragraph("Chapitre 4 — Le complexe de la certitude",22)
	if not saved.is_empty() and int(saved.get("level",1)) in range(16,21):
		modal_box.add_child(button("Reprendre le chapitre 4",func():start_game(true),true))
	for n in range(16,21):modal_box.add_child(button(level_name(n),func():confirm_new(n)))
	paragraph("Chapitre 5 — Pour votre tranquillité définitive",22)
	for n in range(21,26):modal_box.add_child(button(level_name(n),func():confirm_new(n)))
	modal_box.add_child(button("Retour",show_title))
func show_level_select():
	clear_modal("TEST / NIVEAUX","Choisir un niveau")
	paragraph("Un démarrage direct remplace la partie actuelle après confirmation. Pour l’histoire complète, commencez le chapitre 1.")
	paragraph("Chapitre 1 — Le labyrinthe de Folamour",22)
	for n in range(1,6):modal_box.add_child(button(level_name(n),func(): confirm_new(n)))
	paragraph("Chapitre 2 — Le stage non rémunéré",22)
	for n in range(6,11):modal_box.add_child(button(level_name(n),func(): confirm_new(n)))
	paragraph("Chapitre 3 — Le département de la prévoyance",22)
	for n in range(11,16):modal_box.add_child(button(level_name(n),func():confirm_new(n)))
	paragraph("Chapitre 4 — Le complexe de la certitude",22)
	for n in range(16,21):modal_box.add_child(button(level_name(n),func():confirm_new(n)))
	paragraph("Chapitre 5 — Pour votre tranquillité définitive",22)
	for n in range(21,26):modal_box.add_child(button(level_name(n),func():confirm_new(n)))
	modal_box.add_child(button("Retour",show_title))
func level_name(number):
	var names=["Le laboratoire","Le département des machines","Le département d’optique","Le département des essais","Le défi de Folamour","Les serres expérimentales","Le service des photocopies","Le courrier interne","La salle de réunion","Le service des archives"]
	return loc("Chapitre %d · Niveau %d — %s") % [int((number-1)/5)+1,(number-1)%5+1,loc(names[number-1] if number<=10 else chapter3_data[str(number)].title if number<=15 else chapter4_data[str(number)].title if number<=20 else chapter5_data[str(number)].title)]

func confirm_new(target=1):
	if not has_save():
		start_game(false,target)
		return
	clear_modal("NOUVELLE PARTIE",loc("Commencer : %s ?") % level_name(target))
	paragraph("Cela remplacera la sauvegarde de la partie actuelle. Les anciennes sauvegardes 0.2 / 0.3 restent conservées séparément.")
	modal_box.add_child(button("Commencer",func(): start_game(false,target),true))
	modal_box.add_child(button("Retour",show_title))
func set_level(number):
	stop_navigation()
	signal_lights.clear()
	decor.clear()
	ambience_zone=-1
	level=clampi(number,1,25)
	archive_blocks.clear()
	if is_instance_valid(world):
		remove_child(world)
		world.queue_free()
	walls.clear()
	floors.clear()
	event_nodes.clear()
	door_bodies.clear()
	creature_bodies.clear()
	wall_bodies.clear()
	shortcut_nodes.clear()
	machine_parts.clear()
	var suffix="" if level==1 else str(level)
	level_data=JSON.parse_string(FileAccess.get_file_as_string("res://data/maze"+suffix+".json"))
	grid=level_data.grid
	start_cell=Vector2i(level_data.start[0],level_data.start[1])
	events=JSON.parse_string(FileAccess.get_file_as_string("res://data/events"+suffix+".json"))
	folamour=null
	LevelEndings.apply(self)
	Subject16.apply(self)
	shortcuts=JSON.parse_string(FileAccess.get_file_as_string("res://data/shortcuts"+suffix+".json"))
	item_catalog=JSON.parse_string(FileAccess.get_file_as_string("res://data/items"+suffix+".json")) if level>=2 else {}
	world=Node3D.new()
	add_child(world)
	build_world()
	if level==10:preload("res://ArchiveDecor.gd").setup(self)
	if level in range(11,16):preload("res://ForesightDecor.gd").setup(self)
	if level in range(16,21):preload("res://CertaintyDecor.gd").setup(self)
	if level>=21:preload("res://FinaleDecor.gd").setup(self)
	ChapterIdentity.setup(self)
func start_game(resume_v,target=1,keep_campaign=false):
	playing=false
	var data=read_save() if resume_v else {}
	if not data.is_empty(): target=int(data.get("level",1))
	if not keep_campaign:
		level_stats={}
		dossier=Subject16.blank()
	reaction_time=0
	last_observed_errors=0
	done.clear()
	seen.clear()
	journal.clear()
	journal_order.clear()
	walked.clear()
	open_shortcuts.clear()
	shortcut_cells.clear()
	dial_settings.clear()
	puzzle_states.clear()
	hints.clear()
	inventory={}
	elapsed=0
	errors=0
	auto_timer=0
	won=false
	nearest={}
	current_event={}
	set_level(target)
	if not data.is_empty(): load_game()
	dossier.visited[str(level)]=true
	last_observed_errors=errors
	sync_shortcuts()
	record_walk()
	playing=true
	hud.show()
	for e in events: sync_event(e)
	close_modal()
	update_fog()
	update_hud()
	update_camera(1)
	if data.is_empty():
		if level==1:
			add_journal("intro","EXPÉRIENCE 16\nRassemblez les trois disques et la fiche de calibration. I : objets ; J : découvertes. Les raccourcis se révèlent après un passage physique de chaque côté du mur.")
			clear_modal("NIVEAU 1 / LE LABORATOIRE","Bienvenue, sujet 16.")
			paragraph("« Volontaire, vous ? Peu importe. Votre consentement est admirablement implicite. Voyons comment vous vous débrouillez avec quelques portes. »")
			paragraph("Explorez le laboratoire. Approchez-vous des objets et terminaux puis appuyez sur E. Le journal conserve les découvertes.")
		elif level==2:
			add_journal("intro","DÉPARTEMENT DES MACHINES\nRemettre l’ascenseur en marche. Les établis assemblent les objets trouvés. Les conduites et manomètres indiquent les réglages. I : sac ; J : journal. Les ateliers restent accessibles après ouverture des portes.")
			clear_modal("NIVEAU 2 / SECTEUR DES MACHINES","Service de maintenance.")
			paragraph("« Vous avez trouvé la sortie. Très bien. Quelqu’un a malheureusement oublié de réparer l’ascenseur. Votre polyvalence tombe à point. »")
			paragraph("Votre ancien équipement a été consigné. Explorez les ateliers, assemblez les pièces et remettez les installations en service. Objectif : atteindre un ascenseur fonctionnel.")
		elif level==3:
			add_journal("intro","DÉPARTEMENT D’OPTIQUE\nRéparez le projecteur, calibrez les faisceaux puis déchiffrez les archives. Les formes et les textes permettent de résoudre les énigmes sans dépendre des couleurs.")
			clear_modal("NIVEAU 3 / DÉPARTEMENT D’OPTIQUE","Que la lumière soit.")
			paragraph("« Vous avez réparé mon ascenseur. Voyons maintenant si vous savez faire la lumière sur mes archives. »")
			paragraph("Explorez trois secteurs : le banc optique, la galerie des faisceaux et les archives. Retrouvez les pièces, recoupez les notes et ouvrez la chambre d’observation.")
		elif level==4:
			add_journal("intro","DÉPARTEMENT DES ESSAIS\nRépartissez les masses, retrouvez l’ordre des symboles et alimentez les cinq voyants. Les objets installés restent en place ; les manipulations sont réversibles et sauvegardées.")
			clear_modal("NIVEAU 4 / DÉPARTEMENT DES ESSAIS","La théorie ne suffit plus.")
			paragraph("« Aujourd’hui, vous manipulerez le matériel. Les formulaires de responsabilité sont déjà signés. Par moi. »")
			paragraph("Pesez, ordonnez, récupérez et inversez. Les notes donnent les règles ; les mécanismes vous laissent expérimenter sans perdre vos objets.")
		elif level==5:
			show_folamour_intro()
		elif level==6:show_greenhouse_intro()
		elif level==7:show_office_intro()
		elif level==8:show_mail_intro()
		elif level==9:show_meeting_intro()
		elif level==10:show_archive_intro()
		elif level<=15:ForesightChapter.intro(self)
		elif level<=20:CertaintyChapter.intro(self)
		else:FinaleChapter.intro(self)
		if level<5:modal_box.add_child(button("Commencer l’exploration",close_modal,true))
	elif level==5 and not won and not done.has("folamour_met"):
		show_folamour_intro()
	elif level==6 and not won and not done.has("g_met"):
		show_greenhouse_intro()
	elif level==7 and not won and not done.has("p_met"):
		show_office_intro()
	elif level==8 and not won and not done.has("m_met"):
		show_mail_intro()
	elif level==9 and not won and not done.has("r_met"):
		show_meeting_intro()
	elif level==10 and not won and not done.has("a_met"):
		show_archive_intro()
	elif level>=11 and not won and not done.has("c%d_met"%level):
		if level<=15:ForesightChapter.intro(self)
		elif level<=20:CertaintyChapter.intro(self)
		else:FinaleChapter.intro(self)
	save_game()
func _physics_process(delta):
	if not playing or modal_open or won or (is_instance_valid(soundscape) and not soundscape.focused): return
	elapsed+=delta
	var direction=Input.get_vector("west","east","north","south")
	var speed=MOVE_SPEED
	if direction.length()>0.1:
		stop_navigation()
	elif not move_path.is_empty():
		var target=Vector3(move_path[0].x*TILE,player.position.y,move_path[0].y*TILE)
		var offset=target-player.position
		if offset.length()<0.07:
			move_path.pop_front()
			if move_path.is_empty(): finish_navigation()
		else:
			direction=Vector2(offset.x,offset.z).normalized()
			speed=minf(MOVE_SPEED,offset.length()/delta)
	if modal_open: return
	var previous_position=player.position
	player.velocity=Vector3(direction.x*speed,-2,direction.y*speed)
	player.move_and_slide()
	if not move_path.is_empty():
		stuck_time=stuck_time+delta if player.position.distance_to(previous_position)<0.001 else 0.0
		if stuck_time>1.2:
			stop_navigation()
			toast("Passage bloqué. Choisissez une autre destination.")
	record_walk()
	if direction.length()>0.1:
		avatar.rotation.y=lerp_angle(avatar.rotation.y,atan2(-direction.x,-direction.y),delta*12)
		avatar.position.y=sin(elapsed*14)*0.035
	else: avatar.position.y=0
	update_camera(delta)
	fog_timer+=delta
	auto_timer+=delta
	toast_timer-=delta
	if toast_timer<=0: toast_label.text=""
	if fog_timer>0.18:
		fog_timer=0
		update_fog()
		find_nearest()
		update_hud()
	if auto_timer>4:
		auto_timer=0
		save_game()
	for e in events:
		if e.kind=="pickup" and not done.has(e.id): event_nodes[e.id].rotation.y+=delta*0.7
func _unhandled_input(event):
	if playing and not modal_open and not won:
		if event is InputEventMouseButton and event.pressed and event.button_index in [MOUSE_BUTTON_LEFT,MOUSE_BUTTON_RIGHT]:
			click_at(event.position)
			get_viewport().set_input_as_handled()
	if event is InputEventKey and event.pressed and event.keycode==KEY_F11:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if DisplayServer.window_get_mode()==DisplayServer.WINDOW_MODE_FULLSCREEN else DisplayServer.WINDOW_MODE_FULLSCREEN)
	if event is InputEventMouseButton and event.pressed and not modal_open:
		if event.button_index==MOUSE_BUTTON_WHEEL_UP: zoom=maxf(16.0,zoom-1.5)
		if event.button_index==MOUSE_BUTTON_WHEEL_DOWN: zoom=minf(48.0,zoom+1.5)
	if event.is_action_pressed("pause"):
		if modal_open and playing and not won: close_modal()
		elif playing: show_pause()
		return
	if not playing or modal_open: return
	if event.is_action_pressed("interact") and not nearest.is_empty(): interact(nearest)
	if event.is_action_pressed("map"): show_map()
	if event.is_action_pressed("journal"): show_journal()
	if event.is_action_pressed("inventory"): show_inventory()
func update_camera(delta):
	var target=player.position+Vector3(0,0.5,0)
	camera.position=camera.position.lerp(target+Vector3(13,19,13),min(1,delta*8))
	camera.look_at(target)
	camera.size=lerp(camera.size,zoom,min(1,delta*8))
func key(x,y): return str(int(x))+","+str(int(y))
func floor_at(x,y): return not archive_blocks.has(key(x,y)) and y>=0 and x>=0 and y<grid.size() and x<grid.size() and (grid[y][x]==1 or shortcut_cells.has(key(x,y)))
func zone(y,x=17):
	if level==21:return 0 if x<22 else 1 if y<17 else 2
	if level==22:return 2 if x in range(13,22) and y in range(13,22) else 1 if x in range(7,28) and y in range(7,28) else 0
	if level==23:return 0 if y<21 else 1 if x<17 else 2
	if level==24:return 2 if y>19 else 0 if x<15 else 1
	if level==25:return 0 if y<11 else 1 if y<23 else 2
	if level==16:return 0 if y<16 else 1 if x<17 else 2
	if level==17:return 0 if x<17 else 1 if y<17 else 2
	if level==18:return 2 if x in range(15,20) and y in range(15,20) else 1 if x in range(9,26) and y in range(9,26) else 0
	if level==19:return 0 if x<13 else 1 if x<25 else 2
	if level==20:return 1 if x<12 else 2 if x>22 else 0
	if level==11:return mini(2,int(x/12))
	if level==12:return mini(2,int(y/12))
	if level==13:return 1 if x>17 else 0 if y<17 else 2
	if level==14:return 2 if y>19 else 0 if x<17 else 1
	if level==15:return 1 if x<9 else 2 if x>25 else 0
	if level==10:return 0 if x<24 else 1 if y>17 else 2
	if level==9:return 0 if x<12 else 1 if x>23 else 2
	if level==8:return 2 if y>=28 else 0 if x<14 else 1
	if level==7:return 2 if y>=20 else 0 if x<17 else 1
	if level==6:return 0 if x<13 else 1 if x>23 else 2
	if level==5: return 2 if y<12 else 0 if x<15 else 1 if x>19 else 2
	return (0 if y<11 else (1 if y<24 else 2)) if level==1 else (0 if y<12 else (1 if y<24 else 2))
func update_fog():
	var px=int(round(player.position.x/TILE))
	var py=int(round(player.position.z/TILE))
	var frontier=[[px,py,0]]
	var visited={}
	for item in frontier:
		var x=item[0]
		var y=item[1]
		var k=key(x,y)
		if visited.has(k) or item[2]>7: continue
		visited[k]=true
		seen[k]=true
		if not floor_at(x,y): continue
		for d in [Vector2i(1,0),Vector2i(-1,0),Vector2i(0,1),Vector2i(0,-1)]: frontier.append([x+d.x,y+d.y,item[2]+1])
	for k in floors: floors[k].visible=render_near(floors[k]) and seen.has(k) and (not wall_bodies.has(k) or shortcut_cells.has(k))
	for k in walls:
		var w=walls[k]
		w.visible=render_near(w) and seen.has(k) and not shortcut_cells.has(k)
		if not w.visible:continue
		var diff=w.position-player.position
		w.scale.y=0.12 if diff.x+diff.z>0 and abs(diff.x-diff.z)<5 and Vector2(diff.x,diff.z).length()<7 else 1.0
	for e in events: event_nodes[e.id].visible=render_near(event_nodes[e.id]) and seen.has(key(e.cell[0],e.cell[1])) and not ((e.kind=="pickup" and done.has(e.id)) or (e.kind=="collectible" and Subject16.has(self,e)))
	for id in machine_parts:
		if id.begins_with("pipe_"): machine_parts[id].visible=seen.has(machine_parts[id].get_meta("fog_cell"))
	mini_map.queue_redraw()
func render_near(node):
	# Conservative horizontal radius covers maximum zoom in portrait and landscape.
	var radius=maxf(zoom,camera.size)*1.6+TILE*3
	return Vector2(node.global_position.x-player.position.x,node.global_position.z-player.position.z).length_squared()<radius*radius
func find_nearest():
	nearest={}
	var best=3.0
	for e in events:
		if e.kind=="collectible" and Subject16.has(self,e):continue
		if (e.kind=="pickup" or e.kind in ["door","exit"]) and done.has(e.id): continue
		var dist=player.position.distance_to(event_nodes[e.id].position)
		if dist<best:
			var mid=(player.position+event_nodes[e.id].position)/2
			if not floor_at(int(round(mid.x/TILE)),int(round(mid.z/TILE))): continue
			var query=PhysicsRayQueryParameters3D.create(player.position+Vector3(0,0.8,0),event_nodes[e.id].position+Vector3(0,0.8,0))
			query.exclude=[player.get_rid()]
			var hit=get_world_3d().direct_space_state.intersect_ray(query)
			if not hit.is_empty() and hit.collider!=door_bodies.get(e.id): continue
			best=dist
			nearest=e
func update_hud():
	title_label.text=loc((["N1 / OBSERVATION","N1 / DÉCISIONS","N1 / CONFINEMENT"] if level==1 else ["N2 / ATELIERS","N2 / HYDRAULIQUE","N2 / ASCENSEUR"])[zone(int(player.position.z/TILE))])
	if level==3: title_label.text=loc(["N3 / OPTIQUE","N3 / FAISCEAUX","N3 / ARCHIVES"][zone(int(player.position.z/TILE))])
	if level==4: title_label.text=loc(["N4 / MASSES","N4 / SÉQUENCES","N4 / CIRCUITS"][zone(int(player.position.z/TILE))])
	var held=0
	for amount in inventory.values(): held+=int(amount)
	status_label.text=loc("Objets  %d    •    Disques récupérés  %d / 3    •    %02d:%02d") % [held,int(done.has("disc_sun"))+int(done.has("disc_moon"))+int(done.has("disc_star")),int(elapsed)/60,int(elapsed)%60]
	if level==2: status_label.text=loc("Objets  %d    •    Installations  %d / 4    •    %02d:%02d") % [held,int(done.has("generator"))+int(done.has("water_manifold"))+int(done.has("hoist"))+int(done.has("lift_power")),int(elapsed)/60,int(elapsed)%60]
	if level==3: status_label.text=loc("Objets  %d    •    Installations  %d / 3    •    %02d:%02d") % [held,int(done.has("projector"))+int(done.has("beam_router"))+int(done.has("archive_reader")),int(elapsed)/60,int(elapsed)%60]
	if level==5: title_label.text=loc("N5 / "+("PROTOTYPE" if player.position.z<12*TILE else "DOSAGE" if player.position.x<15*TILE else "TRANSFERT" if player.position.x>19*TILE else "HALL CENTRAL"))
	if level==5: status_label.text=loc("Objets  %d    •    Essais  %d / 3    •    %02d:%02d") % [held,int(done.has("f_dosing"))+int(done.has("f_tower"))+int(done.has("f_rotors")),int(elapsed)/60,int(elapsed)%60]
	if level==6:
		title_label.text=loc("C2 / MISSION 1 / LES SERRES")
		status_label.text=loc("Objets  %d    •    Essais  %d / 3    •    %02d:%02d") % [held,int(done.has("g_irrigation"))+int(done.has("g_growth"))+int(done.has("g_blend")),int(elapsed)/60,int(elapsed)%60]
	if level==7:
		title_label.text=loc("C2 / MISSION 2 / PHOTOCOPIES")
		status_label.text=loc("Objets  %d    •    Essais  %d / 3    •    %02d:%02d") % [held,int(done.has("p_overlay"))+int(done.has("p_filing"))+int(done.has("p_copier")),int(elapsed)/60,int(elapsed)%60]
	if level==8:
		title_label.text=loc("C2 / MISSION 3 / COURRIER")
		status_label.text=loc("Objets  %d    •    Essais  %d / 3    •    %02d:%02d") % [held,int(done.has("m_balance"))+int(done.has("m_network"))+int(done.has("m_address")),int(elapsed)/60,int(elapsed)%60]
	if level==9:
		title_label.text=loc("C2 / MISSION 4 / RÉUNION")
		status_label.text=loc("Objets  %d    •    Essais  %d / 3    •    %02d:%02d") % [held,int(done.has("r_seating"))+int(done.has("r_schedule"))+int(done.has("r_conference")),int(elapsed)/60,int(elapsed)%60]
	if level==10:
		title_label.text=loc("C2 / MISSION 5 / ARCHIVES")
		status_label.text=loc("Objets  %d    •    Essais  %d / 3    •    %02d:%02d") % [held,int(done.has("a_stacks"))+int(done.has("a_reports"))+int(done.has("a_twin")),int(elapsed)/60,int(elapsed)%60]
	if level>=11:
		title_label.text=loc("C3 / MISSION %d" if level<=15 else "C4 / MISSION %d")%((level-1)%5+1)
		status_label.text=loc("Objets  %d    •    Essais  %d / 3    •    %02d:%02d")%[held,int(done.has("c%d_p1"%level))+int(done.has("c%d_p2"%level))+int(done.has("c%d_p3"%level)),int(elapsed)/60,int(elapsed)%60]
	if level>=21:title_label.text=loc(FinaleChapter.status(self))
	if level==4: status_label.text=loc("Objets  %d    •    Essais  %d / 3    •    %02d:%02d") % [held,int(done.has("test_balance"))+int(done.has("sequence_panel"))+int(done.has("test_circuit")),int(elapsed)/60,int(elapsed)%60]
	status_label.text+="   ◇ "+str(Subject16.count(self,level))+"/10"
	action_label.text=loc("["+nearest.ref+"] "+nearest.title if not nearest.is_empty() else "Cliquez / touchez le sol pour explorer")
	if not move_path.is_empty(): action_label.text=loc("Destination : ")+ (loc(click_event.title) if not click_event.is_empty() else str(move_path[-1].x)+", "+str(move_path[-1].y))
	if is_instance_valid(interact_button):
		interact_button.disabled=nearest.is_empty()
		interact_button.text=loc("Parler" if LevelEndings.is_doctor(nearest) else "Examiner" if nearest.is_empty() or nearest.kind not in ["pickup","collectible"] else "Ramasser")
func toast(text):
	toast_source=text
	toast_label.text=loc(text)
	toast_timer=6
func interact(e):
	if e.kind=="collectible":
		Subject16.collect(self,e)
		return
	if won and level==25:
		FinaleChapter.finish(self)
		Subject16.finish_button(self)
		return
	if e.kind=="pickup":
		for required in e.get("prerequisites",[]):
			if not done.has(required):
				show_puzzle(e)
				return
		if done.has(e.id): return
		inventory[e.resource]=inventory.get(e.resource,0)+e.get("amount",1)
		add_journal(e.id,e.title+"\n"+e.text)
		done[e.id]=true
		sync_event(e)
		toast(e.title+" ajouté à l'inventaire.")
		clear_modal(e.ref+" / OBJET RÉCUPÉRÉ",e.title)
		paragraph(e.text)
		modal_box.add_child(button("Ranger dans le sac",close_modal,true))
		chime(660)
		find_nearest()
		update_hud()
		save_game()
		return
	if e.kind=="clue":
		add_journal(e.id,e.title+"\n"+e.text)
		done[e.id]=true
		clear_modal(e.get("ref","?")+" / JOURNAL MIS À JOUR",e.title)
		paragraph(e.text)
		modal_box.add_child(button("Continuer",close_modal,true))
		chime(440)
		save_game()
		return
	if e.kind=="oneway":
		open_oneway(e)
		return
	show_puzzle(e)
func item_name(id):
	if item_catalog.has(id): return item_catalog[id].title
	for e in events:
		if e.id==id: return e.title
	return id
func held_all(ids):
	for id in ids:
		if inventory.get(id,0)<1: return false
	return true
func show_puzzle(e):
	if LevelEndings.is_doctor(e):
		LevelEndings.show_dialogue(self,e)
		return
	current_event=e
	clear_modal(e.get("ref","?")+" / MÉCANISME",e.title)
	paragraph(e.get("installed_text",e.text) if done.has("installed_"+e.id) else e.text)
	if done.has(e.id):
		paragraph("Mécanisme déjà activé. Vous pouvez poursuivre.")
		modal_box.add_child(button("Retour",close_modal,true))
		return
	modal_box.add_child(button("Indice facultatif",func(): show_hint(e)))
	for id in e.get("prerequisites",[]):
		if not done.has(id):
			paragraph("Installation requise : "+item_name(id)+".",17)
			modal_box.add_child(button("Revenir explorer",close_modal))
			return
	if e.has("controlled_by"):
		paragraph("Commande reliée à : "+item_name(e.controlled_by)+".",17)
		modal_box.add_child(button("Revenir explorer",close_modal))
		return
	var installed=done.has("installed_"+e.id)
	if e.has("requires") and not installed:
		for id in e.requires:
			paragraph(("✓  " if inventory.get(id,0)>0 else "—  ")+item_name(id),17)
		var b=button(e.get("action","Installer les objets" if e.requires.size()>1 else "Utiliser "+item_name(e.requires[0])),func(): install_items(e),true)
		b.disabled=not held_all(e.requires)
		modal_box.add_child(b)
	elif e.has("puzzle_type"):
		PuzzleControls.render(self,e)
	elif e.has("dials"):
		paragraph(e.question,17)
		if not dial_settings.has(e.id): dial_settings[e.id]=[0,0,0]
		var row=HBoxContainer.new()
		row.add_theme_constant_override("separation",14)
		modal_box.add_child(row)
		for i in range(e.dials.size()):
			var b=button(e.dials[i]+"\n"+str(int(dial_settings[e.id][i])),func(): cycle_dial(e,i))
			b.size_flags_horizontal=Control.SIZE_EXPAND_FILL
			b.custom_minimum_size.y=75
			row.add_child(b)
		paragraph("Cliquez sur une molette pour passer de 0 à 3.",15)
		modal_box.add_child(button("Mettre le circuit en service",submit_answer,true))
		feedback=paragraph("",15)
		modal_box.add_child(button("Consulter le journal",func(): show_journal(e)))
	elif e.has("answer"):
		if installed: paragraph("Les objets sont installés. Leurs descriptions restent dans votre journal.",16)
		paragraph(e.question,17)
		code_entry=LineEdit.new()
		code_entry.placeholder_text=loc("Code…")
		code_entry.custom_minimum_size.y=46
		code_entry.max_length=12
		code_entry.virtual_keyboard_type=LineEdit.KEYBOARD_TYPE_NUMBER
		modal_box.add_child(code_entry)
		if ui_mobile or OS.has_feature("web"):
			code_entry.editable=false
			build_code_keypad()
		code_entry.text_submitted.connect(func(_v): submit_answer())
		modal_box.add_child(button("Valider",submit_answer,true))
		feedback=paragraph("",15)
		modal_box.add_child(button("Consulter les indices du journal",func(): show_journal(e)))
		code_entry.grab_focus()
	elif not e.has("requires"):
		modal_box.add_child(button(e.get("action","Actionner le mécanisme"),func(): complete(e),true))
	modal_box.add_child(button("Revenir explorer",close_modal))
func cycle_dial(e,index):
	dial_settings[e.id][index]=(int(dial_settings[e.id][index])+1)%4
	show_puzzle(e)
	save_game()
func normalize(text): return str(text).strip_edges().replace(" ","")
func submit_answer():
	if current_event.is_empty() or not current_event.has("answer"): return
	if current_event.has("requires") and not done.has("installed_"+current_event.id): return
	for id in current_event.get("prerequisites",[]):
		if not done.has(id): return
	var response=code_entry.text if not current_event.has("dials") else ""
	if current_event.has("dials"):
		for value in dial_settings.get(current_event.id,[0,0,0]): response+=str(int(value))
	if normalize(response)==normalize(current_event.answer): complete(current_event)
	else:
		errors+=1
		feedback.text=loc("Le mécanisme refuse ce code. Vérifiez les indices recueillis.")
		chime(170)
		save_game()
func install_items(e):
	if done.has(e.id) or done.has("installed_"+e.id) or not held_all(e.get("requires",[])): return
	for id in e.get("prerequisites",[]):
		if not done.has(id): return
	for id in e.requires: inventory[id]-=1
	done["installed_"+e.id]=true
	sync_event(e)
	add_journal("installed_"+e.id,e.title+(" — objets remis à Folamour. Descriptions conservées dans le journal." if LevelEndings.is_doctor(e) else " — pièces assemblées ou installées. Descriptions conservées dans le journal."))
	if e.has("answer") or e.has("puzzle_type"):
		show_puzzle(e)
		update_hud()
		save_game()
	else: complete(e)
func open_target(id):
	done[id]=true
	for other in events:
		if other.id==id: sync_event(other)
func complete(e):
	if done.has(e.id): return
	if LevelEndings.is_doctor(e):
		if not LevelEndings.ready(self,e):return
		if e.has("requires") and not done.has("installed_"+e.id):return
	if e.has("puzzle_type") and (not PuzzleControls.available(self,e) or not PuzzleControls.solved(self,e)): return
	done[e.id]=true
	if Guidance.is_challenge(e):Subject16.react(self,"success",e.id)
	for id in e.get("grants",{}):
		inventory[id]=inventory.get(id,0)+e.grants[id]
		add_journal("object_"+id,item_name(id)+"\n"+item_catalog.get(id,{}).get("text","Objet assemblé."))
	add_journal(e.id,e.title+"\n"+e.get("success","Mécanisme activé."))
	for target in e.get("opens",[]): open_target(target)
	sync_event(e)
	chime(880)
	if is_instance_valid(soundscape):soundscape.effect(self,"success" if LevelEndings.is_doctor(e) else "door" if e.kind in ["door","exit"] or e.has("opens") else "machine")
	close_modal()
	toast(e.get("success","Le passage est ouvert."))
	update_hud()
	save_game()
	if e.kind=="exit": show_win()
	elif level>=21:FinaleChapter.checkpoint(self,e)
func sync_event(e):
	if e.kind=="collectible":
		event_nodes[e.id].visible=not Subject16.has(self,e)
		event_nodes[e.id].get_node("PickArea").collision_layer=0 if Subject16.has(self,e) else 2
		return
	if e.id=="g_bridge":
		var bridge=event_nodes[e.id].get_node_or_null("LivingBridge")
		if bridge:bridge.visible=done.has(e.id)
	if e.has("puzzle_type"): PuzzleControls.sync(self,e)
	for child in event_nodes[e.id].get_children():
		if str(child.name).begins_with("Socket"):
			child.material_override=material(accent if done.has("installed_"+e.id) else Color("101f29"))
	if signal_lights.has(e.id):
		var active=done.has(e.id)
		var installed=done.has("installed_"+e.id)
		signal_lights[e.id].material_override=material(Color("6cdda2") if active else Color("e9be72") if installed else Color("db735e"),true)
	if e.kind=="pickup":
		event_nodes[e.id].visible=not done.has(e.id)
		event_nodes[e.id].get_node("PickArea").collision_layer=0 if done.has(e.id) else 2
	if creature_bodies.has(e.id):
		creature_bodies[e.id].collision_layer=0 if done.has(e.id) else 1
		event_nodes[e.id].scale.y=0.5 if done.has(e.id) else 1.0
	if door_bodies.has(e.id):
		door_bodies[e.id].collision_layer=0 if done.has(e.id) and e.kind!="oneway" else 1
		var leaf=event_nodes[e.id].get_node("Leaf")
		leaf.scale.y=0.05 if done.has(e.id) else 1
		leaf.position.y=2.42 if done.has(e.id) else 1.17
func missing_for_sas(e):
	var missing=[]
	for id in e.get("carry",[]):
		if inventory.get(id,0)<1: missing.append(id)
	for id in e.get("records",[]):
		if not done.has(id): missing.append(id)
	return missing
func sas_entry_side(e):
	var p=Vector2(player.position.x/TILE,player.position.z/TILE)
	var c=Vector2(e.cell[0],e.cell[1])
	var d=Vector2(e.direction[0],e.direction[1])
	return (p-c).dot(d)<-0.15 and abs((p-c).cross(d))<0.7 and (p-c).length()<1.8
func open_oneway(e):
	if not sas_entry_side(e):
		clear_modal("50 / SAS À SENS UNIQUE","Accès interdit de ce côté")
		paragraph("Le sas mène uniquement vers le confinement. Son verrou reste fermé du côté de la sortie.")
		modal_box.add_child(button("Retour",close_modal))
		return
	clear_modal("50 / CONTRÔLE AVANT CONFINEMENT",e.title)
	var missing=missing_for_sas(e)
	if not missing.is_empty():
		paragraph("Le scanner refuse le départ : vous ne pourriez pas terminer l’expérience avec cet équipement. Récupérez les éléments suivants avant de quitter le laboratoire.",17)
		for id in missing: paragraph("—  "+item_name(id),16)
		modal_box.add_child(button("Aide au départ : où poursuivre la recherche ?",func(): sas_hint(e,missing)))
	else:
		paragraph("Trois disques détectés. Fiche de calibration archivée. Vous gardez votre sac et votre journal. Ce sas ne permet aucun retour vers les ateliers.")
		modal_box.add_child(button("Entrer dans le confinement",func(): transit_sas(e),true))
	modal_box.add_child(button("Rester de ce côté",close_modal))
func sas_hint(e,missing):
	var locations={"disc_sun":"Soleil : réserve au nord, serrure de cuivre. Sa clé se trouve dans le dépôt près de l’accès 03.","disc_star":"Étoile : atelier optique au centre. Consultez les deux fiches de maintenance, au nord-ouest et au nord-est.","disc_moon":"Lune : chambre à l’ouest. L’artéfact de résonance a été déposé à l’est du laboratoire.","exit_protocol":"Calibration : cherchez le terminal 20 dans le cul-de-sac à l’extrémité nord-est."}
	clear_modal("AIDE AU DÉPART / AUCUN VERROU OUVERT","Compléter votre préparation")
	hints["sas_depart"]=1
	for id in missing:
		paragraph(locations[id],17)
		add_journal("aide_"+id,locations[id])
	modal_box.add_child(button("Retour au contrôle",func(): open_oneway(e),true))
	save_game()
func transit_sas(e):
	if not sas_entry_side(e) or not missing_for_sas(e).is_empty(): return
	var c=Vector2(e.cell[0],e.cell[1])
	var d=Vector2(e.direction[0],e.direction[1])
	player.position=Vector3((c.x+d.x)*TILE,0.1,(c.y+d.y)*TILE)
	player.velocity=Vector3.ZERO
	record_walk()
	add_journal(e.id,e.title+" — franchi vers le confinement. Inventaire conservé.")
	done["traversed_"+e.id]=true
	close_modal()
	update_camera(1)
	update_fog()
	find_nearest()
	save_game()
	chime(520)
func show_inventory():
	clear_modal("I / OBJETS TRANSPORTÉS","Votre sac")
	var scroll=ScrollContainer.new()
	scroll.custom_minimum_size=Vector2(content_width(),260 if ui_mobile else 350)
	modal_box.add_child(scroll)
	var entries=VBoxContainer.new()
	entries.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	entries.add_theme_constant_override("separation",16)
	scroll.add_child(entries)
	var count=0
	for id in inventory:
		if inventory.get(id,0)<1: continue
		var text=item_catalog.get(id,{}).get("text","")
		for e in events:
			if e.id==id: text=e.text
		var l=label(reference_name(id)+"\n"+text,17)
		l.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
		l.size_flags_horizontal=Control.SIZE_EXPAND_FILL
		entries.add_child(l)
		count+=1
	if count==0: entries.add_child(label("Votre sac est vide.",18))
	paragraph("Les objets installés restent dans leur mécanisme. Les indices et descriptions sont conservés dans le journal.",15)
	modal_box.add_child(button("Reprendre",close_modal,true))
func show_journal(return_to={}):
	clear_modal("PLUS RÉCENT EN PREMIER","Journal d’exploration")
	modal_box.add_child(button("Objectif actuel",show_objective))
	for e in events:
		if int(hints.get(e.id,0))>0:
			var hint_event=e
			modal_box.add_child(button(loc("Indices consultés : ")+loc(e.title),func(): show_hint(hint_event,null,false)))
	var scroll=ScrollContainer.new()
	scroll.custom_minimum_size=Vector2(content_width(),300 if ui_mobile else 390)
	modal_box.add_child(scroll)
	var entries=VBoxContainer.new()
	entries.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	entries.add_theme_constant_override("separation",18)
	scroll.add_child(entries)
	for k in recent_journal_keys():
		var l=label(journal_entry(k),17)
		l.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
		l.size_flags_horizontal=Control.SIZE_EXPAND_FILL
		entries.add_child(l)
	if not return_to.is_empty(): modal_box.add_child(button("Retour au mécanisme",func(): show_puzzle(return_to),true))
	else: modal_box.add_child(button("Reprendre",close_modal,true))
func show_map():
	var preview_path=move_path.duplicate()
	clear_modal("CARTOGRAPHIE / ZONES DÉCOUVERTES","Votre progression")
	var map=MapWidget.new()
	map.game=self
	map.route_preview=preview_path
	map.navigation_enabled=true
	map.custom_minimum_size=Vector2(content_width(),content_width()*0.82)
	modal_box.add_child(map)
	paragraph("Clic gauche ou droit sur un passage découvert : fermer la carte et s’y rendre.",14)
	paragraph("Blanc : vous • Or : objet • Turquoise : indice\nBleu : mécanisme • Corail : porte • Vert : activé\nF : Folamour, fin de mission • Cercle blanc : collectible\nLes zones inconnues restent cachées.",14)
	modal_box.add_child(button("Reprendre",close_modal,true))
func show_pause():
	if not playing: return
	clear_modal("EXPÉRIENCE EN PAUSE","Prenez votre temps.")
	save_game()
	paragraph("Sauvegarde automatique toutes les 4 secondes et après chaque action. Le chronomètre s’arrête dans les menus et pendant la lecture.")
	paragraph(save_status,15)
	paragraph("Les raccourcis se révèlent après un passage physique des deux côtés du même mur. Ils restent ouverts dans les deux sens. La carte seule ne suffit pas.",16)
	modal_box.add_child(button("Reprendre",close_modal,true))
	modal_box.add_child(button("Journal",show_journal))
	modal_box.add_child(button("Langue / Language",func(): show_language(true)))
	modal_box.add_child(button("Objectif actuel",show_objective))
	modal_box.add_child(button("Réglages audio",func(): show_audio(true)))
	modal_box.add_child(button("Dossier du sujet 16",func():Subject16.show(self)))
	modal_box.add_child(button("Animations décoratives : OUI" if decorative_motion else "Animations décoratives : NON",func(): decorative_motion=not decorative_motion; save_game(); show_pause()))
	modal_box.add_child(button("Répliques de Folamour : OUI" if folamour_comments else "Répliques de Folamour : NON",func(): folamour_comments=not folamour_comments; save_game(); show_pause()))
	modal_box.add_child(button("Sauvegarder et revenir au menu",func(): save_game(); show_title()))
	if not OS.has_feature("web"): modal_box.add_child(button("Sauvegarder et quitter",func(): save_game(); get_tree().quit()))
func show_win():
	won=true
	var h=0
	var secrets=0
	for value in hints.values(): h+=int(value)
	for e in events:
		if e.get("secret",false) and done.has(e.id): secrets+=1
	var puzzles=0
	for e in events:
		if Guidance.is_challenge(e) and done.has(e.id):puzzles+=1
	var first_completion=not level_stats.has(str(level))
	level_stats[str(level)]={"time":elapsed,"secrets":secrets,"hints":h,"errors":errors,"puzzles":puzzles,"shortcuts":open_shortcuts.size()}
	if first_completion and level in [5,10,15,20,25] and is_instance_valid(soundscape):soundscape.effect(self,"chapter_complete")
	save_game()
	if level>=21:
		FinaleChapter.finish(self)
		Subject16.finish_button(self)
		return
	if level>=16:
		CertaintyChapter.finish(self)
		Subject16.finish_button(self)
		return
	if level>=11:
		ForesightChapter.finish(self)
		Subject16.finish_button(self)
		return
	if level==10:
		show_archive_win()
		Subject16.finish_button(self)
		return
	if level==9:
		show_meeting_win()
		Subject16.finish_button(self)
		return
	if level==8:
		show_mail_win()
		Subject16.finish_button(self)
		return
	if level==7:
		show_office_win()
		Subject16.finish_button(self)
		return
	if level==6:
		show_greenhouse_win()
		Subject16.finish_button(self)
		return
	clear_modal("NIVEAU "+str(level)+" / TERMINÉ", "Le laboratoire est franchi." if level==1 else "L’ascenseur est en marche." if level==2 else "Le ciel vous appartient." if level==3 else "Essais réussis." if level==4 else "Le défi impossible est accompli.")
	if level==5:
		clear_modal("CHAPITRE 1 / TERMINÉ","Le défi impossible est accompli.")
		folamour_portrait()
		paragraph("Folamour écoute votre rapport. Pour la première fois, il semble à court de sarcasmes.",16)
		paragraph("« Vous avez réussi. ZÉRO est stable… Personne n’y était jamais arrivé. Félicitations, sujet 16. Vous pouvez être fier de vous. »",21)
		paragraph("Il remet ses lunettes, puis retrouve son sourire habituel.",16)
		paragraph("« Un tel talent mérite une proposition exceptionnelle : un stage dans mon laboratoire ! Non rémunéré, évidemment. Vous ne voudriez tout de même pas fausser l’expérience avec de l’argent ? »",21)
		paragraph("FIN DU CHAPITRE 1 — Le labyrinthe de Folamour",20)
	else:
		paragraph("« Le prochain département sera ravi de vous recevoir. »" if level==1 else "« Vous avez réparé l’ascenseur. Et sans réclamer de salaire. Une expérience remarquable. »" if level==2 else "« Vous pouvez admirer le ciel. La fenêtre ne constitue pas une autorisation de congé. »" if level==3 else "« Certification accordée. Le service des ressources humaines vous considère désormais comme une ressource. »",21)
	paragraph(loc("Temps du niveau : %02d:%02d\nSecrets : %d / 3    •    Tentatives incorrectes : %d") % [int(elapsed)/60,int(elapsed)%60,secrets,errors],20)
	paragraph(loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d") % [puzzles,open_shortcuts.size(),h],17)
	if level==1:
		paragraph("La suite : le secteur des machines. Votre inventaire sera remis à zéro. Le bilan du laboratoire sera conservé et la transition sera sauvegardée.",17)
		modal_box.add_child(button("Continuer vers le niveau 2",func(): start_game(false,2,true),true))
	elif level==2:
		paragraph("La suite : le département d’optique. Votre inventaire sera remis à zéro ; les bilans précédents seront conservés.",17)
		modal_box.add_child(button("Continuer vers le niveau 3",func(): start_game(false,3,true),true))
	elif level==3:
		paragraph("La suite : le département des essais. Le sac et les notes seront remis à zéro ; les bilans restent conservés.",17)
		modal_box.add_child(button("Continuer vers le niveau 4",func(): start_game(false,4,true),true))
	elif level==4:
		paragraph("La suite : le défi personnel de Folamour. Dernière étape du chapitre 1 ; les bilans précédents restent conservés.",17)
		modal_box.add_child(button("Continuer vers le niveau 5",func(): start_game(false,5,true),true))
	else:
		var total=0.0
		var found=0
		for stat in level_stats.values():
			total+=stat.time
			found+=int(stat.secrets)
		paragraph(loc("Bilan : %d niveau(x) terminé(s), %02d:%02d d’exploration, %d secrets.") % [level_stats.size(),int(total)/60,int(total)%60,found],17)
		var summary=Guidance.summary(self)
		paragraph("DOSSIER DE CANDIDATURE",20)
		paragraph(loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d") % [summary.puzzles,summary.shortcuts,summary.hints],17)
		if summary.tracked<summary.levels:paragraph("Certaines anciennes sauvegardes ne contiennent pas le détail des énigmes et raccourcis des niveaux précédents. Ces totaux couvrent seulement les niveaux enregistrés avec le nouveau bilan.",15)
		if summary.levels<5:paragraph("Bilan partiel : seuls les niveaux terminés dans cette partie sont comptabilisés.",15)
		paragraph("« Votre candidature est retenue. Sens de l’initiative : excellent. Prétentions salariales : nous préférons ne pas les mesurer. » — Folamour",19)
		modal_box.add_child(button("Accepter le stage — Chapitre 2",func(): start_game(false,6,true),true))
		modal_box.add_child(button("Choisir un chapitre",func(): playing=false; hud.hide(); show_chapters(),true))
		modal_box.add_child(button("Recommencer le chapitre 1",func(): confirm_new(1)))
	Subject16.finish_button(self)
	modal_box.add_child(button("Sauvegarder et revenir au menu",show_title))
func save_game():
	if test_mode: return
	var data={"version":4,"subject16":dossier,"decorative_motion":decorative_motion,"folamour_comments":folamour_comments,"shortcut_layout_revision":SHORTCUT_LAYOUT_REVISION,"level":level,"level_stats":level_stats,"dial_settings":dial_settings,"puzzle_states":puzzle_states,"walked":walked,"open_shortcuts":open_shortcuts,"journal_order":journal_order,"position":[player.position.x,player.position.y,player.position.z],"seen":seen,"done":done,"journal":journal,"hints":hints,"inventory":inventory,"elapsed":elapsed,"errors":errors,"won":won,"zoom":zoom,"muted":muted}
	var f=FileAccess.open(SAVE+".tmp",FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(data))
		var write_error=f.get_error()
		f.close()
		if write_error!=OK:
			save_status="Sauvegarde impossible : espace de stockage indisponible."
			return
		if FileAccess.file_exists(SAVE):
			var old=JSON.new()
			if old.parse(FileAccess.get_file_as_string(SAVE))==OK and old.data is Dictionary: DirAccess.copy_absolute(SAVE,SAVE+".bak")
		var result=DirAccess.rename_absolute(SAVE+".tmp",SAVE)
		save_status="Progression sauvegardée sur cet appareil." if result==OK else "Sauvegarde impossible : espace de stockage indisponible."
	else:
		save_status="Sauvegarde impossible : espace de stockage indisponible."
func load_game():
	var data=read_save()
	if data.is_empty(): return
	level_stats=data.get("level_stats",{})
	dossier=data.get("subject16",Subject16.blank())
	for field in ["collection","observations","visited"]:
		if not dossier.has(field):dossier[field]={}
	decorative_motion=data.get("decorative_motion",true)
	folamour_comments=data.get("folamour_comments",true)
	dial_settings=data.get("dial_settings",{})
	puzzle_states=data.get("puzzle_states",{})
	won=data.get("won",false)
	seen=data.get("seen",{})
	done=data.get("done",{})
	journal=data.get("journal",{})
	journal_order=data.get("journal_order",journal.keys())
	walked=data.get("walked",{})
	restore_shortcuts(data)
	sync_shortcuts()
	hints=data.get("hints",{})
	for id in hints:hints[id]=clampi(int(hints[id]),0,3)
	inventory=data.get("inventory",{})
	elapsed=data.get("elapsed",0)
	errors=data.get("errors",0)
	zoom=data.get("zoom",22)
	muted=soundscape.preference_muted if FileAccess.file_exists(soundscape.SETTINGS) else data.get("muted",false)
	var p=data.get("position",[start_cell.x*TILE,0.1,start_cell.y*TILE])
	if floor_at(int(round(p[0]/TILE)),int(round(p[2]/TILE))): player.position=Vector3(p[0],0.1,p[2])
	else:
		# A checkpoint may be inside a shortcut wall removed by the new layout.
		# Restore to the nearest already-walked base-floor cell, never unknown ground.
		var best=INF
		for y in range(grid.size()):
			for x in range(grid[y].size()):
				if grid[y][x]==0 or not walked.has(key(x,y)):continue
				var candidate=Vector3(x*TILE,0.1,y*TILE)
				var distance=candidate.distance_squared_to(Vector3(p[0],0.1,p[2]))
				if distance<best:best=distance;player.position=candidate
	if data.get("won",false): call_deferred("show_win")
func restore_shortcuts(data):
	open_shortcuts={}
	var migrated=int(data.get("shortcut_layout_revision",0))!=SHORTCUT_LAYOUT_REVISION
	for sc in shortcuts:
		if migrated:
			journal.erase(sc.id)
			journal_order.erase(sc.id)
		# IDs alone are insufficient after a relocation. Both current sides must
		# have been physically visited; fog visibility never unlocks a shortcut.
		if walked.has(key(sc.sides[0][0],sc.sides[0][1])) and walked.has(key(sc.sides[1][0],sc.sides[1][1])):
			open_shortcuts[sc.id]=true
			seen[key(sc.cell[0],sc.cell[1])]=true
			if migrated or not journal.has(sc.id):
				journal[sc.id]="Raccourci "+sc.id+" révélé\nVous avez parcouru les deux côtés du mur. Ce passage reste ouvert dans les deux sens et apparaît sur la carte."
				if not journal_order.has(sc.id):journal_order.append(sc.id)
func chime(frequency):
	if muted or test_mode or (is_instance_valid(soundscape) and soundscape.gain(self,"effects")<=0): return
	var tone="success" if frequency>=800 else "error" if frequency<200 else "pickup" if frequency>=600 else "read"
	audio.stream=load("res://assets/"+tone+".wav")
	audio.play()
func _notification(what):
	if is_instance_valid(soundscape):
		if what in [NOTIFICATION_APPLICATION_PAUSED,NOTIFICATION_APPLICATION_FOCUS_OUT]:soundscape.focused=false
		elif what in [NOTIFICATION_APPLICATION_RESUMED,NOTIFICATION_APPLICATION_FOCUS_IN]:soundscape.focused=true
	if what in [NOTIFICATION_WM_CLOSE_REQUEST,NOTIFICATION_APPLICATION_PAUSED,NOTIFICATION_APPLICATION_FOCUS_OUT] and playing: save_game()
func verify_game():
	# Full physical and progression regression tests live in tests/verify_v02.gd.
	var ok=true
	for e in events:
		if not floor_at(e.cell[0],e.cell[1]): ok=false
		if e.kind=="pickup":
			var before=inventory.get(e.resource,0)
			interact(e)
			interact(e)
			if inventory[e.resource]!=before+1: ok=false
	print("VERIFY_ITEMS: ","PASS" if ok else "FAIL")
	get_tree().quit(0 if ok else 1)
func capture_preview():
	await get_tree().create_timer(2).timeout
	get_viewport().get_texture().get_image().save_png("../deliverables/Apercu-prototype.png")
	show_title()
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("../tools/title.png")
	for e in events:
		if e.id=="star_vault": show_puzzle(e)
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("../tools/puzzle.png")
	get_tree().quit()

func build_machine(root,e,gold,dark):
	var metal=material(Color("708994"))
	match e.model:
		"dosing":
			box(root,Vector3(1.9,0.22,1),Vector3(0,0.18,0),metal)
			for i in range(2):
				var x=(i-0.5)*1.0
				for side in [-0.35,0.35]:box(root,Vector3(0.07,1.2,0.65),Vector3(x+side,0.9,0),gold)
				var liquid=box(root,Vector3(0.6,1,0.55),Vector3(x,0.8,0),material(Color("78d9df"),true))
				liquid.name="Liquid"+str(i)
		"tower":
			box(root,Vector3(2.3,0.2,1),Vector3(0,0.18,0),metal)
			for i in range(3):box(root,Vector3(0.08,1.2,0.08),Vector3((i-1)*0.75,0.9,0),gold)
			for i in range(3):
				var disc=box(root,Vector3(0.3+i*0.19,0.18,0.3+i*0.19),Vector3.ZERO,material([Color("cde9ec"),Color("e9be72"),Color("b49ada")][i]))
				disc.name="Disc"+str(i)
		"rotors":
			box(root,Vector3(2.3,0.3,1.1),Vector3(0,0.7,0),metal)
			for i in range(3):
				var rotor=Node3D.new()
				rotor.name="Rotor"+str(i)
				root.add_child(rotor)
				rotor.position=Vector3((i-1)*0.75,0.95,0)
				box(rotor,Vector3(0.08,0.08,0.65),Vector3.ZERO,gold)
				box(rotor,Vector3(0.22,0.08,0.12),Vector3(0,0,-0.28),gold)
		"balance":
			box(root,Vector3(1.5,0.18,1),Vector3(0,0.12,0),metal)
			box(root,Vector3(0.16,1.3,0.16),Vector3(0,0.8,0),gold)
			var beam=Node3D.new()
			beam.name="BalanceBeam"
			beam.position.y=1.5
			root.add_child(beam)
			box(beam,Vector3(1.8,0.1,0.1),Vector3.ZERO,gold)
			for x in [-0.7,0.7]:
				box(beam,Vector3(0.04,0.45,0.04),Vector3(x,-0.22,0),metal)
				box(beam,Vector3(0.65,0.09,0.6),Vector3(x,-0.47,0),gold)
			for i in range(4):
				var weight=box(root,Vector3(0.18,0.14+0.025*i,0.18),Vector3((i-1.5)*0.3,0.33,0.35),gold)
				weight.name="PlacedWeight"+str(i)
				weight.hide()
		"sequence":
			box(root,Vector3(1.8,0.9,0.9),Vector3(0,0.5,0),metal)
			for i in range(5):
				box(root,Vector3(0.22,0.14,0.45),Vector3((i-2)*0.3,1,-0.05),material(Color("a2c5e1"),true))
		"recovery":
			for x in [-0.7,0.7]:box(root,Vector3(0.16,0.4,1.3),Vector3(x,0.2,0),metal)
			for z in [-0.55,-0.25,0.05,0.35,0.6]:box(root,Vector3(1.5,0.06,0.07),Vector3(0,0.45,z),gold)
			box(root,Vector3(0.24,0.08,0.24),Vector3(0,0.1,0),material(Color("c9774a"),true))
		"circuit":
			box(root,Vector3(1.9,1.5,0.6),Vector3(0,0.8,0),metal)
			for i in range(5):
				var lamp=box(root,Vector3(0.24,0.24,0.08),Vector3((i-2)*0.32,1.25,-0.36),gold)
				lamp.name="CircuitLamp"+str(i)
			for i in range(4):box(root,Vector3(0.1,0.3,0.18),Vector3((i-1.5)*0.38,0.7,-0.45),gold)
		"projector":
			box(root,Vector3(1.3,0.85,0.8),Vector3(0,0.65,0),dark)
			var optic=MeshInstance3D.new()
			var lens_shape=CylinderMesh.new()
			lens_shape.top_radius=0.36
			lens_shape.bottom_radius=0.36
			lens_shape.height=0.18
			optic.mesh=lens_shape
			optic.rotation.x=PI/2
			optic.position=Vector3(0,0.9,-0.48)
			optic.material_override=material(Color("9bdce9"),true)
			root.add_child(optic)
			for i in range(3):
				box(root,Vector3(0.09,0.025,0.9),Vector3((i-1)*0.25,0.035,-1.02),material([Color("c696e5"),Color("63d6cf"),Color("edc675")][i],true))
		"bench":
			box(root,Vector3(1.7,0.16,1.25),Vector3(0,0.95,0),metal)
			for x in [-0.65,0.65]: box(root,Vector3(0.16,0.9,0.9),Vector3(x,0.45,0),dark)
			box(root,Vector3(0.45,0.3,0.45),Vector3(0,1.17,0),gold)
			box(root,Vector3(0.12,0.12,0.9),Vector3(0.45,1.1,0),dark)
		"generator":
			box(root,Vector3(1.7,1.2,0.9),Vector3(0,0.6,0.2),dark)
			var wheel=MeshInstance3D.new()
			var ring=TorusMesh.new()
			ring.inner_radius=0.43
			ring.outer_radius=0.7
			wheel.mesh=ring
			wheel.material_override=gold
			wheel.rotation.x=PI/2
			wheel.position=Vector3(0,1,-0.5)
			root.add_child(wheel)
			box(wheel,Vector3(0.12,0.14,1.1),Vector3.ZERO,gold)
			machine_parts.generator=wheel
		"gauge":
			box(root,Vector3(0.75,1.1,0.65),Vector3(0,0.55,0),dark)
			box(root,Vector3(1.1,0.85,0.15),Vector3(0,1.3,-0.3),material(Color(e.pipe_color),true))
			var number=Label3D.new()
			number.text=str(e.value)
			number.font_size=70
			number.pixel_size=0.012
			number.position=Vector3(0,1.35,-0.4)
			number.billboard=BaseMaterial3D.BILLBOARD_ENABLED
			root.add_child(number)
		"valves":
			box(root,Vector3(1.7,0.9,0.65),Vector3(0,0.5,0),metal)
			for x in [-0.55,0,0.55]:
				box(root,Vector3(0.12,1.4,0.12),Vector3(x,0.7,0),gold)
				box(root,Vector3(0.38,0.12,0.22),Vector3(x,1.35,0),gold)
		"hoist":
			for x in [-0.8,0.8]: box(root,Vector3(0.18,2.5,0.4),Vector3(x,1.2,0),metal)
			box(root,Vector3(1.8,0.22,0.4),Vector3(0,2.45,0),gold)
			box(root,Vector3(0.05,2.2,0.05),Vector3(0,1.3,0),dark)
			machine_parts.weight=box(root,Vector3(0.65,0.65,0.65),Vector3(0,0.35,0),metal)
		"cabinet":
			box(root,Vector3(1.1,1.55,0.7),Vector3(0,0.8,0),metal)
			machine_parts.power_light=box(root,Vector3(0.55,0.25,0.06),Vector3(0,1.27,-0.39),material(Color("cc7055"),true))
func build_machine_decor():
	var index=0
	for pipe in level_data.get("pipes",[]):
		var tint=material(Color(pipe.color),true)
		var shift=(index-1)*0.16
		for i in range(pipe.cells.size()-1):
			var a=Vector3(pipe.cells[i][0]*TILE,0.03,pipe.cells[i][1]*TILE)
			var b=Vector3(pipe.cells[i+1][0]*TILE,0.03,pipe.cells[i+1][1]*TILE)
			var mesh=box(world,Vector3(abs(b.x-a.x)+0.085,0.04,abs(b.z-a.z)+0.085),(a+b)/2+Vector3(shift,0,shift),tint)
			mesh.set_meta("fog_cell",key(pipe.cells[i][0],pipe.cells[i][1]))
			mesh.visible=false
			machine_parts["pipe_"+str(index)+"_"+str(i)]=mesh
		index+=1
	machine_parts.water=box(world,Vector3(2.4,0.08,4.8),Vector3(25*TILE,0.02,22*TILE),material(Color("4592aa")))
	var lift=Node3D.new()
	lift.position=Vector3(17*TILE,0,35*TILE)
	world.add_child(lift)
	var metal=material(Color("7a8e95"))
	box(lift,Vector3(TILE-0.1,0.18,TILE-0.1),Vector3(0,0,0),material(accent))
	for x in [-1.1,1.1]:box(lift,Vector3(0.12,3.2,0.12),Vector3(x,1.6,0.9),metal)
	box(lift,Vector3(2.4,0.15,0.3),Vector3(0,3.15,0.9),metal)
	machine_parts.lift=lift
func _process(delta):
	Subject16.update(self,delta)
	if is_instance_valid(soundscape):soundscape.update(self,delta)
	update_ambience()
	if level>=21:preload("res://FinaleDecor.gd").update(self,delta)
	if level>=5 and is_instance_valid(folamour):
		folamour.visible=playing and render_near(folamour) and seen.has(key(roundi(folamour.position.x/TILE),roundi(folamour.position.z/TILE)))
	for prop in decor: prop.visible=render_near(prop) and seen.has(prop.get_meta("fog_cell")) and prop.get_meta("archive_active",true)
	if not playing or modal_open or level!=2 or machine_parts.is_empty(): return
	if done.has("generator") and machine_parts.has("generator"): machine_parts.generator.rotate_y(delta*3)
	if machine_parts.has("weight"): machine_parts.weight.position.y=lerpf(machine_parts.weight.position.y,1.75 if done.has("hoist") else 0.35,minf(1,delta*2))
	if machine_parts.has("water"):
		machine_parts.water.visible=seen.has(key(25,22))
		machine_parts.water.position.y=lerpf(machine_parts.water.position.y,-0.5 if done.has("water_manifold") else 0.02,minf(1,delta*2))
	if machine_parts.has("power_light") and done.has("lift_power") and not machine_parts.power_light.has_meta("powered"):
		machine_parts.power_light.material_override=material(Color("72d0a6"),true)
		machine_parts.power_light.set_meta("powered",true)
	if machine_parts.has("lift"):
		machine_parts.lift.visible=seen.has(key(17,34))
		if won:
			machine_parts.lift.position.y=minf(3,machine_parts.lift.position.y+delta*0.8)
			player.position=Vector3(17*TILE,machine_parts.lift.position.y+0.15,35*TILE)
			update_camera(delta)

func loc(source):
	return localization.translate(str(source))

func refresh_language(node):
	if node.has_meta("source_text"): node.text=loc(node.get_meta("source_text"))
	for child in node.get_children(): refresh_language(child)

func show_language(from_pause=false):
	clear_modal("FRANÇAIS / ENGLISH","Choisir la langue")
	paragraph("Le changement est immédiat et ne modifie pas votre progression.")
	modal_box.add_child(button("Français"+("  ✓" if localization.language=="fr" else ""),func(): choose_language("fr",from_pause),localization.language=="fr"))
	modal_box.add_child(button("English"+("  ✓" if localization.language=="en" else ""),func(): choose_language("en",from_pause),localization.language=="en"))
	modal_box.add_child(button("Retour",func(): show_pause() if from_pause else show_title()))

func choose_language(value,from_pause=false):
	localization.choose(value,not test_mode)
	refresh_language(ui_layer)
	if level==10:preload("res://ArchiveDecor.gd").translate_rooms(self)
	DisplayServer.window_set_title(loc("LE LABYRINTHE")+" — Folamour")
	if playing:
		update_hud()
		toast_label.text=loc(toast_source) if toast_timer>0 else ""
	if from_pause: show_pause()
	else: show_title()

func reference_name(id):
	for e in events:
		if e.id==id: return "["+e.ref+"] "+e.title
	if id=="socket_tool": return "[103] "+item_name(id)
	if id=="power_relay": return "[210] "+item_name(id)
	return item_name(id)
func journal_entry(id):
	var source=journal[id]
	var target=id.trim_prefix("installed_").trim_prefix("object_").trim_prefix("aide_")
	for e in events:
		if e.id==target: return "["+e.ref+"] "+source
	if target in ["socket_tool","power_relay"]: return ("[103] " if target=="socket_tool" else "[210] ")+source
	return source
func stop_navigation():
	move_path.clear()
	click_event={}
	stuck_time=0
	if is_instance_valid(destination_marker): destination_marker.hide()
func click_at(screen):
	var origin=camera.project_ray_origin(screen)
	var direction=camera.project_ray_normal(screen)
	var query=PhysicsRayQueryParameters3D.create(origin,origin+direction*200,3)
	query.collide_with_areas=true
	query.exclude=[player.get_rid()]
	var hit=get_world_3d().direct_space_state.intersect_ray(query)
	if not hit.is_empty() and hit.collider.has_meta("event_id"):
		for e in events:
			if e.id==hit.collider.get_meta("event_id") and seen.has(key(e.cell[0],e.cell[1])):
				request_event(e)
				return
	var ground=Plane(Vector3.UP,0).intersects_ray(origin,direction)
	if ground==null: return
	request_cell(Vector2i(roundi(ground.x/TILE),roundi(ground.z/TILE)))
func request_cell(goal):
	var start=Vector2i(roundi(player.position.x/TILE),roundi(player.position.z/TILE))
	var path=Navigator.route(self,start,goal)
	if path.is_empty():
		stop_navigation()
		toast("Choisissez un passage découvert et accessible.")
		return false
	stop_navigation()
	move_path=path
	destination_marker.position=Vector3(goal.x*TILE,0.04,goal.y*TILE)
	destination_marker.show()
	return true
func request_event(e):
	if e.kind=="pickup" and done.has(e.id): return
	if e.kind=="collectible" and Subject16.has(self,e):return
	stop_navigation()
	var start=Vector2i(roundi(player.position.x/TILE),roundi(player.position.z/TILE))
	var c=Vector2i(e.cell[0],e.cell[1])
	var candidates=[c,c+Vector2i.UP,c+Vector2i.RIGHT,c+Vector2i.DOWN,c+Vector2i.LEFT]
	var best=[]
	for goal in candidates:
		# Wall-mounted controls and offset actors are not at their grid center.
		# Choose a destination inside the same range used by finish_navigation.
		var position=Vector3(goal.x*TILE,0.1,goal.y*TILE)
		if position.distance_to(event_nodes[e.id].position)>3.0:continue
		var path=Navigator.route(self,start,goal)
		if not path.is_empty() and (best.is_empty() or path.size()<best.size()): best=path
	if best.is_empty():
		toast("Approchez-vous par un passage découvert.")
		return
	stop_navigation()
	move_path=best
	click_event=e
	destination_marker.position=Vector3(best[-1].x*TILE,0.04,best[-1].y*TILE)
	destination_marker.show()
func finish_navigation():
	var target=click_event.duplicate()
	stop_navigation()
	if target.is_empty(): return
	# Same physical line of sight as keyboard interactions; never reach through a wall.
	var pos=event_nodes[target.id].position
	if player.position.distance_to(pos)>3.0: return
	var query=PhysicsRayQueryParameters3D.create(player.position+Vector3(0,0.8,0),pos+Vector3(0,0.8,0))
	query.exclude=[player.get_rid()]
	var hit=get_world_3d().direct_space_state.intersect_ray(query)
	if hit.is_empty() or hit.collider==door_bodies.get(target.id): interact(target)

func add_event_signals(root,e):
	var area=Area3D.new()
	area.name="PickArea"
	area.collision_layer=2
	area.collision_mask=0
	area.set_meta("event_id",e.id)
	var shape=CollisionShape3D.new()
	var size_v=BoxShape3D.new()
	size_v.size=Vector3(1.5,2.0,1.5)
	shape.shape=size_v
	shape.position.y=1
	area.add_child(shape)
	root.add_child(area)
	if door_bodies.has(e.id): door_bodies[e.id].set_meta("event_id",e.id)
	if e.kind=="pickup":
		box(root,Vector3(0.7,0.035,0.7),Vector3(0,0.2,0),material(accent,true))
	elif e.kind=="clue":
		# A pale sheet visibly distinguishes a readable terminal from an item.
		box(root,Vector3(0.5,0.45,0.035),Vector3(0,1.16,-0.34),material(Color("b4e6e1")))
	elif not LevelEndings.is_doctor(e) and e.kind!="collectible":
		var lamp=box(root,Vector3(0.18,0.18,0.18),Vector3(0.75,1.8,0),material(Color("db735e"),true))
		signal_lights[e.id]=lamp
		for index in range(e.get("requires",[]).size()):
			# Empty dark sockets denote a place where a matching component is installed.
			var socket=box(root,Vector3(0.2,0.2,0.06),Vector3(-0.3+index*0.27,1.1,-0.49),material(Color("101f29")))
			socket.name="Socket"+str(index)
func build_readability_decor():
	destination_marker=Node3D.new()
	world.add_child(destination_marker)
	var ring=MeshInstance3D.new()
	var shape=TorusMesh.new()
	shape.inner_radius=0.35
	shape.outer_radius=0.46
	ring.mesh=shape
	ring.material_override=material(Color("8aefd1"),true)
	destination_marker.add_child(ring)
	destination_marker.hide()
	# Wall-mounted accents have no collision and never obstruct a corridor.
	for y in range(1,grid.size()-1):
		for x in range(1,grid.size()-1):
			if not floor_at(x,y) or (x*7+y*3)%19!=0: continue
			if floor_at(x,y-1): continue
			var prop=Node3D.new()
			prop.position=Vector3(x*TILE,0,y*TILE)
			prop.set_meta("fog_cell",key(x,y))
			world.add_child(prop)
			var tint=[Color("8ddbc3"),Color("9caedf"),Color("e6b979")][zone(y,x)]
			box(prop,Vector3(0.85,0.12,0.08),Vector3(0,1.6,-1.25),material(tint,true))
			box(prop,Vector3(1.05,0.28,0.08),Vector3(0,1.6,-1.3),material(Color("243942")))
			if level==2: box(prop,Vector3(0.11,1.35,0.11),Vector3(0.8,0.7,-1.2),material(Color("7b929c")))
			decor.append(prop)
			prop.hide()
func update_ambience():
	if not is_instance_valid(ambience): return
	if muted or not playing or modal_open or test_mode or (is_instance_valid(soundscape) and not soundscape.focused):
		soundscape.set_paused(ambience,true)
		return
	if level==25 or (level==24 and FinaleChapter.stage(self)==3):
		soundscape.set_paused(ambience,true)
		return
	var background_gain=soundscape.gain(self,"ambience") if is_instance_valid(soundscape) else 1.0
	if background_gain<=0:
		soundscape.set_paused(ambience,true)
		return
	var sector=zone(int(player.position.z/TILE),int(player.position.x/TILE))
	if level==24:sector=3+FinaleChapter.stage(self)
	if sector!=ambience_zone:
		ambience_zone=sector
		ambience.stream=load("res://assets/"+("horizon"+str(mini(2,sector-3)) if sector>=3 else "ambience"+str(sector))+".wav")
		ambience.play()
	elif not ambience.playing: ambience.play()
	soundscape.set_paused(ambience,false)
	ambience.volume_db=(-28 if not done.has("generator") else -23)+linear_to_db(maxf(background_gain,0.00001))

func build_code_keypad():
	var pad=GridContainer.new()
	pad.columns=3
	pad.add_theme_constant_override("h_separation",6)
	pad.add_theme_constant_override("v_separation",6)
	modal_box.add_child(pad)
	for digit in ["1","2","3","4","5","6","7","8","9","⌫","0","Effacer"]:
		var b=button(digit,func():
			if not is_instance_valid(code_entry): return
			if digit=="⌫": code_entry.text=code_entry.text.left(-1)
			elif digit=="Effacer": code_entry.text=""
			elif code_entry.text.length()<code_entry.max_length: code_entry.text+=digit
		)
		b.size_flags_horizontal=Control.SIZE_EXPAND_FILL
		pad.add_child(b)

func make_folamour(parent):
	var actor=Node3D.new()
	actor.name="DocteurFolamour"
	parent.add_child(actor)
	animated_doctors=animated_doctors.filter(func(a):return is_instance_valid(a))
	animated_doctors.append(actor)
	var coat=material(Color("e7eeee"))
	var skin=material(Color("e7bc99"))
	var dark=material(Color("243344"))
	box(actor,Vector3(0.72,1.05,0.48),Vector3(0,0.9,0),coat)
	box(actor,Vector3(0.5,0.5,0.46),Vector3(0,1.7,0),skin)
	box(actor,Vector3(0.6,0.22,0.5),Vector3(0,1.98,0.05),coat)
	for x in [-0.29,0.29]:
		var hair=box(actor,Vector3(0.28,0.38,0.5),Vector3(x,1.88,0.06),coat)
		hair.rotation.z=x*1.2
	for x in [-0.15,0.15]:
		box(actor,Vector3(0.25,0.2,0.05),Vector3(x,1.75,-0.26),dark)
		box(actor,Vector3(0.16,0.11,0.02),Vector3(x,1.75,-0.295),material(Color("b7e3e9"),true))
		box(actor,Vector3(0.25,0.4,0.26),Vector3(x,0.22,0),dark)
	box(actor,Vector3(0.12,0.08,0.08),Vector3(0,1.75,-0.27),dark)
	box(actor,Vector3(0.12,0.3,0.04),Vector3(0,1.15,-0.26),material(Color("bc5762")))
	for x in [-0.47,0.47]:
		var arm=Node3D.new();arm.name="ArmPivot"+str(x);arm.position=Vector3(x,1.3,0);arm.set_meta("side",signf(x));actor.add_child(arm)
		box(arm,Vector3(0.2,0.7,0.24),Vector3(0,-.3,0),coat)
		box(arm,Vector3(0.19,0.19,0.22),Vector3(0,-.7,0),skin)
	box(actor,Vector3(0.25,0.03,0.03),Vector3(0,1.54,-0.25),dark)
	return actor
func folamour_portrait():
	var container=SubViewportContainer.new()
	container.custom_minimum_size=Vector2(200,190)
	container.size_flags_horizontal=Control.SIZE_SHRINK_CENTER
	modal_box.add_child(container)
	var viewport=SubViewport.new()
	viewport.size=Vector2i(200,190)
	viewport.own_world_3d=true
	viewport.transparent_bg=true
	container.add_child(viewport)
	var actor=make_folamour(viewport)
	actor.rotation.y=-0.12
	var light=DirectionalLight3D.new()
	light.rotation_degrees=Vector3(-30,-25,0)
	light.light_energy=1.6
	viewport.add_child(light)
	var portrait_camera=Camera3D.new()
	viewport.add_child(portrait_camera)
	portrait_camera.position=Vector3(0,1.3,-4)
	portrait_camera.look_at(Vector3(0,1.15,0))
	portrait_camera.projection=Camera3D.PROJECTION_ORTHOGONAL
	portrait_camera.size=2.5
func show_folamour_intro():
	clear_modal("NIVEAU 5 / LE DÉFI DE FOLAMOUR","Enfin, en personne.")
	folamour_portrait()
	paragraph("Le docteur Folamour vous accueille en personne, puis rejoint la galerie nord du stabilisateur. Il y attendra votre démonstration.",17)
	paragraph("« Sujet 16 ! Encore debout ? Je commençais à soupçonner mes labyrinthes d’être trop accueillants. Rassurez-vous, je corrigerai cela. »",21)
	paragraph("« Voici ZÉRO. Personne n’a jamais réussi à stabiliser ce prototype. Pas un seul de mes brillants assistants. Je vous mets au défi d’être le premier. Le matériel est précieux ; vous, nous verrons. »",21)
	paragraph("Explorez les ailes ouest et est, assemblez leurs résultats dans le hall, puis accédez au stabilisateur nord. Aucun compte à rebours. Tous les essais peuvent être recommencés.",17)
	modal_box.add_child(button("Relever le défi",func(): done["folamour_met"]=true; add_journal("intro","LE DÉFI DE FOLAMOUR\nStabiliser ZÉRO : dosage à l’ouest, transfert à l’est, assemblage dans le hall, rotors au nord. Personne n’y est encore arrivé."); close_modal(),true))

func show_objective():
	clear_modal("CARNET DE BORD","Objectif actuel")
	paragraph_ready(Guidance.objective(self),20)
	paragraph("Les objectifs se mettent à jour avec votre progression. Les solutions restent dans les indices facultatifs de chaque mécanisme.",16)
	modal_box.add_child(button("Journal",show_journal))
	modal_box.add_child(button("Reprendre",close_modal,true))

func show_hint(e,typed=null,at_mechanism=true):
	if typed==null:typed=code_entry.text if is_instance_valid(code_entry) and current_event.get("id","")==e.id else ""
	clear_modal("AIDE FACULTATIVE",e.title)
	var steps=Guidance.hint_steps(self,e)
	var count=clampi(int(hints.get(e.id,0)),0,steps.size())
	paragraph("Les indices sont facultatifs et sans pénalité. La troisième étape révèle la solution. Les consulter ne modifie pas le mécanisme.",16)
	for i in range(count):
		paragraph(loc("Indice %d / 3") % (i+1),16)
		paragraph_ready(steps[i])
	if count<steps.size():
		modal_box.add_child(button("Révéler la solution" if count==2 else "Afficher une piste" if count==0 else "Afficher la méthode",func():
			hints[e.id]=count+1
			save_game()
			show_hint(e,typed,at_mechanism)))
	if at_mechanism:
		modal_box.add_child(button("Retour au mécanisme",func():
			show_puzzle(e)
			if is_instance_valid(code_entry) and e.has("answer") and not e.has("dials"):code_entry.text=typed
		,true))
	else:modal_box.add_child(button("Journal",show_journal,true))
	modal_box.add_child(button("Reprendre",close_modal))

func show_audio(from_pause=true):
	clear_modal("AMBIANCE DU LABORATOIRE","Réglages audio")
	paragraph("Une musique lounge différente par chapitre, de plus en plus rythmée, et une ouverture décalée au menu. Le fond musical s’atténue pendant la lecture.",16)
	for channel in ["master","music","effects","ambience"]:
		var titles={"master":"Volume général","music":"Musique","effects":"Effets sonores","ambience":"Bruit des machines"}
		var caption=paragraph(loc(titles[channel])+" : "+str(roundi(soundscape.levels[channel]*100))+" %",17)
		var slider=HSlider.new()
		slider.min_value=0
		slider.max_value=100
		slider.step=1
		slider.value=soundscape.levels[channel]*100
		slider.custom_minimum_size=Vector2(0,48)
		modal_box.add_child(slider)
		slider.value_changed.connect(func(value):
			soundscape.levels[channel]=value/100.0
			caption.text=loc(titles[channel])+" : "+str(int(value))+" %"
			soundscape.persist())
	modal_box.add_child(button("Son : "+("désactivé" if muted else "activé"),func():
		muted=not muted
		soundscape.preference_muted=muted
		soundscape.persist()
		if playing:save_game()
		show_audio(from_pause)))
	modal_box.add_child(button("Retour",func():
		if from_pause:show_pause()
		else:show_title()
	,true))

# Guidance already selected its language; do not translate embedded English twice.
func paragraph_ready(text,size_v=18):
	var l=paragraph("",size_v)
	l.remove_meta("source_text")
	l.text=text
	return l

func show_greenhouse_intro():
	clear_modal("CHAPITRE 2 / LE STAGE NON RÉMUNÉRÉ","Mission 1 — Les serres expérimentales")
	folamour_portrait()
	paragraph("« Bienvenue dans l’équipe. Pour votre première mission, un simple café. La cafetière dépend de l’irrigation, de la botanique et d’un mélangeur expérimental. Mais je vous fais confiance : je suis déjà en pause. » — Folamour",20)
	paragraph("Rétablissez l’eau à l’ouest, faites pousser la liane au centre, récoltez à l’est puis préparez le mélange au nord. Une tasse vous attend dans le vestiaire au sud. Les essais sont réversibles ; aucun compte à rebours.",17)
	modal_box.add_child(button("Prendre mon service",func():
		done.g_met=true
		add_journal("intro","STAGE / PREMIÈRE MISSION\nPréparer le café : irrigation, liane-pont, récoltes, mélange et tasse. Le rappel d’objectif suit votre progression.")
		close_modal(),true))

func show_greenhouse_win():
	clear_modal("CHAPITRE 2 / MISSION 1 TERMINÉE","Le café est servi.")
	folamour_portrait()
	paragraph("Folamour prend une gorgée, examine la tasse et hoche la tête.",17)
	paragraph("« Excellent. Vous avez restauré un écosystème pour une tasse de café. Voilà exactement le sens des priorités que nous recherchons. Demain, nous verrons si vous savez faire des photocopies. » — Folamour",20)
	var stat=level_stats["6"]
	paragraph(loc("Temps du niveau : %02d:%02d\nSecrets : %d / 3    •    Tentatives incorrectes : %d") % [int(elapsed)/60,int(elapsed)%60,stat.secrets,errors],20)
	paragraph(loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d") % [stat.puzzles,stat.shortcuts,stat.hints],17)
	paragraph("Votre bilan est sauvegardé. La deuxième mission du stage est disponible.",17)
	modal_box.add_child(button("Passer aux photocopies",func():start_game(false,7,true),true))
	modal_box.add_child(button("Choisir un chapitre",func(): playing=false; hud.hide(); show_chapters(),true))
	modal_box.add_child(button("Sauvegarder et revenir au menu",show_title))

func show_office_intro():
	clear_modal("CHAPITRE 2 / LE STAGE NON RÉMUNÉRÉ","Mission 2 — Le service des photocopies")
	folamour_portrait()
	paragraph("« Votre café était presque tiède. Passons à une tâche à votre portée : une photocopie. Les archives sont verrouillées et le photocopieur inverse les images. Des détails, pour quelqu’un d’aussi peu rémunéré. » — Folamour",20)
	paragraph("Alignez les calques à l’ouest, classez les dossiers au nord-est, puis préparez la copie au sud. Rapportez-la à l’accueil. Les essais sont réversibles et sauvegardés.",17)
	modal_box.add_child(button("Accepter la mission",func():
		done.p_met=true
		add_journal("intro","STAGE / DEUXIÈME MISSION\nPréparer une photocopie : calques, classement, papier, toner et transformations. Livraison à l’accueil 101.")
		close_modal(),true))

func show_office_win():
	clear_modal("CHAPITRE 2 / MISSION 2 TERMINÉE","Une copie presque parfaite.")
	folamour_portrait()
	paragraph("Folamour examine la feuille, la retourne et vous adresse un sourire satisfait.",17)
	paragraph("« Félicitations. Une copie parfaitement conforme ! J’avais oublié de préciser : je la voulais recto verso. Mais gardez votre enthousiasme, c’est la seule chose que nous ne fournissons pas. » — Folamour",20)
	var stat=level_stats["7"]
	paragraph(loc("Temps du niveau : %02d:%02d\nSecrets : %d / 3    •    Tentatives incorrectes : %d") % [int(elapsed)/60,int(elapsed)%60,stat.secrets,errors],20)
	paragraph(loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d") % [stat.puzzles,stat.shortcuts,stat.hints],17)
	paragraph("Votre copie est acceptée. La troisième mission du stage est disponible.",17)
	modal_box.add_child(button("Passer au courrier interne",func():start_game(false,8,true),true))
	modal_box.add_child(button("Choisir un chapitre",func():playing=false;hud.hide();show_chapters(),true))
	modal_box.add_child(button("Sauvegarder et revenir au menu",show_title))

func show_mail_intro():
	clear_modal("CHAPITRE 2 / LE STAGE NON RÉMUNÉRÉ","Mission 3 — Le courrier interne")
	folamour_portrait()
	paragraph("« Une simple livraison. Même vous devriez pouvoir y arriver. Évitez seulement d’ouvrir le colis : son contenu n’a pas encore accepté son affectation. » — Folamour",20)
	paragraph("Identifiez le colis plus lourd à l’ouest, réglez le réseau au centre et reconstituez l’adresse au sud. Livraison à la réception est. Aucun compte à rebours, aucun essai destructif.",17)
	modal_box.add_child(button("Accepter la mission",func():
		done.m_met=true
		add_journal("intro","STAGE / TROISIÈME MISSION\nLivrer un colis : balance à l’ouest, réseau au centre, adresse au sud, livraison en 101.")
		close_modal(),true))
func show_mail_win():
	clear_modal("CHAPITRE 2 / MISSION 3 TERMINÉE","Livraison accomplie.")
	folamour_portrait()
	paragraph("Folamour ouvre le colis : une sonnette de bureau. Il la fait tinter, puis vous regarde.",17)
	paragraph("« Excellent ! Maintenant, vous pourrez annoncer votre arrivée avant de me déranger. » — Folamour",20)
	var stat=level_stats["8"]
	paragraph(loc("Temps du niveau : %02d:%02d\nSecrets : %d / 3    •    Tentatives incorrectes : %d") % [int(elapsed)/60,int(elapsed)%60,stat.secrets,errors],20)
	paragraph(loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d") % [stat.puzzles,stat.shortcuts,stat.hints],17)
	paragraph("Le colis est livré. La quatrième mission du stage est disponible.",17)
	modal_box.add_child(button("Passer à la salle de réunion",func():start_game(false,9,true),true))
	modal_box.add_child(button("Choisir un chapitre",func():playing=false;hud.hide();show_chapters(),true))
	modal_box.add_child(button("Sauvegarder et revenir au menu",show_title))

func show_meeting_intro():
	clear_modal("CHAPITRE 2 / LE STAGE NON RÉMUNÉRÉ","Mission 4 — La salle de réunion")
	folamour_portrait()
	paragraph("« Aujourd’hui, vous allez rencontrer mes collègues. Des esprits brillants, exigeants… et particulièrement difficiles à faire venir depuis l’incident. Préparez la salle. Je m’occupe des excuses. » — Folamour",20)
	paragraph("Placez les invités à l’ouest, préparez le planning à l’est, puis branchez la conférence dans la salle centrale. Les bureaux au nord et au sud contiennent du matériel et des indices.",17)
	modal_box.add_child(button("Accepter la mission",func():
		done.r_met=true
		add_journal("intro","STAGE / QUATRIÈME MISSION\nPréparer le comité : placement 203, planning 303, conférence 403 puis ouverture en 105.")
		close_modal(),true))
func show_meeting_win():
	for e in events:
		if e.id=="r_conference":PuzzleControls.sync(self,e)
	clear_modal("CHAPITRE 2 / MISSION 4 TERMINÉE","Un comité très indépendant.")
	folamour_portrait()
	paragraph("Les six écrans s’allument : chacun affiche Folamour, avec une voix et un titre différents. Aster réclame une pause ; Boréal ouvre la séance ; Cobalt conteste sa présidence.",17)
	paragraph("« Des versions artificielles de moi-même. Pour obtenir des avis indépendants. Elles ne sont d’accord sur rien… sauf sur votre rémunération. Aucun changement, à l’unanimité. » — Folamour",20)
	paragraph("« Une réunion productive : nous avons confirmé une décision prise avant votre arrivée. Vous commencez à comprendre le fonctionnement du laboratoire. » — Folamour",20)
	paragraph("Sur les écrans, un nouveau dossier apparaît : PROJET MIROIR — UNIFICATION. Folamour coupe la transmission avant que vous puissiez en lire davantage.",17)
	var stat=level_stats["9"]
	paragraph(loc("Temps du niveau : %02d:%02d\nSecrets : %d / 3    •    Tentatives incorrectes : %d") % [int(elapsed)/60,int(elapsed)%60,stat.secrets,errors],20)
	paragraph(loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d") % [stat.puzzles,stat.shortcuts,stat.hints],17)
	paragraph("La réunion est terminée. Folamour vous attend aux archives pour votre cinquième mission.",17)
	modal_box.add_child(button("Passer au service des archives",func():start_game(false,10,true),true))
	modal_box.add_child(button("Choisir un chapitre",func():playing=false;hud.hide();show_chapters(),true))
	modal_box.add_child(button("Sauvegarder et revenir au menu",show_title))

func show_archive_intro():
	clear_modal("CHAPITRE 2 / LE STAGE NON RÉMUNÉRÉ","Mission 5 — Le service des archives")
	folamour_portrait()
	paragraph("« Rapportez-moi le dossier MIROIR. L’original, évidemment. Les copies ont une fâcheuse tendance à se prendre pour l’original. » — Folamour",20)
	paragraph("Explorez les rayonnages au nord, recoupez les preuves à l’ouest et comparez les salles jumelles à l’est. Trois validations et le sceau donnent accès au dossier central.",17)
	modal_box.add_child(button("Accepter la mission",func():
		done.a_met=true
		add_journal("intro","STAGE / CINQUIÈME MISSION\nRayonnages 203, sceau 204, rapport 303, salle jumelle 403, puis dossier MIROIR 105.")
		close_modal(),true))
func show_archive_win():
	preload("res://ArchiveDecor.gd").finish(self)
	clear_modal("CHAPITRE 2 / MISSION 5 TERMINÉE","L’original et ses mauvaises habitudes.")
	paragraph("MIROIR reproduit les lieux et les comportements des occupants du laboratoire. Le comité était un premier essai : six versions artificielles de Folamour. L’UNIFICATION doit réunir leurs observations dans une copie cohérente.",18)
	paragraph("Votre fiche : « Sujet : en cours d’évaluation. Capacité à résoudre les problèmes : satisfaisante. Capacité à demander pourquoi : préoccupante. »",19)
	folamour_portrait()
	paragraph("« Ah. Vous avez ouvert le dossier. J’avais demandé de le rapporter, pas de développer un esprit critique. » — Folamour",20)
	paragraph("Au fond du hall, un voyant s’allume : SECTEUR DES PROTOTYPES. La porte s’entrouvre sur le département de la prévoyance. Folamour a cinq nouvelles missions pour vous.",17)
	modal_box.add_child(button("Entrer au département de la prévoyance",func():start_game(false,11,true),true))
	var stat=level_stats["10"]
	paragraph(loc("Temps du niveau : %02d:%02d\nSecrets : %d / 3    •    Tentatives incorrectes : %d") % [int(elapsed)/60,int(elapsed)%60,stat.secrets,errors],20)
	paragraph(loc("Énigmes résolues : %d • Raccourcis découverts : %d • Indices révélés : %d") % [stat.puzzles,stat.shortcuts,stat.hints],17)
	modal_box.add_child(button("Choisir un chapitre",func():playing=false;hud.hide();show_chapters(),true))
	modal_box.add_child(button("Sauvegarder et revenir au menu",show_title))
