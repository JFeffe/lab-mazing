extends RefCounted
static func model(g,root,e,gold,dark):
	var cream=g.material(Color("d6cfb8"))
	if e.model=="filing":
		g.box(root,Vector3(1.4,1.65,.7),Vector3(0,.83,0),dark)
		for i in range(4):
			g.box(root,Vector3(1.25,.06,.8),Vector3(0,.27+i*.28,0),cream)
			var file=g.box(root,Vector3(.23,.18,.12),Vector3((i-1.5)*.28,.4,-.44),gold)
			file.name="File"+str(i)
	else:
		g.box(root,Vector3(1.7,.85,1.15),Vector3(0,.45,0),cream)
		g.box(root,Vector3(1.65,.1,1.1),Vector3(0,.92,0),dark)
		for i in range(9):
			var pixel=g.box(root,Vector3(.24,.025,.24),Vector3((i%3-1)*.27,.99,(i/3-1)*.27),cream)
			pixel.name="Pixel"+str(i)
		if e.model=="copier":
			g.box(root,Vector3(1.5,.15,.15),Vector3(0,.5,-.6),dark)
			g.box(root,Vector3(.8,.025,.6),Vector3(0,.4,-.85),cream)
