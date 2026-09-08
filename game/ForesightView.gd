extends Control
var event={}
var values=[]
var second=false
func _draw():
	if event.is_empty():return
	var mode=event.mode
	draw_rect(Rect2(Vector2.ZERO,size),Color("101f2b"))
	var font=get_theme_default_font()
	if mode in ["courier","duet","cameras"]:
		var board=event.board_b if second else event.board
		var cell=minf((size.x-24)/5,(size.y-28)/5);var offset=Vector2((size.x-cell*5)/2,20)
		var covered=preload("res://ForesightControls.gd").coverage(event,values) if mode=="cameras" else {}
		for y in range(5):
			for x in range(5):
				var p=Vector2i(x,y);var mark=board[y][x];var col=Color("273d4a") if mark=="#" else Color("659989") if covered.has(p) else Color("496576")
				draw_rect(Rect2(offset+Vector2(p)*cell,Vector2.ONE*(cell-2)),col)
				if mark not in [".","#"]:draw_string(font,offset+(Vector2(p)+Vector2(.35,.68))*cell,mark,HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color.WHITE)
		if mode!="cameras" and values.back()==1:
			var r=preload("res://ForesightControls.gd").result(event,values);var trace=r.b.path if second else r.a.path
			for i in range(1,trace.size()):draw_line(offset+(Vector2(trace[i-1])+Vector2.ONE*.5)*cell,offset+(Vector2(trace[i])+Vector2.ONE*.5)*cell,Color("f0c77f"),3)
			draw_circle(offset+(Vector2(trace.back())+Vector2.ONE*.5)*cell,7,Color.WHITE)
		draw_string(font,Vector2(10,16),"B" if second else "A",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
	elif mode in ["tanks","budget"]:
		var count=3 if mode=="tanks" else 4;var w=(size.x-30)/count
		for i in range(count):
			var cap=int(event.capacities[i]) if mode=="tanks" else int(event.budget)
			var h=150*float(values[i])/cap
			draw_rect(Rect2(20+i*w,30,w-18,160),Color("294454"))
			draw_rect(Rect2(20+i*w,190-h,w-18,h),Color("82c8bc"))
			draw_string(font,Vector2(27+i*w,218),str(values[i]),HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color.WHITE)
	elif mode=="echoes":
		var r=preload("res://ForesightControls.gd").result(event,values)
		for i in range(6):
			var c=Vector2(size.x*(i%3+1)/4,65+int(i/3)*110)
			draw_circle(c,26,Color("e9be72") if r.lamps&(1<<i) else Color("3b515f"))
			draw_string(font,c+Vector2(-5,6),str(i+1),HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
	elif mode=="audit":
		var points=[Vector2(.18,.22),Vector2(.65,.12),Vector2(.65,.45),Vector2(.65,.8),Vector2(.18,.8)]
		for edge in [[1,2],[2,3]]:draw_line(points[edge[0]]*size,points[edge[1]]*size,Color("8bb9c4"),3)
		for i in range(5):
			var p=points[i]*size
			draw_circle(p,23,Color("8ccbb6") if values[i]==1 else Color("607383"))
			draw_string(font,p+Vector2(-6,6),["A","B","C","D","E"][i],HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
