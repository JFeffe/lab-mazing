extends Control
var game
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
		var col=Color("e9be72")
		if e.kind=="clue": col=Color("85d8d2")
		if e.kind in ["mechanism","craft"]: col=Color("93aff0")
		if e.kind in ["door","oneway"]: col=Color("e28b73")
		if game.done.has(e.id): col=Color("538975")
		if e.kind=="exit": col=Color.WHITE
		draw_circle(offset+(Vector2(e.cell[0],e.cell[1])+Vector2.ONE*0.5)*cell,max(2,cell*0.28),col)
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
	var p=game.player.position/game.TILE
	var c=offset+(Vector2(p.x,p.z)+Vector2.ONE*0.5)*cell
	draw_circle(c,max(4,cell*0.35),Color("fff1d4"))
	draw_arc(c,max(6,cell*0.52),0,TAU,24,Color("e9be72"),2)
