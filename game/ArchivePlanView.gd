extends Control
var values=[0,0,0]
func _draw():
	var w=size.x/11.0
	draw_rect(Rect2(Vector2.ZERO,size),Color("101e29"))
	for row in range(3):
		var gap=[1,4,7][values[row]]
		for x in range(9):
			if x==gap:continue
			draw_rect(Rect2((x+1)*w,18+row*48,w-2,30),Color("b79868"))
		draw_string(get_theme_default_font(),Vector2(5,40+row*48),["A","B","C"][row],HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
		draw_rect(Rect2((gap+1)*w,18+row*48,w-2,30),Color("518d87"),false,2)
