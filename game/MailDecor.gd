extends RefCounted
static func model(g,root,e,gold,dark):
	var tan=g.material(Color("c8a67c"))
	if e.model=="parcels":
		g.box(root,Vector3(.16,.8,.16),Vector3(0,.5,0),dark)
		var beam=Node3D.new();beam.name="MailBeam";beam.position.y=.9;root.add_child(beam)
		g.box(beam,Vector3(1.7,.08,.1),Vector3.ZERO,gold)
		for side in [-1,1]:g.box(beam,Vector3(.65,.08,.8),Vector3(side*.6,-.15,0),dark)
		for i in range(6):
			var parcel=g.box(root,Vector3(.2,.2,.2),Vector3((i-2.5)*.26,.22,.72),tan);parcel.name="Parcel"+str(i)
	elif e.model=="mailnet":
		g.box(root,Vector3(1.7,1.4,.45),Vector3(0,.75,0),dark)
		for i in range(3):
			g.box(root,Vector3(.15,1,.15),Vector3((i-1)*.5,.8,-.3),gold)
			g.box(root,Vector3(.45,.15,.15),Vector3((i-1)*.5,1.15-i*.25,-.3),gold)
	else:
		g.box(root,Vector3(1.5,.8,.9),Vector3(0,.4,0),dark)
		g.box(root,Vector3(.7,.55,.08),Vector3(0,1,-.2),g.material(Color("83b6ad")))
		g.box(root,Vector3(.55,.4,.45),Vector3(.35,.95,.3),tan)
