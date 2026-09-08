extends Control
var event={}
var values=[]
var game
func label(at,text,color=Color("e5eced"),font_size=16):
	draw_string(get_theme_default_font(),at,text,HORIZONTAL_ALIGNMENT_LEFT,-1,font_size,color)
func _draw():
	if event.is_empty():return
	draw_style_box(panel(),Rect2(Vector2.ZERO,size))
	var ink=Color("e7bb77");var good=Color("8cdbc6");var dim=Color("6e8398")
	if event.mode in ["badges","routine","gaze"]:
		for i in range(3):
			var gate=event.world_gates[i];var open=values[int(gate.channel)] in gate.allowed.map(func(x):return int(x)) or game.done.has(event.id)
			var p=Vector2(size.x*(i+1)/4,85)
			draw_line(Vector2(size.x/2,205),p,good if open else dim,3)
			draw_rect(Rect2(p-Vector2(30,28),Vector2(60,56)),good if open else dim,false,3)
			label(p+Vector2(-6,5),gate.label,ink,20)
			label(p+Vector2(-25,-39),"%d,%d"%[gate.cell[0],gate.cell[1]],dim,14)
			label(p+Vector2(-4,65),"✓" if game.done.has(event.observations[i]) else "?",good,19)
			if event.mode=="gaze":
				var d=[Vector2.UP,Vector2.RIGHT,Vector2.DOWN,Vector2.LEFT][values[i]]
				draw_line(p,p+d*23,ink,4);draw_circle(p+d*23,4,ink)
		label(Vector2(size.x/2-16,228),"203",ink,17)
	elif event.mode in ["tubes","trust","conveyor"]:
		var count=event.names.size();var positions=[]
		for i in range(count):
			var x=size.x*(.2 if i%2==0 else .8);var y=38+floor(i/2.0)*57
			positions.append(Vector2(x,y))
		for i in range(event.edges.size()):
			var end=int(event.edges[i][values[i]]);var a=positions[i];var b=positions[end]
			draw_line(a,b,good,2)
			var d=(b-a).normalized();var tip=b-d*20
			draw_colored_polygon(PackedVector2Array([tip,tip-d*9+Vector2(-d.y,d.x)*5,tip-d*9-Vector2(-d.y,d.x)*5]),good)
		if event.has("fixed"):
			for key in event.fixed:
				var a=positions[int(key)];var b=positions[int(event.fixed[key])];draw_line(a,b,dim,2)
		for i in range(count):
			draw_circle(positions[i],18,Color("233c49"));draw_arc(positions[i],18,0,TAU,24,ink,2)
			label(positions[i]+Vector2(-6,5),event.names[i],ink,18)
	elif event.mode=="energy":
		for i in range(3):
			var x=size.x*(i+1)/4;draw_rect(Rect2(x-18,40,36,135),dim,false,2)
			draw_rect(Rect2(x-15,172-values[i]*21,30,values[i]*21),good)
			label(Vector2(x-6,202),["A","B","C"][i],ink,18)
	elif event.mode=="seal":
		draw_line(Vector2(size.x*.2,115),Vector2(size.x*.8,115),dim,9)
		label(Vector2(12,30),game.loc("BUREAUX"),ink,15);label(Vector2(size.x-100,30),game.loc("CONSEIL"),ink,15)
		for i in range(4):
			var x=size.x*(.8 if values[0]&(1<<i) else .2);var y=57+i*43
			draw_circle(Vector2(x,y),16,good if values[3]&(1<<i) else dim)
			label(Vector2(x-6,y+5),["A","B","C","D"][i],Color("12222c"),17)
		draw_circle(Vector2(size.x*(.8 if values[1] else .2)+32,220),8,ink)
func panel():
	var p=StyleBoxFlat.new();p.bg_color=Color("11222f");p.corner_radius_top_left=10;p.corner_radius_top_right=10;p.corner_radius_bottom_left=10;p.corner_radius_bottom_right=10;return p
