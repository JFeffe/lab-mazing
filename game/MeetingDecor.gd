extends RefCounted
static func model(g,root,e,gold,dark):
	if e.model!="conference":
		g.box(root,Vector3(1.6,.8,1),Vector3(0,.4,0),dark)
		for i in range(6 if e.model=="seating" else 4):g.box(root,Vector3(.18,.06,.3),Vector3((i-2.5)*.22,.83,0),gold)
		return
	g.box(root,Vector3(2.4,.18,3.5),Vector3(0,.85,0),dark)
	for i in range(6):
		var side=-1 if i<3 else 1
		var z=(i%3-1)*1.3
		g.box(root,Vector3(.8,.65,.13),Vector3(side*1.65,1.3,z),dark)
		var face=Node3D.new();face.name="ScreenFace"+str(i);face.position=Vector3(side*1.65,1.3,z-.1);root.add_child(face)
		g.box(face,Vector3(.62,.48,.025),Vector3.ZERO,g.material(Color("76a4ac")))
		g.box(face,Vector3(.24,.25,.03),Vector3(0,-.02,-.03),g.material(Color("e6c4a5")))
		g.box(face,Vector3(.34,.1,.04),Vector3(0,.12,-.03),g.material(Color("eee9d8")))
		for x in [-.09,.09]:g.box(face,Vector3(.12,.07,.03),Vector3(x,.025,-.06),dark)
		face.visible=false
	for i in range(2):
		var light=g.box(root,Vector3(.25,.06,.25),Vector3((i-.5)*.4,.98,1.3),gold);light.name="Preparation"+str(i)
	var indicator=g.box(root,Vector3(.5,.06,.25),Vector3(0,.98,-1.3),gold);indicator.name="ConferenceSignal"
