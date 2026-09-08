extends Control
var game
var event={}
var values=[]
func label_at(p,text,color=Color("e6efe9"),font_size=17):
	draw_string(get_theme_default_font(),p,text,HORIZONTAL_ALIGNMENT_LEFT,-1,font_size,color)
func _draw():
	if event.is_empty():return
	draw_style_box(game.style(Color("142a35")),Rect2(Vector2.ZERO,size))
	if event.mode=="courier":
		var count=event.boards.size();var width=(size.x-20)/count;var tile=minf((width-16)/5,36)
		var results=game.PuzzleControls.Finale.result(event,values)
		for b in range(count):
			var origin=Vector2(10+b*width+(width-5*tile)/2,37)
			label_at(Vector2(12+b*width,23),game.loc("CAPSULE %s")%'AB'[b],Color("e5bc7f"),15)
			for y in range(5):
				for x in range(5):
					var c=event.boards[b][y][x];var p=origin+Vector2(x,y)*tile
					draw_rect(Rect2(p,Vector2.ONE*(tile-2)),Color("415464") if c=="#" else Color("bac9c3"))
					if c not in ['#','.']:label_at(p+Vector2(tile*.27,tile*.73),c,Color("6e3030") if c=="X" else Color("12363d"),int(tile*.6))
			if values.back()==1:
				var points=PackedVector2Array()
				for p in results.paths[b].trace:points.append(origin+Vector2(p)*tile+Vector2.ONE*(tile-2)*.5)
				if points.size()>1:draw_polyline(points,Color("386ae5"),2.5,true)
	elif event.mode=="gantry":
		for i in range(3):
			var x=20+i*(size.x-25)/3;var width=(size.x-45)/3
			label_at(Vector2(x,28),'ABC'[i]+" · "+str(values[i]))
			draw_rect(Rect2(x,43,width,60),Color("506674"))
			draw_line(Vector2(x+4,73),Vector2(x+width-4,73+(values[i]-1)*18 if values[i]!=0 else 73),Color("a0d9b2") if values[i]==0 else Color("e4b171"),6)
			label_at(Vector2(x,133),game.loc("OUVERT" if values[i]==0 else "FERMÉ"),Color("e6efe9"),14)
	elif event.mode=="damping":
		for i in range(6):
			var x=18+(i%3)*(size.x-20)/3;var y=30+int(i/3)*70;var active=bool(values[0]&(1<<i))
			draw_circle(Vector2(x+11,y),10,Color("e4956b") if active else Color("9dd0b0"))
			label_at(Vector2(x+29,y+6),'ABCDEF'[i],Color("e6efe9"),18)
			label_at(Vector2(x,y+32),game.loc("ACTIF" if active else "ÉTEINT"),Color("e6efe9"),13)
