extends Control
var game
var route_preview=[]
var navigation_enabled=false

func _gui_input(event):
	if not navigation_enabled or game==null or not game.playing or game.won: return
	if event is InputEventMouseButton and event.pressed and event.button_index in [MOUSE_BUTTON_LEFT,MOUSE_BUTTON_RIGHT]:
		accept_event()
		var n=game.grid.size()
		var cell=min(size.x,size.y)/float(n)
		var offset=(size-Vector2.ONE*cell*n)/2
		var point=(event.position-offset)/cell
		if point.x<0 or point.y<0 or point.x>=n or point.y>=n: return
		var goal=Vector2i(floori(point.x),floori(point.y))
		if game.request_cell(goal): game.close_modal()

func _draw():
	if game==null: return
	var n=game.grid.size()
	var cell=min(size.x,size.y)/float(n)
	var offset=(size-Vector2.ONE*cell*n)/2
	draw_rect(Rect2(Vector2.ZERO,size),Color("101e29"))
	for y in range(n):
		for x in range(n):
			if not game.seen.has(game.key(x,y)): continue
			draw_rect(Rect2(offset+Vector2(x,y)*cell,Vector2.ONE*(cell-0.5)),Color("89a7a0") if game.floor_at(x,y) else Color("2a3e49"))
	for e in game.events:
		if not game.seen.has(game.key(e.cell[0],e.cell[1])): continue
		if e.kind=="pickup" and game.done.has(e.id): continue
		if e.kind=="collectible" and game.Subject16.has(game,e):continue
		var col=Color("e9be72")
		if e.kind=="clue": col=Color("85d8d2")
		if e.kind in ["mechanism","craft"]: col=Color("93aff0")
		if e.kind in ["door","oneway"]: col=Color("e28b73")
		if game.done.has(e.id): col=Color("538975")
		if e.kind=="exit": col=Color.WHITE
		if e.kind=="collectible":col=Color(game.Subject16.theme(game.level).color)
		draw_circle(offset+(Vector2(e.cell[0],e.cell[1])+Vector2.ONE*0.5)*cell,max(2,cell*0.28),col)
		if e.kind=="collectible":
			var center=offset+(Vector2(e.cell[0],e.cell[1])+Vector2.ONE*.5)*cell
			draw_arc(center,max(3,cell*.38),0,TAU,12,Color.WHITE,1)
		if game.LevelEndings.is_doctor(e):
			var point=offset+(Vector2(e.cell[0],e.cell[1])+Vector2.ONE*0.5)*cell
			draw_string(get_theme_default_font(),point+Vector2(-4,4),"F",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("152631"))
		if e.kind=="oneway":
			var c=offset+(Vector2(e.cell[0],e.cell[1])+Vector2.ONE*0.5)*cell
			var d=Vector2(e.direction[0],e.direction[1])*max(4,cell*0.45)
			draw_line(c-d,c+d,Color("fff0c9"),2)
			draw_line(c+d,c+Vector2(-d.y,d.x)*0.7,Color("fff0c9"),2)
			draw_line(c+d,c+Vector2(d.y,-d.x)*0.7,Color("fff0c9"),2)
	for sc in game.shortcuts:
		if not game.open_shortcuts.has(sc.id): continue
		var c=offset+(Vector2(sc.cell[0],sc.cell[1])+Vector2.ONE*0.5)*cell
		draw_rect(Rect2(c-Vector2.ONE*cell*0.4,Vector2.ONE*cell*0.8),Color("53cfaf"))
		if cell>10:
			draw_string(get_theme_default_font(),c+Vector2(-cell*0.5,3),sc.id,HORIZONTAL_ALIGNMENT_LEFT,-1,10,Color("122e29"))
	var route=game.move_path if not game.move_path.is_empty() else route_preview
	if not route.is_empty():
		var last=offset+(Vector2(game.player.position.x,game.player.position.z)/game.TILE+Vector2.ONE*0.5)*cell
		for step in route:
			var point=offset+(Vector2(step)+Vector2.ONE*0.5)*cell
			draw_line(last,point,Color("f3d58d"),max(1,cell*0.15))
			last=point
		draw_arc(last,max(4,cell*0.5),0,TAU,20,Color("fff1b8"),2)
	var p=game.player.position/game.TILE
	var c=offset+(Vector2(p.x,p.z)+Vector2.ONE*0.5)*cell
	draw_circle(c,max(4,cell*0.35),Color("fff1d4"))
	draw_arc(c,max(6,cell*0.52),0,TAU,24,Color("e9be72"),2)
