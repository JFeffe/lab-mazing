extends Control
# A small 2D diagram; processing stops as soon as the trial animation finishes.
var names=[]
var path=[]
var elapsed=0.0
const POS=[Vector2(.5,.06),Vector2(.5,.24),Vector2(.14,.43),Vector2(.72,.43),Vector2(.91,.64),Vector2(.44,.64),Vector2(.16,.87),Vector2(.72,.87)]
const EDGES=[[0,1,""],[1,2,"1"],[1,3,"2"],[3,5,"1"],[3,4,"2"],[5,6,"1"],[5,7,"2"]]
func _ready():
	mouse_filter=Control.MOUSE_FILTER_IGNORE
	set_process(not path.is_empty())
	queue_redraw()
func _process(delta):
	elapsed+=delta
	queue_redraw()
	if elapsed>=maxi(1,path.size()-1)*.35:set_process(false)
func _draw():
	if names.size()!=8:return
	var points=[]
	for v in POS:points.append(Vector2(24+v.x*(size.x-48),v.y*size.y))
	var font=ThemeDB.fallback_font
	for edge in EDGES:
		var a=points[edge[0]];var b=points[edge[1]]
		draw_line(a,b,Color("82949a"),2,true)
		var mid=(a+b)/2
		draw_string(font,mid+Vector2(6,-3),edge[2],HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color("ead6a3"))
	if path.size()>1:
		var progress=minf(elapsed/.35,path.size()-1)
		for i in range(path.size()-1):
			if progress<=i:break
			draw_line(points[path[i]],points[path[i]].lerp(points[path[i+1]],minf(1,progress-i)),Color("79e0b5"),5,true)
		var segment=mini(int(progress),path.size()-2)
		var capsule=points[path[segment]].lerp(points[path[segment+1]],minf(1,progress-segment))
		draw_circle(capsule,7,Color("ffd17a"))
	for i in range(8):
		draw_circle(points[i],6,Color("e7ece7"))
		var width=font.get_string_size(names[i],HORIZONTAL_ALIGNMENT_LEFT,-1,13).x
		draw_string(font,points[i]+Vector2(-width/2,-10),names[i],HORIZONTAL_ALIGNMENT_LEFT,-1,13,Color("e7ece7"))
