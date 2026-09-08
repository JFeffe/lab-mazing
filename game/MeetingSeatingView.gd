extends Control
var labels=[]
func _ready():mouse_filter=Control.MOUSE_FILTER_IGNORE;queue_redraw()
func _draw():
	var font=ThemeDB.fallback_font
	var centre=size/2
	draw_style_box(panel(),Rect2(centre-Vector2(size.x*.2,55),Vector2(size.x*.4,110)))
	var points=[Vector2(.5,.06),Vector2(.85,.28),Vector2(.85,.63),Vector2(.5,.87),Vector2(.15,.63),Vector2(.15,.28)]
	for i in range(mini(6,labels.size())):
		var p=Vector2(points[i].x*size.x,points[i].y*size.y)
		var lines=labels[i].split("\n")
		draw_circle(p+Vector2(0,4),5,Color("d9b978"))
		draw_string(font,p+Vector2(-4,-7),lines[0],HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color("d9b978"))
		# Long duplicate groups remain in the controls below; keep the diagram compact.
		var name_v=lines[1] if lines[1].length()<15 else "+"+str(lines[1].split(" / ").size())
		var w=font.get_string_size(name_v,HORIZONTAL_ALIGNMENT_LEFT,-1,13).x
		draw_string(font,p+Vector2(-w/2,23),name_v,HORIZONTAL_ALIGNMENT_LEFT,-1,13,Color("e5eee6"))
	draw_line(Vector2(centre.x-15,size.y-2),Vector2(centre.x+15,size.y-2),Color("d9b978"),4)
func panel():
	var s=StyleBoxFlat.new();s.bg_color=Color("34535b");s.set_corner_radius_all(18);return s
