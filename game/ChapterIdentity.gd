extends RefCounted
static func model(g,root,e):
	var theme=g.Subject16.theme(g.level);var c=g.Subject16.chapter(g.level)
	var color=g.material(Color(theme.color),true);var dark=g.material(Color("273843"));var paper=g.material(Color("f4e5c8"))
	var visual=Node3D.new();visual.name="CollectibleModel";root.add_child(visual)
	g.box(visual,Vector3(.65,.08,.65),Vector3(0,.15,0),dark)
	match c:
		1:
			g.box(visual,Vector3(.38,.7,.38),Vector3(0,.85,0),color)
			for y in [.48,1.23]:g.box(visual,Vector3(.48,.12,.48),Vector3(0,y,0),paper)
			g.box(visual,Vector3(.08,.32,.04),Vector3(-.08,.9,-.21),paper)
		2:
			g.box(visual,Vector3(.78,.17,.55),Vector3(0,.55,0),color)
			g.box(visual,Vector3(.25,.5,.25),Vector3(0,.85,0),dark)
			g.box(visual,Vector3(.5,.18,.4),Vector3(0,1.15,0),color)
			g.box(visual,Vector3(.45,.025,.6),Vector3(.15,.24,.12),paper)
		3:
			for i in range(8):
				var tooth=g.box(visual,Vector3(.18,.25,.28),Vector3(sin(i*TAU/8)*.36,.85+cos(i*TAU/8)*.36,0),color);tooth.rotation.z=-i*TAU/8
			g.box(visual,Vector3(.37,.37,.18),Vector3(0,.85,0),dark)
			g.box(visual,Vector3(.15,.15,.23),Vector3(0,.85,0),paper)
		4:
			var prism=g.box(visual,Vector3(.55,.8,.55),Vector3(0,.95,0),color);prism.rotation_degrees=Vector3(15,45,25)
			g.box(visual,Vector3(.07,.48,.06),Vector3(-.21,.97,-.27),paper)
		5:
			g.box(visual,Vector3(.46,.7,.46),Vector3(0,.85,0),paper)
			var top=g.box(visual,Vector3(.36,.36,.36),Vector3(0,1.28,0),color);top.rotation.z=PI/4
			for x in [-.32,.32]:g.box(visual,Vector3(.16,.35,.3),Vector3(x,.55,0),color)
			g.box(visual,Vector3(.24,.2,.05),Vector3(0,.98,-.25),dark)
	# A different engraved notch count per mission, within the chapter silhouette.
	for i in range((g.level-1)%5+1):g.box(visual,Vector3(.06,.05,.035),Vector3((i-2)*.10,.30,-.32),color)
static func setup(g):
	var theme=g.Subject16.theme(g.level);var c=g.Subject16.chapter(g.level)
	var tint=g.material(Color(theme.color));var dark=g.material(Color("283e49"));var paper=g.material(Color("ddd2b9"))
	var placed=0
	for y in range(2,g.grid.size()-2,2):
		for x in range(2,g.grid.size()-2,2):
			if placed>=28:break
			if g.floor_at(x,y) or (x*3+y*7+g.level)%5!=0:continue
			var access=Vector2i(-1,-1)
			for d in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
				if g.floor_at(x+d.x,y+d.y):access=Vector2i(x,y)+d;break
			if access.x<0:continue
			var nearby=false
			for e in g.events:
				if abs(e.cell[0]-access.x)+abs(e.cell[1]-access.y)<3:nearby=true;break
			if nearby:continue
			var prop=Node3D.new();prop.name="ChapterIdentity%d"%placed;prop.position=Vector3(x*g.TILE,2.3,y*g.TILE);prop.set_meta("fog_cell",g.key(access.x,access.y));g.world.add_child(prop);g.decor.append(prop)
			g.box(prop,Vector3(1.5,.14,1.5),Vector3.ZERO,dark)
			match c:
				1:
					for i in range(3):
						g.box(prop,Vector3(.28,.5+i*.15,.28),Vector3((i-1)*.45,.4,0),tint)
						g.box(prop,Vector3(.38,.12,.38),Vector3((i-1)*.45,.7+i*.075,0),paper)
				2:
					g.box(prop,Vector3(1.35,.9,.65),Vector3(0,.5,0),dark)
					for i in range(4):g.box(prop,Vector3(.20,.64,.48),Vector3((i-1.5)*.28,.57,-.1),paper if i%2==0 else tint)
				3:
					for i in range(3):
						var panel=g.box(prop,Vector3(.75,.09,.75),Vector3(0,.2+i*.30,0),tint);panel.rotation.y=i*.35
					g.box(prop,Vector3(.13,1.0,.13),Vector3(0,.5,0),paper)
				4:
					for side in [-1,1]:
						var mirror=g.box(prop,Vector3(.12,1.2,.8),Vector3(side*.46,.65,0),tint);mirror.rotation.z=side*.10
					g.box(prop,Vector3(.45,.08,.45),Vector3(0,.3,0),paper)
				5:
					for side in [-1,1]:g.box(prop,Vector3(.24,.4,1.3),Vector3(side*.42,.3,0),tint)
					for z in [-.4,0,.4]:g.box(prop,Vector3(1.2,.12,.16),Vector3(0,.53,z),paper)
			placed+=1
	# Thin floor inlays differentiate chapters without adding physical obstacles.
	for y in range(3,g.grid.size()-2,5):
		for x in range(3,g.grid.size()-2,5):
			if not g.floor_at(x,y):continue
			var prop=Node3D.new();prop.position=Vector3(x*g.TILE,0,y*g.TILE);prop.set_meta("fog_cell",g.key(x,y));g.world.add_child(prop);g.decor.append(prop)
			for side in [-1,1]:g.box(prop,Vector3(.55,.025,.08),Vector3(side*.6,.01,-.8),tint)
